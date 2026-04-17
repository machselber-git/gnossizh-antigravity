import csv
import os
import datetime
import re

# --- CONFIGURATION ---

# Get the absolute path of the directory the script is in.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Path to the input CSV file, relative to the script's location.
CSV_FILE_PATH = os.path.join(SCRIPT_DIR, 'Assets', 'Einträge-Statuten und Vermietungsbestimmungen.csv')

# --- New: Date-based output folder ---
TODAY_STR = datetime.date.today().isoformat()  # e.g., '2026-03-12'
BASE_OUTPUT_DIR = os.path.join(SCRIPT_DIR, TODAY_STR)

# 2. Directory configuration, now inside the date-based folder.
OUTPUT_DIR_CONFIG = {
    'mapping_column': 'Typ Einträge',  # Column to determine the directory
    'directories': {
        'Statuten': os.path.join(BASE_OUTPUT_DIR, 'anteilsscheine'),
        'Vermietungsbestimmungen': os.path.join(BASE_OUTPUT_DIR, 'vermietungsbestimmungen'),
        'Zusammenleben': os.path.join(BASE_OUTPUT_DIR, 'Zusammenleben'),
        'Depositenkasse': os.path.join(BASE_OUTPUT_DIR, 'Depositenkasse'),
        '__default__': os.path.join(BASE_OUTPUT_DIR, 'uncategorized')
    }
}

# 3. Filename configuration
FILENAME_COLUMN = 'Name'
FILENAME_SUFFIX = '.md'

# 4. Markdown content structure
CONTENT_STRUCTURE = [
    ('title', 'Name'),
    ('property', 'Typ Einträge'),
    ('line', '---'),
    ('raw', 'AI assist')
]

# --- END OF CONFIGURATION ---


def sanitize_filename(name):
    """
    Removes invalid characters from a string to make it a valid filename.
    """
    # Remove invalid file system characters
    s = re.sub(r'[\\/*?:"<>|]', "", name)
    # Replace whitespace sequences with a single underscore
    s = re.sub(r'\s+', '_', s)
    return s


def create_markdown_files():
    """
    Parses the CSV file and creates markdown files based on the configuration.
    """
    
    # --- Directory Setup ---
    print(f"Creating base output directory: {BASE_OUTPUT_DIR}")
    os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)
    if isinstance(OUTPUT_DIR_CONFIG, dict):
        all_dirs = list(OUTPUT_DIR_CONFIG['directories'].values())
        for dir_path in all_dirs:
            os.makedirs(dir_path, exist_ok=True)
    else:
        print("Error: Invalid OUTPUT_DIR_CONFIG. Must be a dictionary.")
        return

    # --- CSV Processing ---
    try:
        # Using 'utf-8-sig' to handle potential BOM at the start of the file
        with open(CSV_FILE_PATH, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            
            print("CSV Header detected:", reader.fieldnames)

            for i, row in enumerate(reader):
                # --- Determine Output Directory ---
                key_column = OUTPUT_DIR_CONFIG['mapping_column']
                key_value = row.get(key_column, '').strip()
                output_dir = OUTPUT_DIR_CONFIG['directories'].get(key_value, OUTPUT_DIR_CONFIG['directories']['__default__'])

                # --- Determine Filename ---
                base_name = row.get(FILENAME_COLUMN, f'Unnamed_File_{i+1}').strip()
                if not base_name:
                    base_name = f'Unnamed_File_{i+1}'
                
                sanitized_base_name = sanitize_filename(base_name)
                filename = f"{sanitized_base_name}{FILENAME_SUFFIX}"
                file_path = os.path.join(output_dir, filename)

                # --- Generate Markdown Content ---
                md_content = ""
                for item_type, value in CONTENT_STRUCTURE:
                    if item_type == 'title':
                        md_content += f"# {row.get(value, '').strip()}\n\n"
                    elif item_type == 'property':
                        md_content += f"**{value.strip()}:** {row.get(value, '').strip()}\n\n"
                    elif item_type == 'raw':
                        md_content += f"{row.get(value, '').strip()}\n"
                    elif item_type == 'line':
                        md_content += f"---\n\n"
                
                # --- Write File ---
                try:
                    with open(file_path, 'w', encoding='utf-8') as md_file:
                        md_file.write(md_content)
                    print(f"Created: {file_path}")
                except IOError as e:
                    print(f"Error writing file {file_path}: {e}")

    except FileNotFoundError:
        print(f"Error: The file was not found at {CSV_FILE_PATH}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    create_markdown_files()
    print("Processing complete.")
