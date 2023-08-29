# wpi_data_migration_pipeline_project

Access Database to PostgreSQL Migration E-L Python Pipeline
This repository contains a Python script to perform an Extract-Load (EL) migration from an Access database to a 
PostgreSQL database. The script extracts data from an Access database, transforms it if needed, and loads it into 
a PostgreSQL database. This README provides an overview of the implementation and guidelines for using the script.

-Requirements
Python 3.x
Required Python libraries: pyodbc (for Access DB), psycopg2 (for PostgreSQL DB)
    
-Installation
Install the required Python libraries using pip:
pip install pyodbc psycopg2 pandas

import pyodbc  # for Access db connection
import psycopg2 # for Postgresql db connection
import logging # for logging errors during migration
from sqlalchemy import create_engine # a unified interface for interacting with different databases
import pandas as pd # for converting the dataset to a dataframe

-Configuration
Access Database Connection:

Modify the access_connection_string in the script to match your Access database connection parameters. Update the 
database path and other relevant details.

-PostgreSQL Connection:

Update the pg_connection_params dictionary with your PostgreSQL database connection parameters, including host, port, database name, username, and password.

-Queries:

Adjust the Access and PostgreSQL queries (access_query and pg_insert_query) to fit your source and target table structures.

-Usage
Run the Script:

Open a terminal and navigate to the directory containing the script. Run the script using the following bash command:
    
python access_to_postgres_migration.py

-Monitoring Progress:

The script will display progress messages in the terminal as it extracts and loads data. Keep an eye out for any error 

messages that might occur.

-Completion:

Once the script completes, it will display a message indicating the ETL process is finished.

-Customization
Feel free to customize the script further to suit your specific requirements. You can add error handling, logging, data 
transformation, and other features to make the ETL process more robust.

-Troubleshooting
If you encounter issues with the Access database connection, verify the connection string, ODBC driver installation, 
and relevant environment settings.
If PostgreSQL connection issues arise, ensure your PostgreSQL server is running and accessible, and the connection 
parameters are correctly specified.

-Disclaimer
This script is provided as-is and should be thoroughly tested in a non-production environment before being used for a 
real migration. It's recommended to create backups of your data before attempting any migration.

Credits
This script was created by Andy Olisaemeka a.k.a Emmeker007 and can be reached at emmeker@gmail.com.
