from datetime import datetime

def clean_data(sales):
    for sale in sales:
        sale['order_id'] = sale['order_id'].strip()
        sale['customer_id'] = sale['customer_id'].strip()
        sale['product_name'] = sale['product_name'].strip()
        sale['quantity'] = sale['quantity'].strip()
        sale['unit_price'] = sale['unit_price'].strip()
        sale['sale_date'] = sale['sale_date'].strip()
        sale['payment_method'] = sale['payment_method'].strip()
        sale['city'] = sale['city'].strip()
    return sales

def convert_data(sales):
    valid_sales = []
    invalid_sales = []
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
    return valid_sales, invalid_sales

def validate_data(valid_sales, invalid_sales):
    approved_sales = []
    rejected_sales = []
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
    return approved_sales, rejected_sales

