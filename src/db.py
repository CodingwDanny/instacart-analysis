# src/db.py
from pathlib import Path
from sqlalchemy import create_engine

def sqlite_engine(db_name: str = "company.db"):
    """
    Crea un engine de SQLAlchemy apuntando a data/<db_name>.
    Crea la carpeta data/ si no existe y devuelve (engine, db_path).
    """
    project_root = Path(__file__).resolve().parents[1]
    db_path = project_root / "data" / db_name
    db_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}")
    return engine, db_path