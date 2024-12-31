from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


USE_DB = "postgres"

# this is a base class that will be inherited by models
# this has all the functionality of ORM
# use this in models
Base = declarative_base()

if USE_DB == "sqllite":
    SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

    engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



if USE_DB == "postgres":

    ## postgres connectivity
    POSTGRES_URL  = "postgresql://postgres:postgres123#$@localhost:5432/TodoApplication"

    # Create the database engine
    engine = create_engine(POSTGRES_URL)

    # Create the sessionmaker to manage sessions
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


