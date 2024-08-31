import requests
from sqlalchemy import create_engine, text
import pandas as pd
import logging
import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 

# Configure logging
logging.basicConfig(
    filename='../logging/insurance_data_processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def download_object_from_fake_gcs(bucket_name, object_name, local_file_name):
    """Download an object from a fake GCS server and save it locally."""
    url = f"https://localhost:4443/storage/v1/b/{bucket_name}/o/{object_name}?alt=media"
    
    try:
        # Make a GET request to the fake GCS server to download the object
        response = requests.get(url, verify=False)  # verify=False to ignore SSL errors

        # Check if the request was successful
        if response.status_code == 200:
            with open(local_file_name, 'wb+') as f:
                f.write(response.content)
            logging.info(f"Successfully downloaded {object_name} from bucket {bucket_name} to {local_file_name}")
        else:
            logging.error(f"Failed to download object. Status code: {response.status_code}. Response: {response.text}")
    
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while downloading from GCS: {e}")

def create_insurance_data_table(engine):
    """Create the insurance_data table in the PostgreSQL database."""
    try:
        with engine.connect() as conn:
            with conn.begin():  # Use a transaction to ensure atomicity
                # Define SQL statements
                sql_statements = """
                    DROP TABLE IF EXISTS insurance_data;

                    CREATE TABLE IF NOT EXISTS insurance_data (
                        IDpol INT,
                        ClaimNb INT,
                        Exposure DECIMAL(5, 2),
                        VehPower INT,
                        VehAge INT,
                        DrivAge INT,
                        BonusMalus INT,
                        VehBrand VARCHAR(10),
                        VehGas VARCHAR(10),
                        Area VARCHAR(5),
                        Density INT,
                        Region VARCHAR(50),
                        ClaimAmount INT
                    );

                    GRANT INSERT, UPDATE ON TABLE insurance_data TO writeonly_user;
                    GRANT SELECT ON TABLE insurance_data TO readonly_user;
                    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE insurance_data TO readwrite_user;
                """
                # Execute the SQL statements
                conn.execute(text(sql_statements))
                
            logging.info("insurance_data table created and permissions set successfully!")
    except Exception as e:
        logging.error(f"An error occurred while creating the insurance_data table: {e}")
        
def insert_insurance_data_table(engine, local_file_name):
    """Insert data from a CSV file into the insurance_data table."""
    try:
        df = pd.read_csv(local_file_name)
        # Clean up and prepare DataFrame
        df.columns = [col.lower() for col in df.columns]
        df['idpol'] = df['idpol'].fillna(0).astype(int)
        df['density'] = df['density'].astype(int)

        # Insert data into PostgreSQL
        df.to_sql('insurance_data', engine, if_exists='append', index=False)
        logging.info("Data loaded into insurance_data table successfully!")
    except FileNotFoundError:
        logging.error(f"CSV file not found: {local_file_name}")
    except pd.errors.EmptyDataError:
        logging.error("CSV file is empty.")
    except pd.errors.ParserError:
        logging.error("Error parsing CSV file.")
    except Exception as e:
        logging.error(f"An error occurred while loading data into insurance_data table: {e}")

# Example usage
bucket_name = 'sample-bucket'  # Replace with your bucket name
object_name = 'insurance_claims.csv'  # Replace with your object name
local_file_name = '../local_data/insurance_claims.csv'  # Replace with your desired local file name

# Download file from fake GCS
download_object_from_fake_gcs(bucket_name, object_name, local_file_name)

db_username_table_manager = os.getenv('table_manager_username')
db_password_table_manager = os.getenv('table_manager_password')

db_username_write_only = os.getenv('write_only_username')
db_password_write_only = os.getenv('write_only_password')

db_host = os.getenv('db_host')
db_port = os.getenv('db_port')
db_name = os.getenv('db_name')
# Create database engine
engine_table_manager = create_engine(f'postgresql+psycopg2://{db_username_table_manager}:{db_password_table_manager}@{db_host}:{db_port}/{db_name}')
engine_write_only = create_engine(f'postgresql+psycopg2://{db_username_write_only}:{db_password_write_only}@{db_host}:{db_port}/{db_name}')

# Create insurance_data table
create_insurance_data_table(engine_table_manager)

# Insert data into insurance_data table
insert_insurance_data_table(engine_write_only, local_file_name)
