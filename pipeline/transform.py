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
    valid_sales = []
    invalid_sales = []
    logging.info('Converting data types...')
    for sale in sales:
        try:
            sale['order_id'] = int(sale['order_id'])
        except ValueError:
            invalid_sales.append(sale)
            continue
        try:
            sale['customer_id'] = int(sale['customer_id'])
        except ValueError:
            invalid_sales.append(sale)
            continue
        try:
            sale['quantity'] = int(sale['quantity'])
        except ValueError:
            invalid_sales.append(sale)
            continue
        try:
            sale['unit_price'] = float(sale['unit_price'])
        except ValueError:
            invalid_sales.append(sale)
            continue
        try:
            sale['sale_date'] = datetime.strptime(sale['sale_date'], '%Y-%m-%d')
        except ValueError:
            invalid_sales.append(sale)
            continue
        valid_sales.append(sale)
    logging.info(f'{len(valid_sales)} valid | {len(invalid_sales)} invalid after conversion')
    return valid_sales, invalid_sales

def validate_data(valid_sales, invalid_sales):
    approved_sales = []
    rejected_sales = []
    logging.info('Validating business rules...')
    for sale in valid_sales:
        if sale['order_id'] <= 0:
            rejected_sales.append(sale)
            continue
        if sale['customer_id'] <= 0:
            rejected_sales.append(sale)
            continue
        if sale['product_name'] == '':
            rejected_sales.append(sale)
            continue
        if sale['quantity'] <= 0:
            rejected_sales.append(sale)
            continue
        if sale['unit_price'] <= 0:
            rejected_sales.append(sale)
            continue
        if sale['payment_method'] == '':
            rejected_sales.append(sale)
            continue
        if sale['city'] == '':
            rejected_sales.append(sale)
            continue
        approved_sales.append(sale)
    rejected_sales.extend(invalid_sales)
    logging.info(f'{len(approved_sales)} approved | {len(rejected_sales)} rejected after validation')
    return approved_sales, rejected_sales