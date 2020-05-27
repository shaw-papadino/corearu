import os
from sqlalchemy import *
from sqlalchemy.orm import *

# from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# 本番はpostgre
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False}
        )
SessionLocal = scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = engine))
Base = declarative_base()
