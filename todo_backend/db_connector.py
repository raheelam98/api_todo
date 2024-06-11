from sqlmodel import SQLModel, create_engine, Session
from todo_backend import setting
from sqlmodel.pool import StaticPool

# connecting with database url
connection_string = str(setting.database_url).replace("postgresql", "postgresql+psycopg2")

# create engine
engine = create_engine(connection_string, connect_args={"sslmode":"require"}, pool_recycle=300, echo=True)
#  engine with echo=True, it will show the SQL it executes in the output

# create database and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# create session to get memory space in db
def get_session():
    with Session(engine) as session:
        yield session

# ===============  test databse =============== #

# connecting with database 
test_conn_string = str(setting.test_database_url).replace("postgresql", "postgresql+psycopg2")

# create engine
test_engine = create_engine(test_conn_string, connect_args={"sslmode":"require"}, pool_recycle=300, echo=True)

# create database and tables
def test_create_db_tables():
    SQLModel.metadata.create_all(test_engine)