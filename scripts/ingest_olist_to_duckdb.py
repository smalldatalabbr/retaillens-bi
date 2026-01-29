"""
Ingestão do dataset OLIST:
CSV (zipado) → DuckDB (camada bronze)

- Fonte: data/raw/olist.zip
- Destino: data/processed/olist.duckdb
"""

from pathlib import Path
from zipfile import ZipFile
import shutil
import duckdb

from src.paths import RAW_DATA, RAW_FOLDER, PROCESSED_DATA

def main():
    RAW_FOLDER.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA.parent.mkdir(parents=True, exist_ok=True)

    tmp_extract = RAW_FOLDER / "_tmp_extract"

    # garante pasta temporária limpa
    if tmp_extract.exists():
        shutil.rmtree(tmp_extract)
    tmp_extract.mkdir(parents=True, exist_ok=True)

    try:
        # extrai CSVs temporariamente
        with ZipFile(RAW_DATA, "r") as zf:
            zf.extractall(tmp_extract)

        con = duckdb.connect(str(PROCESSED_DATA))

        csv_paths = sorted(tmp_extract.rglob("*.csv"))

        for p in csv_paths:
            table = p.stem.lower().replace("-", "_")
            con.execute(f"DROP TABLE IF EXISTS {table}")
            con.execute(
                f"""
                CREATE TABLE {table} AS
                SELECT * FROM read_csv_auto('{p.as_posix()}', SAMPLE_SIZE=-1);
                """
            )
            print("ok:", table)

        con.close()
        print("✔ DuckDB criado em:", PROCESSED_DATA)

    finally:
        # apaga CSVs extraídos (sempre)
        if tmp_extract.exists():
            shutil.rmtree(tmp_extract)

if __name__ == "__main__":
    main()

