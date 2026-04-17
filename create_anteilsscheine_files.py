import csv
import os

# Define paths
csv_file_path = '/home/hanskanns/geminitest/gnossizh-ai/Assets/Einträge-Anteilssscheine Import Obsidian.csv'
output_dir = '/home/hanskanns/geminitest/gnossizh-ai/anteilsscheine'
os.makedirs(output_dir, exist_ok=True)

# Correctly identify the header row in the CSV
header = []
rows = []
with open(csv_file_path, 'r', encoding='utf-8-sig') as infile:
    reader = csv.reader(infile)
    # Find the header row, assuming it's the first non-empty row
    for row in reader:
        if any(field.strip() for field in row):
            header = [h.strip() for h in row]
            break
    
    # Find the column indices
    try:
        name_idx = header.index("Name")
        url_idx = header.index("URL")
        genossenschaft_idx = header.index("Genossenschaft")
        typ_eintraege_idx = header.index("Typ Einträge")
        select_idx = header.index("Select")
        ai_summary_idx = header.index("AI Summary Anteilsscheine") # Assuming this is the correct column name for the new CSV
    except ValueError as e:
        print(f"Error: Missing expected column in header: {e}")
        print(f"Header found: {header}")
        exit(1)

    # Process the rest of the rows
    for row in reader:
        if len(row) < len(header):
            continue # Skip malformed or empty rows

        name = row[name_idx].strip()
        url = row[url_idx].strip()
        genossenschaft = row[genossenschaft_idx].strip()
        typ_eintraege = row[typ_eintraege_idx].strip()
        select = row[select_idx].strip()
        ai_summary = row[ai_summary_idx].strip()

        if not name:
            continue # Skip rows without a name

        # Sanitize filename
        safe_filename = name.replace('/', '_').replace('\\', '_')
        md_file_path = os.path.join(output_dir, f"{safe_filename}.md")

        # Create MD content with YAML frontmatter
        content = f"""---
URL: {url}
Genossenschaft: \"[[{genossenschaft}]]\"\nTyp Einträge: {typ_eintraege}\nSelect: {select}\n---\n\n{ai_summary}\n"""

        # Write the content to the new .md file
        with open(md_file_path, 'w', encoding='utf-8') as md_file:
            md_file.write(content)
        print(f"Created file: {md_file_path}")

print("Processing complete.")