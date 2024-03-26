import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
DB_LOGIN = os.environ.get('recipeBot_postgres_login')
DB_PASS = os.environ.get('recipeBot_postgres_pass')
DB_LOCATION = os.environ.get('db_location')

engine = create_engine(f"postgresql+psycopg2://{DB_LOGIN}:{DB_PASS}{DB_LOCATION}", echo=True)
Base = declarative_base()
