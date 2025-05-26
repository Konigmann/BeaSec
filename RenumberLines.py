#   Usage:  python update_ln_tags.py input.txt output.txt
#   Usage:  python "C:\Users\windo\Documents\SL Toys\LSL\RenumberLines.py"  C:\Users\windo\AppData\Local\Temp\sl_script__Bunny's-MultiTeleporter50524.0747.ossl_0191de0aad770f55c8e1b4ffe2b83caa.lsl  C:\Users\windo\AppData\Local\Temp\sl_script__Bunny's-MultiTeleporter50524.0747.ossl_0191de0aad770f55c8e1b4ffe2b83caa.lsl 


import re
import sys
import os


# Pattern: Ln followed by 3 or 4 digits and a colon
pattern = re.compile(r'Ln\d{3,4}:')


def update_ln_tags_by_line_number(lines):
    updated_lines = []

    for i, line in enumerate(lines, start=1):
        # Replace all Ln####: occurrences with Ln<line_number>:
        updated_line = pattern.sub(f'Ln{str(i).zfill(4)}:', line)
        updated_lines.append(updated_line)

    return updated_lines


def main():
    if len(sys.argv) != 3:
        print("Usage: python update_ln_tags_by_line.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: input file '{input_file}' does not exist.")
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated_lines = update_ln_tags_by_line_number(lines)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

    print(f"Updated tags written to: {output_file}")


if __name__ == '__main__':
    main()
