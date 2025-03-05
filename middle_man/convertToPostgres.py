import pandas as pd
import openpyxl
from sqlalchemy import create_engine, text, inspect
import env_variables

default_database_name = 'postgres'
# database = f'postgresql://myuser:mypassword@localhost:5432/'
database = f'postgresql://{env_variables.gcp_postgres_username}:{env_variables.gcp_postgres_password}/@34.76.117.61:5432/'
database_url = database + default_database_name
engine = create_engine(database_url)
new_db_name = "converted_db"

with engine.connect() as connection_1:
    connection_1.connection.set_session(autocommit=True)
    connection_1.execute(text(f'DROP DATABASE IF EXISTS "{new_db_name}"'))
    connection_1.execute(text(f"""CREATE DATABASE {new_db_name}"""))
    connection_1.connection.set_session(autocommit=False)

new_url = database + new_db_name
new_engine = create_engine(new_url)
connection_2 = new_engine.connect()

workbook = openpyxl.load_workbook('decentralized_employee_data.xlsx')

sheet_list = workbook.sheetnames
print("Sheets present: ", sheet_list)

excel_df = pd.read_excel("decentralized_employee_data.xlsx", sheet_name=sheet_list)

for table in excel_df:
    table_data = excel_df[table]
    table_data.to_sql(table.lower(), con=new_engine, index=False)

result = connection_2.execute(text("""SELECT * FROM employees"""))
for i, row in enumerate(result):
    print(row)

try:
    inspector = inspect(new_engine)
    print(f"Available tables in {new_db_name}: ", inspector.get_table_names(schema='public'))
except Exception as e:
    print("Failed to convert excel to database")
    print(f"Unexpected Error: {e}")