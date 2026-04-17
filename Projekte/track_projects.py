import os
import re
import json
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
import csv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- CONFIGURATION ---
# These would ideally come from environment variables in Coolify
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "YOUR_KEY_HERE")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "YOUR_BASE_HERE")
AIRTABLE_TABLE_PROJECTS = "Projekte"
AIRTABLE_TABLE_SOURCES = "Genossenschaften"

# Local backup paths
PROJECTS_CSV = "/home/gravity-test/gnossiZH/Projekte/Projekte_Datenbank.csv"
SOURCES_CSV = "/home/gravity-test/gnossiZH/Projekte/Projekte-Projektübersicht.csv"

# Regex patterns for discovery and extraction
PROJECT_LINK_PATTERNS = [re.compile(p, re.I) for p in [
    r"/projekt", r"/neubau", r"/areal", r"/bauvorhaben", r"/siedlung", 
    r"/zukunft", r"/entwicklung", r"/zeitraum", r"/bau", r"/quartier"
]]
PROJECT_TEXT_KEYWORDS = [
    "projekt", "neubau", "bauvorhaben", "entwicklung", "zukunft", 
    "areal", "zeitraum", "bau", "wohnen", "siedlung", "umbau", "category"
]
DATE_PATTERN = re.compile(r"(20\d{2})") # Simple year extraction
MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

class CoopScraper:
    def __init__(self):
        self.client = httpx.Client(follow_redirects=True, timeout=10.0)
    
    def fetch_page(self, url):
        try:
            response = self.client.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def discover_links(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(separator=' ', strip=True).lower()
            
            # Convert relative to absolute
            if href.startswith('/'):
                href = f"{base_url.rstrip('/')}/{href.lstrip('/')}"
            
            # Check URL for patterns
            url_match = any(pattern.search(href) for pattern in PROJECT_LINK_PATTERNS)
            
            # Check Link Text for keywords
            text_match = any(keyword in text for keyword in PROJECT_TEXT_KEYWORDS)
            
            if url_match or text_match:
                # Filter out obvious false positives
                href_lower = href.lower()
                blacklisted = ["facebook", "instagram", "twitter", "linkedin", "youtube", "mailto:", "tel:", "javascript:", ".pdf", ".jpg", ".png"]
                if any(b in href_lower for b in blacklisted):
                    continue
                links.add(href)
        return links

    def find_overview_page(self, homepage_url):
        print(f"  Attempting to discover overview page for {homepage_url}...")
        html = self.fetch_page(homepage_url)
        if not html: return homepage_url
        
        soup = BeautifulSoup(html, 'html.parser')
        possible_links = []
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(separator=' ', strip=True).lower()
            if href.startswith('/'):
                href = f"{homepage_url.rstrip('/')}/{href.lstrip('/')}"
            
            # Score links based on keywords
            score = 0
            if any(k in text for k in PROJECT_TEXT_KEYWORDS): score += 2
            if any(p.search(href) for p in PROJECT_LINK_PATTERNS): score += 1
            
            if score > 0:
                possible_links.append((score, href))
        
        if possible_links:
            # Sort by score descending and return the best one
            possible_links.sort(key=lambda x: x[0], reverse=True)
            best_link = possible_links[0][1]
            print(f"  Discovered potential overview: {best_link}")
            return best_link
            
        return homepage_url

    def extract_details(self, html, project_url):
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        
        # Look for external landing pages / rental pages
        landing_page = None
        for a in soup.find_all('a', href=True):
            a_text = a.get_text(separator=' ', strip=True).lower()
            if any(k in a_text for k in ["projektwebseite", "projekt-webseite", "vermietung", "landingpage", "projektseite"]):
                href = a['href']
                if href.startswith('http') and project_url.split('/')[2] not in href: # External domain
                    landing_page = href
                    break

        details = {
            "name": soup.title.string.split('|')[0].strip() if soup.title else "Unknown Project",
            "baustart": self.find_date_near(text, "Baustart"),
            "bezug": self.find_date_near(text, "Bezug"),
            "vermietung": self.find_date_near(text, "Vermietung"),
            "url": project_url,
            "landing_page": landing_page
        }
        return details

    def find_date_near(self, text, keyword):
        # Look for the keyword and then a year nearby (within 100 characters)
        start_idx = text.lower().find(keyword.lower())
        if start_idx == -1:
            return None
        
        fragment = text[start_idx : start_idx + 100]
        match = DATE_PATTERN.search(fragment)
        if match:
            return match.group(1)
        return None

    def run_sync(self, test_mode=False):
        print(f"Starting sync at {datetime.now()}")
        
        try:
            from pyairtable import Api
        except ImportError:
            print("pyairtable not found. Skipping sync.")
            return

        api = Api(AIRTABLE_API_KEY)
        table_sources = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_SOURCES)
        
        # 1. Load Sources from Airtable (Master Source)
        records = table_sources.all()
        print(f"Loaded {len(records)} cooperatives from Airtable.")

        all_projects = []

        for record in records:
            fields = record['fields']
            name = fields.get('Name')
            homepage = fields.get('Website')
            overview_url = fields.get('Projektübersicht')
            record_id = record['id']

            if not name: continue
            
            # Decide on the start URL for scanning
            # If we don't have an overview URL but we have a homepage, discover it.
            final_url = overview_url
            is_new_discovery = False

            if not final_url and homepage:
                # Extract just the URL if there is surrounding text
                url_match = re.search(r"(https?://\S+[^.,; \n\r])", homepage)
                homepage_clean = url_match.group(1) if url_match else homepage
                
                final_url = self.find_overview_page(homepage_clean)
                if final_url and final_url != homepage_clean:
                    is_new_discovery = True
            
            if not final_url:
                print(f"Skipping {name}: No overview URL or homepage found.")
                continue

            # Update Airtable if we discovered a NEW overview page
            if is_new_discovery:
                print(f"  Saving discovered overview for {name}: {final_url}")
                table_sources.update(record_id, {"Projektübersicht": final_url})

            print(f"Scanning {name} -> {final_url}")
            html = self.fetch_page(final_url)
            if not html: continue

            # Discovery
            project_links = self.discover_links(html, final_url)
            print(f"  Found {len(project_links)} potential project links")

            for p_url in project_links:
                p_html = self.fetch_page(p_url)
                if p_html:
                    details = self.extract_details(p_html, p_url)
                    details['cooperative'] = name
                    all_projects.append(details)
                    if test_mode: break
            
            if test_mode: break

        # 2. Update Airtable Projects
        self.push_to_airtable(all_projects)

    def save_to_csv(self, projects):
        keys = projects[0].keys() if projects else []
        with open(PROJECTS_CSV, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(projects)
        print(f"Saved {len(projects)} projects to {PROJECTS_CSV}")

    def push_to_airtable(self, projects):
        try:
            from pyairtable import Api
        except ImportError:
            print("pyairtable not found. Skipping push.")
            return

        api = Api(AIRTABLE_API_KEY)
        table_projects = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_PROJECTS)
        table_sources = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_SOURCES)
        
        # 1. Map Cooperative Names to Record IDs
        sources_records = table_sources.all()
        name_to_id = {r['fields'].get('Name'): r['id'] for r in sources_records if 'Name' in r['fields']}
        
        # 2. Get existing projects to avoid duplicates (using URL as the key)
        # Note: In your schema, the URL field is named 'URL'
        existing_projects = table_projects.all()
        url_to_id = {r['fields'].get('URL'): r['id'] for r in existing_projects if 'URL' in r['fields']}

        for p in projects:
            # Prepare fields based on your Airtable schema
            fields = {
                "Projektname": p['name'],
                "URL": p['url'],
                "Zeitplan": p['baustart'],
                "Stat Bezug": p['bezug'],
                "Start Vermietung": p['vermietung'],
                "Vermietungsseite": p.get('landing_page'),
                "Status Bauprojekt": "Ausschreibung läuft" if p['baustart'] else "Projekt geplant",
                "Notes 2": f"Automatisch aktualisiert am {datetime.now().strftime('%d.%m.%Y')}"
            }
            
            # Map the cooperative link
            coop_name = p['cooperative']
            if coop_name in name_to_id:
                fields["Genossenschaft"] = [name_to_id[coop_name]]
            
            if p['url'] in url_to_id:
                print(f"Updating {p['name']}...")
                table_projects.update(url_to_id[p['url']], fields)
            else:
                print(f"Creating {p['name']}...")
                table_projects.create(fields)

if __name__ == "__main__":
    scraper = CoopScraper()
    scraper.run_sync(test_mode=False)
