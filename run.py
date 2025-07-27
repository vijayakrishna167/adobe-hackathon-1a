# run.py
import os
import json
from src.processing import extract_outline_from_pdf

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

def main():
    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Process each PDF in the input directory
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"Processing: {pdf_path}")

            # Extract the outline
            result = extract_outline_from_pdf(pdf_path)

            # Create the corresponding JSON output file
            output_filename = os.path.splitext(filename)[0] + '.json'
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            with open(output_path, 'w') as f:
                json.dump(result, f, indent=4)

            print(f"Successfully created output: {output_path}")

if __name__ == '__main__':
    main()