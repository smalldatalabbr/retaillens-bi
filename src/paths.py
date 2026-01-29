from pathlib import Path

# Raiz do projeto
BASE_PATH = Path(__file__).resolve().parents[1]

DATA_FOLDER = BASE_PATH / "data"
RAW_FOLDER = DATA_FOLDER / "raw"
PROCESSED_FOLDER = DATA_FOLDER / "processed"

RAW_DATA = RAW_FOLDER / "olist.zip"
PROCESSED_DATA = PROCESSED_FOLDER / "olist.duckdb"
