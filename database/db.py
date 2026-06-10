import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

#1. this will load the environment variables from the .env file
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

#2. here the mysql connection is built from .env file
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#3. creating sqlalchemy engine here
engine = create_engine(DATABASE_URL)

#4. creating a session
SessionLocal = sessionmaker(bind=engine)

#5. creating a base class for inheritance for models
Base = declarative_base()