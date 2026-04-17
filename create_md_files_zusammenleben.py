import csv
import os
import re

def sanitize_filename(name):
    """Sanitize the name to be a valid filename."""
    name = re.sub(r'[^\w\s-]', '', name).strip()
    name = re.sub(r'[-\s]+', '-', name)
    return name

def create_markdown_files(csv_file_path, output_folder, mappings):
    os.makedirs(output_folder, exist_ok=True)

    with open(csv_file_path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filename_raw = row[mappings['filename']]
            filename = sanitize_filename(filename_raw) + ".md"
            file_path = os.path.join(output_folder, filename)

            yaml_frontmatter = {}
            if 'URL' in mappings and mappings['URL'] in row:
                yaml_frontmatter['URL'] = row[mappings['URL']]
            if 'Genossenschaft' in mappings and mappings['Genossenschaft'] in row:
                yaml_frontmatter['Genossenschaft'] = row[mappings['Genossenschaft']]
            if 'Typ Einträge' in mappings and mappings['Typ Einträge'] in row:
                yaml_frontmatter['Typ Einträge'] = row[mappings['Typ Einträge']]
            if 'Select' in mappings and mappings['Select'] in row:
                yaml_frontmatter['Select'] = row[mappings['Select']]

            body_content = row.get(mappings['body'], '')

            with open(file_path, 'w', encoding='utf-8') as md_file:
                if yaml_frontmatter:
                    md_file.write("---\
")
                    for key, value in yaml_frontmatter.items():
                        md_file.write(f"{key}: {value}\n")
                    md_file.write("---\
\n")
                md_file.write(body_content)
    print(f"Successfully created Markdown files in '{output_folder}'")

# Define the paths and mappings
csv_file = '/home/hanskanns/geminitest/gnossizh-ai/Assets/Einträge-Depositenkasse Import Obsidian.csv'
output_dir = '/home/hanskanns/geminitest/gnossizh-ai/Depositenkasse'
column_mappings = {
    'filename': 'Name',
    'URL': 'URL',
    'Genossenschaft': 'Genossenschaft',
    'Typ Einträge': 'Typ Einträge',
    'Select': 'Select',
    'body': 'AI Zusammenfassung Depositenkasse'
}

create_markdown_files(csv_file, output_dir, column_mappings)
