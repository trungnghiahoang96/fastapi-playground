import os

from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

print('Database URL:', os.environ['DATABASE_URL'])


load_dotenv()

engine = create_engine(os.environ['DATABASE_URL'])
Session = sessionmaker(engine)