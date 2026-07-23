from dotenv import load_dotenv
from pipeline.schema_loader import load_schema
import os
import psycopg2
import logging
load_dotenv()

sql_type = {'int':'INTEGER', 'float':'REAL', 'string':'TEXT', 'date':'TEXT'}

def get_connection():
    conn = psycopg2.connect(host = os.getenv('DB_HOST'), dbname = os.getenv('DB_NAME'), user = os.getenv('DB_USER'), password = os.getenv('DB_PASSWORD'), port = os.getenv('DB_PORT'))
    cursor = conn.cursor()
    return conn, cursor

def create_table():
    collums = []
    schema = load_schema()
    for field in schema['fields']:
        if field.get('primary_key'):
            collums.append(f"{field['name']} {sql_type[field['type']]} PRIMARY KEY")
        else:
            collums.append(f"{field['name']} {sql_type[field['type']]}")
    sql_collums = ', '.join(collums)
    conn, cursor = get_connection()
    logging.info('Creating tables if not exists...')
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {schema["table_name"]} ({sql_collums})')
    cursor.execute('CREATE TABLE IF NOT EXISTS rejected_sales (order_id TEXT, customer_id TEXT, product_name TEXT, quantity TEXT, unit_price TEXT, sale_date TEXT, payment_method TEXT, city TEXT)')
    conn.commit()
    conn.close()
    logging.info('Table ready')

def insert_data(approved_sales, rejected_sales):
    schema = load_schema()
    placeholders = ', '.join(['%s'] * len(schema['fields']))
    conn, cursor = get_connection()
    logging.info('Loading data into database')
    duplicates = 0
    for sale in approved_sales:
        values = []
        for field in schema['fields']:
            if field['type'] == 'date':
                values.append(sale[field['name']].strftime('%Y-%m-%d'))
            else:
                values.append(sale[field['name']])
        try:
            cursor.execute(f'INSERT INTO {schema["table_name"]} VALUES({placeholders})', values)
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            duplicates += 1
            continue
    for sale in rejected_sales:
        values = []
        for field in schema['fields']:
            values.append(sale[field['name']])
        cursor.execute(f'INSERT INTO rejected_sales VALUES({placeholders})', values)
    conn.commit()
    conn.close()
    logging.info(f'{len(approved_sales) - duplicates} records loaded | {duplicates} duplicates skipped | {len(rejected_sales)} rejected')