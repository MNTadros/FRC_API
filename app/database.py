from databases import Database
from sqlalchemy import MetaData, create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tmp/frc_components.db")

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
