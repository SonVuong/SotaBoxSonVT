import requests
from sqlalchemy import create_engine, text
import pandas as pd
import logging

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
            drop_statement = text("DROP TABLE IF EXISTS insurance_data")
            create_statement = text("""
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
            """)
            conn.execute(drop_statement)
            conn.execute(create_statement)
            logging.info("insurance_data table created successfully!")
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

# Create database engine
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/postgres')

# Create insurance_data table
create_insurance_data_table(engine)

# Insert data into insurance_data table
insert_insurance_data_table(engine, local_file_name)
