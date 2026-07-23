import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, create_model
import os
from pipeline.schema_loader import load_schema

load_dotenv()
app = FastAPI()

python_types = {'int': int, 'float': float, 'string': str, 'date': str}

_schema = load_schema()
_fields = {}
for field in _schema['fields']:
    _fields[field['name']] = (python_types[field['type']], ...)

Sale = create_model('Sale', **_fields)

def get_connection():
    conn = psycopg2.connect(host = os.getenv('DB_HOST'), dbname = os.getenv('DB_NAME'), user = os.getenv('DB_USER'),password = os.getenv('DB_PASSWORD'), port = os.getenv('DB_PORT'))
    cursor = conn.cursor()
    return conn, cursor

def row_to_dict(cursor):
    columns = [col[0] for col in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return data

def get_sales():
    schema = load_schema()
    conn, cursor = get_connection()
    cursor.execute(f'SELECT * FROM {schema["table_name"]}')
    data = row_to_dict(cursor)
    conn.close()
    return data

def get_sale_by_id(id: int):
    schema = load_schema()
    conn, cursor = get_connection()
    cursor.execute(f'SELECT * FROM {schema["table_name"]} WHERE order_id = %s', (id,))
    data = row_to_dict(cursor)
    conn.close()
    return data

def get_sale_by_city(city: str):
    schema = load_schema()
    conn, cursor = get_connection()
    cursor.execute(f'SELECT * FROM {schema["table_name"]} WHERE city = %s', (city,))
    data = row_to_dict(cursor)
    conn.close()
    return data

def get_sale_by_payment_method(payment_method: str):
    schema = load_schema()
    conn, cursor = get_connection()
    cursor.execute(f'SELECT * FROM {schema["table_name"]} WHERE payment_method = %s', (payment_method,))
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
    schema = load_schema()
    conn, cursor = get_connection()
    cursor.execute(f'SELECT(SELECT COUNT(*) FROM {schema["table_name"]})+(SELECT COUNT(*) FROM rejected_sales) AS total_records,(SELECT SUM(unit_price) FROM {schema["table_name"]}) AS total_sum;')
    data = row_to_dict(cursor)
    conn.close()
    return data

def insert_sale(sale):
    schema = load_schema()
    placeholders = ', '.join(['%s'] * len(schema['fields']))
    values = []
    for field in schema['fields']:
        values.append(getattr(sale, field['name']))
    conn, cursor = get_connection()
    cursor.execute(f'INSERT INTO {schema["table_name"]} VALUES({placeholders})', values)
    conn.commit()
    conn.close()

def remove_sale(order_id: int):
    schema = load_schema()
    conn, cursor = get_connection()
    cursor.execute(f'DELETE FROM {schema["table_name"]} WHERE order_id = %s', (order_id,))
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