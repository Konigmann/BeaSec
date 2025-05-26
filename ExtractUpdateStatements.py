import os
import re

# Settings
input_directory = 'C:/http/info/hypercat.info/sql'  # Change to your directory
output_file = 'C:/temp/extracted_updates.sql'
max_lines = 100

# Regex patterns
update_start_pattern = re.compile(r'^\s*UPDATE\s+.*\bRegion\b', re.IGNORECASE)
set_uuid_pattern = re.compile(r'\bSET\b.*\bRegionUuid\b', re.IGNORECASE | re.DOTALL)



def extract_update_statements(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = []
        for i in range(max_lines):
            line = f.readline()
            if not line:
                break
            lines.append(line)

    # Join lines for easier multi-line pattern matching
    content = ''.join(lines)
    
    # Try to find all potential UPDATE statements to Region
    update_statements = []
    statement_blocks = re.split(r';\s*\n', content)

    for block in statement_blocks:
        if update_start_pattern.search(block) and set_uuid_pattern.search(block):
            # Clean up and normalize
            update_statements.append(block.strip() + '\n\n\n')
    
    return update_statements



def main():
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for filename in os.listdir(input_directory):
            if filename.lower().endswith('.sql'):
                file_path = os.path.join(input_directory, filename)
                updates = extract_update_statements(file_path)
                for update in updates:
                    out_file.write(f'-- From file: {filename}\n')
                    out_file.write(update)

    print(f'Extraction complete. See: {output_file}')

if __name__ == '__main__':
    main()
