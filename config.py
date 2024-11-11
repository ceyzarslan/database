from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite için bağlantı cümlesi:

CONNECTION_STRING = "sqlite:///data.db"

engine = create_engine(CONNECTION_STRING, echo=True)
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()
