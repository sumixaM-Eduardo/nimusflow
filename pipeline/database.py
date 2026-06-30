from dotenv import load_dotenv
import os
import sqlite3
import logging

load_dotenv()
pathdb = os.getenv('DATABASE_PATH')

def create_table():
    conn = sqlite3.connect(pathdb)
    cursor = conn.cursor()
    logging.info('Creating tables if not exists...')
    cursor.execute('CREATE TABLE IF NOT EXISTS sales (order_id INTEGER, customer_id INTEGER, product_name TEXT, quantity INTEGER, unit_price REAL, sale_date TEXT, payment_method TEXT, city TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS rejected_sales (order_id TEXT, customer_id TEXT, product_name TEXT, quantity TEXT, unit_price TEXT, sale_date TEXT, payment_method TEXT, city TEXT)')
    conn.commit()
    conn.close()
    logging.info('Table ready')

def insert_data(approved_sales, rejected_sales):
    conn = sqlite3.connect(pathdb)
    cursor = conn.cursor()
    logging.info('Loading data into database')
    for sale in approved_sales:
        cursor.execute('INSERT INTO sales VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (sale['order_id'], sale['customer_id'], sale['product_name'],sale['quantity'], sale['unit_price'], sale['sale_date'].strftime('%Y-%m-%d'), sale['payment_method'], sale['city']))
    for sale in rejected_sales:
        cursor.execute('INSERT INTO rejected_sales VALUES(?, ?, ?, ?, ?, ?, ?, ?)',(sale['order_id'], sale['customer_id'], sale['product_name'], sale['quantity'],sale['unit_price'], sale['sale_date'], sale['payment_method'], sale['city']))
    conn.commit()
    conn.close()
    logging.info(f'{len(approved_sales)} records loaded | {len(rejected_sales)} rejected')
