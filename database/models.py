#1. here I import base from db.py and column types from sqlalchemy
from database.db import Base
from sqlalchemy import Column, Integer, String, Text, DateTime


#2. here I will define the RiskEntry class whih will inherit from the base class after i import it
class RiskEntry(Base):

#3. here i will set the table name
    __tablename__ = "risk_entries"
#4. here I will be defining all the 6 columns that I have planned in the project blueprint
    id = Column(Integer, primary_key=True, autoincrement = True)
    risk_input = Column(Text)
    strategy = Column(String(50))
    ai_response = Column(Text)
    rating = Column(String(50))
    created_at = Column(DateTime) 