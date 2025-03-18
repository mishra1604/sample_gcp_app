import pandas as pd
from sqlalchemy import create_engine

# Database connection details
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "your_host"
DB_PORT = "your_port"
DB_NAME = "your_database"
TABLE_NAME = "your_table"

# Create database connection
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Load new data from Excel
new_data = pd.read_excel("new_data.xlsx")

# Load existing data from PostgreSQL
existing_data = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", engine)

# Ensure column names match
new_data.columns = new_data.columns.str.lower()
existing_data.columns = existing_data.columns.str.lower()

# Identify new records
new_records = new_data[~new_data['id'].isin(existing_data['id'])]

# Identify updated records
updated_records = new_data[new_data['id'].isin(existing_data['id'])]

# Insert new records into database
if not new_records.empty:
    new_records.to_sql(TABLE_NAME, engine, if_exists='append', index=False)

# Update existing records
if not updated_records.empty:
    for index, row in updated_records.iterrows():
        update_query = f"""
        UPDATE {TABLE_NAME} 
        SET column1 = '{row['column1']}', column2 = '{row['column2']}' 
        WHERE id = {row['id']}
        """
        with engine.begin() as conn:
            conn.execute(update_query)

print("Database updated successfully!")
