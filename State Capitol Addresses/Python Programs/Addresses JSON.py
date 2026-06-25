import csv
import json


INPUT_FILE  = "capitol-buildings-by-state-2026.csv"   
OUTPUT_FILE = "state_capitals.json"

def csv_to_json(input_file, output_file):
    capitals = []

    with open(input_file, newline="", encoding="latin-1") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Strip extra whitespace from keys and values
            cleaned_row = {k.strip(): v.strip() for k, v in row.items()}
            capitals.append(cleaned_row)

    with open(output_file, "w", encoding="utf-8") as jsonfile:
        json.dump(capitals, jsonfile, indent=4)

    print(f"Success! {len(capitals)} records written to '{output_file}'")

if __name__ == "__main__":
    csv_to_json(INPUT_FILE, OUTPUT_FILE)
