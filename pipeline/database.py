from dotenv import load_dotenv
import os
import psycopg2
import logging
load_dotenv()

def get_connection():
    conn = psycopg2.connect(host = os.getenv('DB_HOST'), dbname = os.getenv('DB_NAME'), user = os.getenv('DB_USER'), password = os.getenv('DB_PASSWORD'), port = os.getenv('DB_PORT'))
    cursor = conn.cursor()
    return conn, cursor

def create_table():
    conn, cursor = get_connection()
    logging.info('Creating tables if not exists...')
    cursor.execute('CREATE TABLE IF NOT EXISTS sales (order_id INTEGER, customer_id INTEGER, product_name TEXT, quantity INTEGER, unit_price REAL, sale_date TEXT, payment_method TEXT, city TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS rejected_sales (order_id TEXT, customer_id TEXT, product_name TEXT, quantity TEXT, unit_price TEXT, sale_date TEXT, payment_method TEXT, city TEXT)')
    conn.commit()
    conn.close()
    logging.info('Table ready')

def insert_data(approved_sales, rejected_sales):
    conn, cursor = get_connection()
    logging.info('Loading data into database')
    for sale in approved_sales:
        cursor.execute('INSERT INTO sales VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', (sale['order_id'], sale['customer_id'], sale['product_name'],sale['quantity'], sale['unit_price'], sale['sale_date'].strftime('%Y-%m-%d'), sale['payment_method'], sale['city']))
    for sale in rejected_sales:
        cursor.execute('INSERT INTO rejected_sales VALUES(%s, %s, %s, %s, %s, %s, %s, %s)',(sale['order_id'], sale['customer_id'], sale['product_name'], sale['quantity'],sale['unit_price'], sale['sale_date'], sale['payment_method'], sale['city']))
    conn.commit()
    conn.close()
    logging.info(f'{len(approved_sales)} records loaded | {len(rejected_sales)} rejected')
