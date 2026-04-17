
import csv
import os

# Define the input CSV file and output directory
csv_filename = "/home/hanskanns/geminitest/gnossizh-ai/Einträge-Vermietungsbestimmungen Import Obsidian.csv"
output_dir = 'vermietungsbestimmungen'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Open the CSV file
with open(csv_filename, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Extract data from the row
        name = row['Name']
        url = row['URL']
        genossenschaft = row['Genossenschaft']
        typ_eintrage = row['Typ Einträge']
        select = row['Select']
        ai_summary = row['AI Summary Vermietungsbestimmungen']

        # Create the Markdown file name
        md_filename = os.path.join(output_dir, f'{name}.md')

        # Create the YAML frontmatter
        yaml_frontmatter = f"""---
URL: {url}
Genossenschaft: "[[{genossenschaft}]]"
Typ Einträge: {typ_eintrage}
Select: {select}
---
"""

        # Combine YAML frontmatter and AI summary
        md_content = yaml_frontmatter + '\n' + ai_summary

        # Write the content to the Markdown file
        with open(md_filename, 'w', encoding='utf-8') as md_file:
            md_file.write(md_content)

print(f'{len(os.listdir(output_dir))} Markdown files created in the "{output_dir}" directory.')
