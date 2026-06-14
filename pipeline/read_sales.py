import csv

file_path = "data/raw/sales_sample.csv"

with open(file_path, "r", encoding ='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)