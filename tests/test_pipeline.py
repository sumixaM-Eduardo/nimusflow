from pipeline.transform import clean_data, validate_data, convert_data
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_clean_data():
    sale = {
        'order_id': '1  ',
        'customer_id': '100  ',
        'product_name': 'Notebook  ',
        'quantity': '2  ',
        'unit_price': '1500.00  ',
        'sale_date': '2026-01-15  ',
        'payment_method': 'PIX  ',
        'city': 'Maceió  '
    }
    result = clean_data([sale])
    assert result[0]['order_id'] == '1'
    assert result[0]['product_name'] == 'Notebook'

def test_validate_data():
    valid_sale = {
        'order_id': 1,
        'customer_id': 100,
        'product_name': 'Notebook',
        'quantity': 2,
        'unit_price': 1500.00,
        'sale_date': '2026-01-15',
        'payment_method': 'PIX',
        'city': 'Maceió'
    }
    invalid_sale = {
        'order_id': -1,
        'customer_id': -100,
        'product_name': 'Notebook',
        'quantity': 2,
        'unit_price': 1500.00,
        'sale_date': '2026-01-15',
        'payment_method': 'PIX',
        'city': 'Maceió'
    }
    approved_sales, rejected_sales = validate_data([valid_sale], [invalid_sale])
    assert len(approved_sales) == 1
    assert len(rejected_sales) == 1

def test_convert_data():
    sale = {
        'order_id': '1',
        'customer_id': '100',
        'product_name': 'Notebook',
        'quantity': '2',
        'unit_price': '1500.00',
        'sale_date': '2026-01-15',
        'payment_method': 'PIX',
        'city': 'Maceió'
    }
    aproved_sales, rejected_sales = convert_data([sale])
    assert len(aproved_sales) == 1
    assert len(rejected_sales) == 0

def test_get_sales():
    response = client.get('/sales')
    assert response.status_code == 200

def test_get_sales_by_id():
    response = client.get('/sales/1')
    assert response.status_code == 200

def test_get_summary():
    response = client.get('/summary')
    assert response.status_code == 200

def test_get_rejected():
    response = client.get('/rejected')
    assert response.status_code == 200