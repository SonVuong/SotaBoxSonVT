# SotaBoxSonVT
This is the documentation for Data Engineering Test: Google Cloud Storage to PostgreSQL

# Requirements

## Context
The assumption is a CSV file containing insurance claim data is stored in Google Cloud Storage. Your task is to extract this data, load it into PostgreSQL, perform some analyses, and store the results in PostgreSQL tables.

## Input Data
The CSV file in Google Cloud Storage contains the following columns: The CSV file in Google Cloud Storage contains the following columns: The CSV file in Google Cloud Storage contains the following columns: IDpol, ClaimNb, Exposure, VehPower, VehAge, DrivAge, BonusMalus, VehBrand, VehGas, Area, Density, Region, ClaimAmount

## Deliverables
1. The script for extracting data from GCS and loading it into PostgreSQL.
2. SQL queries for tasks 2 and 3, including table creation statements. (Sum of Exposure by VehBrand and Area and Min and Max Density by Area).
3. SQL commands for indexing and access control.
4. A brief explanation of your approach, including error handling, performance optimization, and security considerations.

# Approach and Solution
1. Approach
- Data Extraction and Loading
  - Source data is stored in GCS. However i don't have an existing GCP account so i use a local GCS server. Here's the link to the original https://github.com/fsouza/fake-gcs-server.
  - Create PostgreSQL table and grant permissions using SQLAlchemy and SQL commands.
  - Use pandas to load the data into dataframe and insert into the database.
- Indexing and Access Controls
  - Create multiple indexes on the columns in task 2 and 3. 
  - Create read-only, write-only, read-write-only and table-manager roles to ensure the least privlege provided for each necessary steps.

2. Deployment
- Docker is being used to deploy fake-gcs-server, PostgreSQL, PgAdmin. There's a docker-compose.yml file.
- Credentials are stored in .env file. All necessary python libraries listed in requirements.txt file.
- Data extraction and loading step is being handled by SQLAlchemy, Pandas.
- To interact with fake-gcs-server, i use JSON API similar to normal GCS.
- To perform the SQL queries in task 2, 3, create roles, create indexes, i use PgAdmin UI to run the queries. The SQL scripts are in /SQL folder.

3. Setup environment
- Start the fake-gcs-server and PostgreSQL with docker-compose up command.
- Logging will be stored in /logging folder.
- Data for the GCS bucket will be stored in /data/sample-bucket folder. To change the bucket name you can change the folder sample-bucket to another name.

## Considerations for each steps.
1. Data Extraction and Loading
- Error Handling: Implement error handling for network issues, authentication errors, and invalid file paths. Use retries with exponential backoff to handle transient errors. 
- Logging: Log all steps, including successful downloads and any errors, to aid in debugging and monitoring.
- Use Environment Variables: Store sensitive information, such as PostgreSQL credentials instead of hard-coding it to the script.
- Pandas for Data Loading: Use Pandas’ to_sql() method with chunksize to efficiently load large datasets in batches, reducing memory usage.
- Data Validation: Validate the data types and check for nulls or inconsistencies before loading to prevent data integrity issues.

2. SQL Query Efficiency and Accuracy
- Indexing: Create indexes on columns used in joins, filters, and aggregations to speed up query execution.
- Analyze and Optimize: Use PostgreSQL's EXPLAIN ANALYZE to understand query performance and optimize accordingly.
- **Avoid SELECT ***: Specify only the columns you need to reduce data transfer and improve performance.
- Access Control: Grant minimal necessary privileges to database users and roles. Use separate roles for reading and writing data.
- Transaction: Wrapping SQL commands in transactions block to ensure integrity and consistency of the database.

# Next possible steps
- Develop fully into a ETL/ELT pipeline. Use Airflow to orchestrate, schedule the data processing process. The pipeline can also integrate steps to load into data lake or data warehouse if necessary.
- Data quality checks and validations. Implement auto data quality checks after each pipeline runs using Great Expectations data quality library.
- Reporting and visualizations. Connect the PostgreSQL database or data warehouse to reporting tools like Tableau or PowerBI for visualization and reporting.