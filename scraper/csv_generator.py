import csv
class CsvGenerator:
    def __init__(self):
        pass

   
    def Generate_Csv(self, Registry, file_pathname):
        if not Registry:
            raise Exception("registry is not defined")

        filtered = [row for row in Registry if row.get("time") != "NO_TIME"]

        fieldnames = ["site_origin", "title", "desc", "url", "time"]

        with open(file_pathname, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(Registry)

        filtered_path = "csv_data/filtered.csv"
        with open(filtered_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered)