from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os

load_dotenv()
pathdb = os.getenv('DATABASE_PATH')
app = FastAPI()

class Sale(BaseModel):
    order_id: int
    customer_id: int
    product_name: str
    quantity: int
    unit_price: float
    sale_date: str
    payment_method: str
    city: str

def get_connection():
    conn = sqlite3.connect(pathdb)
    cursor = conn.cursor()
    return conn, cursor

def row_to_dict(cursor):
    columns = [col[0] for col in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return data

def get_sales():
    conn, cursor = get_connection()
    cursor.execute("SELECT * FROM sales")
    data = row_to_dict(cursor)
    conn.close()
    return data

def get_sale_by_id(id: int):
    conn, cursor = get_connection()
    cursor.execute('SELECT * FROM sales WHERE order_id = ?', (id,))
    data = row_to_dict(cursor)
    conn.close()
    return data

def get_sale_by_city(city: str):
    conn, cursor = get_connection()
    cursor.execute('SELECT * FROM sales WHERE city = ?', (city,))
    data = row_to_dict(cursor)
    conn.close()
    return data

def get_sale_by_payment_method(payment_method: str):
    conn, cursor = get_connection()
    cursor.execute('SELECT * FROM sales WHERE payment_method = ?', (payment_method,))
    data = row_to_dict(cursor)
    conn.close()
    return data

def get_rejected_sales():
    conn, cursor = get_connection()
    cursor.execute('SELECT * FROM rejected_sales')
    data = row_to_dict(cursor)
    conn.close()
    return data

def get_summary():
    conn, cursor = get_connection()
    cursor.execute('SELECT(SELECT COUNT(*) FROM sales)+(SELECT COUNT(*) FROM rejected_sales) AS total_records,(SELECT SUM(unit_price) FROM sales) AS total_sum;')
    data = row_to_dict(cursor)
    conn.close()
    return data

def insert_sale(sale):
    conn, cursor = get_connection()
    cursor.execute('INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (sale.order_id, sale.customer_id, sale.product_name, sale.quantity, sale.unit_price, sale.sale_date, sale.payment_method, sale.city))
    conn.commit()
    conn.close()

def remove_sale(order_id: int):
    conn, cursor = get_connection()
    cursor.execute('DELETE FROM sales WHERE order_id = ?', (order_id,))
    conn.commit()
    conn.close()

@app.get('/sales')
def list_sales():
    sales = get_sales()
    return sales

@app.get('/sales/city/{city}')
def list_get_sales_city(city: str):
    data = get_sale_by_city(city)
    return data

@app.get('/sales/payment_method/{payment_method}')
def list_get_sales_payment_method(payment_method: str):
    data = get_sale_by_payment_method(payment_method)
    return data

@app.get('/rejected')
def list_rejected():
    data = get_rejected_sales()
    return data

@app.get('/sales/{order_id}')
def list_get_sales_id(order_id: int):
    data = get_sale_by_id(order_id)
    return data

@app.get('/summary')
def summary():
    data = get_summary()
    return data

@app.post('/sales')
def create_sale(sale: Sale):
    insert_sale(sale)
    return {
        "message": "Sale created successfully"
    }

@app.delete('/sales/{order_id}')
def delete_sale(order_id: int):
    remove_sale(order_id)
    return {
        'message': 'Sale deleted successfully'
    }