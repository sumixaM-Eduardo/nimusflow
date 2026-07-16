from datetime import datetime
import logging
from pipeline.schema_loader import load_schema

def clean_data(sales):
    schema = load_schema()
    logging.info('Cleaning data...')
    for sale in sales:
        for field in schema['fields']:
            sale[field['name']] = sale[field['name']].strip()
    logging.info(f'{len(sales)} records cleaned')
    return sales

def convert_data(sales):
    schema = load_schema()
    converts = {'int': int, 'float':  float}
    valid_sales = []
    invalid_sales = []
    logging.info('Converting data types...')
    for sale in sales:
        try:
            for field in schema['fields']:
                if field['type'] == 'date':
                    sale[field['name']] = datetime.strptime(sale[field['name']], field['format'])
                elif field['type'] == 'string':
                    continue
                else:
                    sale[field['name']] = converts[field['type']](sale[field['name']])
        except ValueError:
            invalid_sales.append(sale)
            continue
        valid_sales.append(sale)
    logging.info(f'{len(valid_sales)} valid | {len(invalid_sales)} invalid after conversion')
    return valid_sales, invalid_sales

def validate_data(valid_sales, invalid_sales):
    schema = load_schema()
    approved_sales = []
    rejected_sales = []
    logging.info('Validating business rules...')
    for sale in valid_sales:
        rejected = False
        for field in schema['fields']:
            if ('min' in field and sale[field['name']] < field['min']) or (field.get('required') and sale[field['name']] == ''):
                rejected_sales.append(sale)
                rejected = True
                break
        if not rejected:
            approved_sales.append(sale)
    rejected_sales.extend(invalid_sales)
    logging.info(f'{len(approved_sales)} approved | {len(rejected_sales)} rejected after validation')
    return approved_sales, rejected_sales