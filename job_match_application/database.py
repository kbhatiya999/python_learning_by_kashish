import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
from job_match_application.config import get_db

mysql_db = get_db()
SQLALCHEMY_DATABASE_URL = sqlalchemy.engine.url.URL.create(drivername='mysql', username=mysql_db['user'],
                              password=mysql_db['pass'], database=mysql_db['db'],
                              host=mysql_db['host'], port=mysql_db['port'])

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()