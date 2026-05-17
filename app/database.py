from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Projektbasis ermitteln:
# app/database.py liegt im Ordner app/
# parent.parent geht zurück auf den Projektordner complaint-management-cockpit/
BASE_DIR = Path(__file__).resolve().parent.parent

# Datenbankordner und Datenbankdatei
DATA_DIR = BASE_DIR / "data"
DATABASE_FILE = DATA_DIR / "complaints.db"

# Sicherstellen, dass der data-Ordner existiert
DATA_DIR.mkdir(exist_ok=True)

# SQLite-Datenbank-URL
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)

# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Basisklasse für alle Datenbankmodelle
Base = declarative_base()


def get_db_session():
    """
    Erstellt eine neue Datenbanksitzung.
    Diese Funktion wird später von Services genutzt.
    """
    return SessionLocal()


def create_tables():
    """
    Erstellt alle Tabellen in der SQLite-Datenbank.
    Die konkreten Tabellen kommen aus models.py.
    """
    Base.metadata.create_all(bind=engine)