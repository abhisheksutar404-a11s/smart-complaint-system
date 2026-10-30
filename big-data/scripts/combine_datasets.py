
import csv
from pathlib import Path

# Locate the data folder
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

# Input and output files
original_file = data_folder / "complaints.csv"
synthetic_file = data_folder / "synthetic_complaints.csv"
output_file = data_folder / "all_complaints.csv"

# Read column names from the original CSV
with open(original_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames

    if not fieldnames:
        raise ValueError("Original CSV has no column headers.")

# Combine both datasets
total_records = 0

with open(output_file, "w", newline="", encoding="utf-8") as output:
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for input_file in [original_file, synthetic_file]:

        with open(input_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames != fieldnames:
                raise ValueError(
                    f"Column mismatch in {input_file.name}"
                )

            for row in reader:
                category = (row.get("category") or "").strip()

                if category.lower() == "road":
                    continue

                writer.writerow(row)
                total_records += 1

print("Datasets combined successfully!")
print("Total complaints:", total_records)
print("Output file:", output_file)
