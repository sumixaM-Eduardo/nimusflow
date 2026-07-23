# NimusFlow

A production-style ETL pipeline and REST API for processing sales data, built with a **schema-driven architecture** — every layer (data cleaning, validation, database schema, and API model) is generated dynamically from a single configuration file, not hardcoded to a specific dataset.

## Features

- **ETL pipeline**: extract → clean → convert → validate → load, with structured logging and error handling
- **Schema-driven design**: a single `config/schema.json` defines every field, type, and validation rule. Changing the dataset's structure requires no code changes — table creation, data validation, type conversion, and the API's request model all adapt automatically
- **REST API** built with FastAPI, exposing CRUD operations over the processed data
- **PostgreSQL** as the persistence layer, with duplicate-insertion protection via primary key constraints
- **Automated testing** with pytest (unit and integration tests against the live API)
- **CI/CD** via GitHub Actions, running the full test suite against an ephemeral PostgreSQL service container on every push
- **Containerized** with Docker and Docker Compose, orchestrating the API and database together with a single command

## Architecture

```
CSV (raw data)
      │
      ▼
┌─────────────┐     ┌─────────────────────┐
│  pipeline/  │────▶│ config/schema.json  │  (single source of truth)
│ transform.py│     └─────────────────────┘
│ database.py │              │
└─────────────┘              │
      │                      │
      ▼                      ▼
 PostgreSQL  ◀────────  api.py (FastAPI)
```

Every component reads field names, types, and validation rules from `schema.json` at runtime:

- `pipeline/transform.py` — cleans, type-converts, and validates records based on each field's declared type and rules (`required`, `min`)
- `pipeline/database.py` — generates `CREATE TABLE` and `INSERT` statements dynamically, mapping schema types to PostgreSQL types
- `api.py` — builds the Pydantic request model at runtime using `pydantic.create_model`, and all queries reference the table name from the schema

## Project structure

```
NimusFlow/
├── api.py                    # FastAPI application
├── main.py                   # Pipeline entrypoint
├── config/
│   └── schema.json           # Single source of truth for fields, types, and rules
├── pipeline/
│   ├── schema_loader.py      # Loads and parses schema.json
│   ├── transform.py          # clean / convert / validate
│   ├── database.py           # Table creation and data loading
│   └── pipeline.py           # Orchestrates the ETL steps
├── tests/
│   └── test_pipeline.py      # Unit and integration tests
├── data/
│   └── raw/                  # Input CSV files
├── Dockerfile
├── docker-compose.yml        # Orchestrates API + PostgreSQL
├── .env.example               # Template for required environment variables
└── .github/workflows/
    └── pipeline.yml           # CI: tests run against a PostgreSQL service container
```

## Getting started

### Option 1: Docker Compose (recommended)

```bash
cp .env.example .env
# edit .env with your desired credentials
docker-compose up --build
```

This starts PostgreSQL and the API together. The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

To create the tables and load data inside the running container:

```bash
docker-compose exec api python -c "from pipeline.database import create_table; create_table()"
docker-compose exec api python main.py
```

### Option 2: Local setup

Requires Python 3.12+ and a running PostgreSQL instance.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with your local PostgreSQL credentials
python main.py            # runs the ETL pipeline
uvicorn api:app --reload  # starts the API
```

## Configuration

Environment variables (see `.env.example`):

| Variable | Description |
|---|---|
| `RAW_CSV_PATH` | Path to the input CSV file |
| `DB_HOST` | PostgreSQL host |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `DB_PORT` | Database port |

## Customizing the schema

To adapt the pipeline to a different dataset, edit `config/schema.json`:

```json
{
  "table_name": "sales",
  "fields": [
    {"name": "order_id", "type": "int", "required": true, "min": 1, "primary_key": true},
    {"name": "unit_price", "type": "float", "required": true, "min": 0.01},
    {"name": "sale_date", "type": "date", "required": true, "format": "%Y-%m-%d"},
    {"name": "city", "type": "string", "required": true}
  ]
}
```

Supported types: `int`, `float`, `string`, `date`. No changes to `transform.py`, `database.py`, or `api.py` are needed.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/sales` | List all sales |
| GET | `/sales/{order_id}` | Get a sale by ID |
| GET | `/sales/city/{city}` | Filter sales by city |
| GET | `/sales/payment_method/{payment_method}` | Filter sales by payment method |
| GET | `/rejected` | List records rejected during validation |
| GET | `/summary` | Aggregate summary (total records, total revenue) |
| POST | `/sales` | Create a new sale |
| DELETE | `/sales/{order_id}` | Delete a sale |

## Running tests

```bash
python -m pytest -v
```

Tests cover both the pipeline's transformation functions and the API endpoints (via FastAPI's `TestClient`), exercising the full stack against a real PostgreSQL database.

## CI/CD

Every push triggers a GitHub Actions workflow that spins up a temporary PostgreSQL service container, creates the schema, and runs the full test suite — validating the project end-to-end without any manual setup.
