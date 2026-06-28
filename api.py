from fastapi import FastAPI
import sqlite3

app = FastAPI()

def get_sales():
    conn = sqlite3.connect('data/sales.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales")
    columns = [coll[0] for coll in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return data

@app.get('/sales')
def list_sales():
    sales = get_sales()
    return sales



