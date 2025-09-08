# scripts/setup_db.py
import pandas as pd
from src.db import sqlite_engine

def main():
    engine, db_path = sqlite_engine()

    # Datos de ejemplo
    employees = pd.DataFrame([
        {"id": 1, "name": "Ana",    "age": 29, "department_id": 1, "salary": 1200},
        {"id": 2, "name": "Carlos", "age": 35, "department_id": 2, "salary": 1500},
        {"id": 3, "name": "María",  "age": 41, "department_id": 3, "salary": 1800},
        {"id": 4, "name": "Pedro",  "age": 30, "department_id": 1, "salary": 1300},
        {"id": 5, "name": "Eva",    "age": 26, "department_id": 2, "salary": 1100},
    ])

    departments = pd.DataFrame([
        {"id": 1, "name": "IT"},
        {"id": 2, "name": "Finance"},
        {"id": 3, "name": "HR"},
    ])

    # Volcar a SQLite
    employees.to_sql("employees", con=engine, if_exists="replace", index=False)
    departments.to_sql("departments", con=engine, if_exists="replace", index=False)

    print(f"✅ SQLite created at: {db_path}")
    print("✅ Tables: employees, departments")

if __name__ == "__main__":
    main()