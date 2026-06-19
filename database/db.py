import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from urllib.parse import quote_plus

#1. this will load the environment variables from the .env file
load_dotenv()

#2. SQLite connection instead of MySQL
DATABASE_URL = "sqlite:///risks.db"

#3. creating sqlalchemy engine here
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

#4. creating a session
SessionLocal = sessionmaker(bind=engine)

#5. creating a base class for inheritance for models
Base = declarative_base()







#6. this is the function to save a risk entry in the database
def save_risk(risk_input, strategy, ai_response, rating):

    #a. importing the risk entry model
    from database.models import RiskEntry

    #b. creating a session
    session = SessionLocal()
    
    #c. creating a risk entry object with the data here
    new_risk = RiskEntry(risk_input=risk_input, strategy=strategy, ai_response=ai_response, rating = rating)
    
    #d. adding it to the session and commit 
    session.add(new_risk)
    session.commit()
    #e. closing the session
    session.close()


#7. Function to get all the risk entries from the database
def get_all_risks():
    #a. import the riskentry model
    from database.models import RiskEntry

    #b. creating a session
    session = SessionLocal()

    #c. Quering for all the risk entries
    risks = session.query(RiskEntry).all()

    #d. close the session
    session.close()

    #e. return the results
    return risks

# 8. Initialize database automatically for SQLite
from database.models import RiskEntry
Base.metadata.create_all(bind=engine)