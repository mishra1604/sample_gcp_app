import os
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import pg8000.dbapi
from sqlalchemy import create_engine, text, inspect
from env_variables import gcp_postgres_username, gcp_postgres_password

gcp_database_url = f'postgresql://{gcp_postgres_username}:{gcp_postgres_password}/@34.76.117.61:5432/postgres'
local_database_url = 'postgresql://myuser:mypassword@localhost:5432/converted_db'
engine = create_engine(gcp_database_url)

# with engine.connect() as connection_1:
#     connection_1.connection.set_session(autocommit=True)
#     connection_1.execute(text(f'DROP DATABASE IF EXISTS "converted_db"'))
#     connection_1.connection.set_session(autocommit=False)

with engine.connect() as conn:
    result = conn.execute(text("""SELECT datname FROM pg_database WHERE datistemplate = false;"""))
    # result = conn.execute(text("""SELECT version();"""))
    for i, row in enumerate(result):
        print(row)