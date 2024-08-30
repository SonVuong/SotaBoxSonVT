import requests
from sqlalchemy import create_engine, text, insert
import pandas as pd

def download_object_from_fake_gcs(bucket_name, object_name, local_file_name):
    # URL to access the fake GCS server
    url = f"https://localhost:4443/storage/v1/b/{bucket_name}/o/{object_name}?alt=media"
    
    try:
        # Make a GET request to the fake GCS server to download the object
        response = requests.get(url, verify=False)  # verify=False to ignore SSL errors
        
        # Check if the request was successful
        if response.status_code == 200:
            # Write the content to a local file
            with open(local_file_name, 'wb+') as f:
                f.write(response.content)
            print(f"Successfully downloaded {object_name} from bucket {bucket_name} to {local_file_name}")
        else:
            print(f"Failed to download object. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage
bucket_name = 'sample-bucket'  # Replace with your bucket name
object_name = 'insurance_claims.csv'  # Replace with your object name
local_file_name = '../local_data/insurance_claims.csv'  # Replace with your desired local file name

download_object_from_fake_gcs(bucket_name, object_name, local_file_name)

engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/postgres')

def create_insurance_data_table():
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
        print("insurance_table created successfully!")

def insert_insurance_data_table():
    df = pd.read_csv(local_file_name)

    df.columns = [col.lower() for col in df.columns]
    df['idpol'] = df['idpol'].fillna(0).astype(int)
    df['density'] = df['density'].astype(int)

    df.to_sql('insurance_data', engine, if_exists='append', index=False)

    print("Data loaded successfully!")

create_insurance_data_table()
insert_insurance_data_table()