from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:@localhost/clinica"

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)