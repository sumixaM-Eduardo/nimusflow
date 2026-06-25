from pipeline.pipeline import extract
from pipeline.transform import clean_data, validate_data, convert_data
from pipeline.database import create_table, insert_data
import logging

logging.basicConfig(filename='logs/pipeline.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        logging.info('Pipeline started')
        sales = extract()
        clean_sales = clean_data(sales)
        valid_data, invalid_data = convert_data(clean_sales)
        approved_data, rejected_data = validate_data(valid_data, invalid_data)
        create_table()
        insert_data(approved_data, rejected_data)
        logging.info('Pipeline finished')
    except Exception as e:
        logging.info(f'Pipeline failed: {e}')
        raise


if __name__ == '__main__':
    main()
