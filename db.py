import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base

dotenv

load_dotenv()
DATABASE_URL = 
s.getenv("DATABASE_URL)
engine = 
create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, bind=engine)
