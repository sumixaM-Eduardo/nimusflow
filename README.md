# NimusFlow

A simple data pipeline for sales data built with Python.

## About

This is a personal project I built to learn how data pipelines work in practice.
The pipeline reads a CSV file with sales data, processes it and loads the results into a SQLite database.

## Technologies

- Python 3.12
- SQLite
- CSV (built-in)
- Logging (built-in)

## How it Works

The pipeline follows these steps:

1. **Extraction** - reads the raw sales CSV file
2. **Cleaning** - removes extra spaces from the fields
3. **Conversion** - converts data types (string to int, float and datetime)
4. **Validation** - applies business rules to separate valid and invalid records
5. **Loading** - saves the results into a SQLite database

## Project Structure
NimusFlow/

├── data/

│   ├── raw/          # raw CSV files

│   └── sales.db      # SQLite database

├── logs/             # pipeline logs

├── pipeline/

│   ├── pipeline.py   # extraction

│   ├── transform.py  # cleaning, conversion and validation

│   └── database.py   # database connection and loading

└── main.py           # entry point

## How to Run

1. Clone the repository
2. Create a virtual environment
`bash python -m venv .venv source .venv/bin/activate`
3. Run the pipeline
`bash python main.py`

## Next Steps

- [ ] Add scheduling
- [ ] Build a REST API with FastAPI
- [ ] Add Docker support
- [ ] Deploy to cloud
- [ ] Add Apache Airflow for orchestration
