# scripts/load_instacart.py
import pandas as pd
from pathlib import Path
from src.db import sqlite_engine

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "instacart"

FILES = {
    "aisles": "aisles.csv",                       # 134 filas
    "departments": "departments.csv",             # 21 filas aprox
    "orders": "orders.csv",                       # ~3.4M filas
    "products": "products.csv",                   # ~50k filas
    "order_products_prior": "order_products__prior.csv",  # ~32M filas (en el comp grande)
    "order_products_train": "order_products__train.csv",  # ~1.4M filas
}

# Algunas columnas de fecha/hora en orders
DATE_COLS = {
    "orders": ["order_hour_of_day"],    # (numérico), lo dejamos como está
}

def load_csv(name, filename):
    path = RAW / filename
    # Para datasets grandes evitamos que infiera tipos inconsistentes
    df = pd.read_csv(path, low_memory=False)
    # Si hubiera columnas listadas para parseo, acá las trataríamos
    for col in DATE_COLS.get(name, []):
        if col in df.columns:
            # ejemplo: si viniera string, podríamos convertir
            pass
    return df

def main():
    engine, db_path = sqlite_engine("instacart.db")

    # Tablas pequeñas primero (dimensiones)
    for table in ["aisles", "departments", "products"]:
        df = load_csv(table, FILES[table])
        df.to_sql(table, con=engine, if_exists="replace", index=False)
        print(f"Loaded {table}: {len(df):,} rows")

    # Orders (medio)
    df = load_csv("orders", FILES["orders"])
    df.to_sql("orders", con=engine, if_exists="replace", index=False)
    print(f"Loaded orders: {len(df):,} rows")

    # Tablas de líneas (grandes): prior + train
    # Si tu RAM es limitada, usa chunks (descomenta el bloque CHUNKS más abajo)
    for table in ["order_products_prior", "order_products_train"]:
        csv_path = RAW / FILES[table]
        print(f"Loading {table} in chunks...")
        chunksize = 1_000_000
        inserted = 0
        for chunk in pd.read_csv(csv_path, chunksize=chunksize):
            chunk.to_sql(table, con=engine, if_exists="append", index=False)
            inserted += len(chunk)
            print(f"  inserted {inserted:,} rows...", end="\r")
        print(f"\nLoaded {table}: {inserted:,} rows")

    print(f"✅ Instacart loaded into: {db_path}")

if __name__ == "__main__":
    main()