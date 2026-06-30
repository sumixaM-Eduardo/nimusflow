from dotenv import load_dotenv
import os
import logging
import csv

load_dotenv()
pathcsv = os.getenv('RAW_CSV_PATH')
def extract():
    logging.info('Extracting data from csv')
    with open(pathcsv, "r", encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        sales = list(reader)
    logging.info(f'extracted: {len(sales)} records')
    return sales