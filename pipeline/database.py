import sqlite3

pathdb = '/data/sales.db'

def create_table():
    conn = sqlite3.connect(pathdb)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS sales (order_id INTEGER, customer_id INTEGER, product_name TEXT, quantity INTEGER, unit_price REAL, sale_date TEXT, payment_method TEXT, city TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS rejected_sales (order_id TEXT, customer_id TEXT, product_name TEXT, quantity TEXT, unit_price TEXT, sale_date TEXT, payment_method TEXT, city TEXT)')
    conn.commit()
    conn.close()

def insert_data(approved_sales, rejected_sales):
    conn = sqlite3.connect(pathdb)
    cursor = conn.cursor()
    for sale in approved_sales:
        cursor.execute('INSERT INTO sales VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (sale['order_id'], sale['customer_id'], sale['product_name'],sale['quantity'], sale['unit_price'], sale['sale_date'], sale['payment_method'], sale['city']))
    for sale in rejected_sales:
        cursor.execute('INSERT INTO sales VALUES(?, ?, ?, ?, ?, ?, ?, ?)',(sale['order_id'], sale['customer_id'], sale['product_name'], sale['quantity'],sale['unit_price'], sale['sale_date'], sale['payment_method'], sale['city']))
    conn.commit()
    conn.close()
