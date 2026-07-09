# NimusFlow

NimusFlow is a personal project developed by **Maximus Eduardo**, a second-semester Information Systems student at the **Federal University of Alagoas (UFAL)**.

The project is part of my Data Engineering learning journey, with the goal of building a configurable ETL pipeline capable of validating, transforming, and loading structured data based on a user-defined schema. The pipeline is designed to be reusable across different datasets without requiring changes to the application code.

The project is still under active development and is continuously evolving as I learn new technologies and software engineering best practices.

## Project Goals

Learn ETL (Extract, Transform, Load) concepts

Build a reusable and configurable data pipeline

Practice Python for Data Engineering

Work with SQL databases

Develop REST APIs using FastAPI

Learn Docker, testing, and software architecture

## Current Features

Schema-driven data validation

Automatic data type conversion

Separation of valid and rejected records

Dynamic database generation

SQLite database integration

REST API for data access

Basic pipeline statistics

## Technologies Used

Python

FastAPI

SQLite

Docker

Git

GitHub

Pytest

## Project Structure

```text
NimusFlow/
├── .github/
│   └── workflows/
├── config/
│   └── schema.json
├── data/
│   ├── raw/
│   │   └── sales_sample.csv
│   └── sales.db
├── logs/
│   └── pipeline.log
├── pipeline/
│   ├── database.py
│   ├── pipeline.py
│   ├── schema_loader.py
│   └── transform.py
├── tests/
│   └── test_pipeline.py
├── .env
├── .gitignore
├── api.py
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```

## Roadmap

Support additional validation rules

Improve error handling

Add structured logging

PostgreSQL integration

Improve test coverage

## Learning Purpose

This project is part of my journey to become a Data Engineer. My objective is to understand how real-world data pipelines are designed and implemented by combining software engineering principles with data processing, databases, APIs, testing, and automation.

The project is intentionally being developed incrementally, focusing on solving real problems before introducing additional technologies.

Feedback, suggestions, and contributions are always welcome.
