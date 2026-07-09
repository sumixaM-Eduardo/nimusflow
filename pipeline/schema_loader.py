import json
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent.parent / 'config' / 'schema.json'

def load_schema():
    with open (SCHEMA_PATH, 'r', encoding='utf-8') as json_data:
        return json.load(json_data)