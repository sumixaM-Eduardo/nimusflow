from fastapi import FastAPI
import sqlite3

path_db = 'data/sales.db'
app = FastAPI()

def row_to_dict(cursor):
    columns = [col[0] for col in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return data

def get_sales():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales")
    data = row_to_dict(cursor)
    conn.close()
    return data

def get_sale_by_id(id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sales WHERE order_id = ?', (id,))
    data = row_to_dict(cursor)
    conn.close()
    return data

@app.get('/sales')
def list_sales():
    sales = get_sales()
    return sales

@app.get('/sales/{order_id}')
def list_get_sales(order_id: int):
    data = get_sale_by_id(order_id)
    return data

