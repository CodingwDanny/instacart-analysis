# scripts/run_queries.py
import pandas as pd
from src.db import sqlite_engine

def main():
    engine, _ = sqlite_engine()

    print("\n== Employees ==")
    print(pd.read_sql("SELECT * FROM employees;", engine))

    print("\n== Salaries >= 1300 ==")
    q_filter = "SELECT id, name, salary FROM employees WHERE salary >= 1300 ORDER BY salary DESC;"
    print(pd.read_sql(q_filter, engine))

    print("\n== Join with departments ==")
    q_join = """
    SELECT e.id, e.name, d.name AS department, e.salary
    FROM employees e
    JOIN departments d ON d.id = e.department_id
    ORDER BY e.salary DESC;
    """
    print(pd.read_sql(q_join, engine))

    print("\n== Avg salary by department ==")
    q_group = """
    SELECT d.name AS department, AVG(e.salary) AS avg_salary, COUNT(*) AS headcount
    FROM employees e
    JOIN departments d ON d.id = e.department_id
    GROUP BY d.name
    ORDER BY avg_salary DESC;
    """
    print(pd.read_sql(q_group, engine))

if __name__ == "__main__":
    main()