#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Install the necessary packages

get_ipython().system('pip install pandas pyodbc psycopg2')

import pyodbc  # for Access db connection
import psycopg2 # for Postgresql db connection
import logging # for logging errors during migration
from sqlalchemy import create_engine # for 
import pandas as pd # for converting the dataset to a dataframe

[i for i in pyodbc.drivers() if i.startswith('Microsoft Access Driver')]

def get_accessbase_conn():
    return pyodbc.connect('Driver={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=C:/Users/emmek/Documents/WPI.mdb')
get_accessbase_conn()

conn = get_accessbase_conn()
cursor = conn.cursor()

# Get the List of table names

table_names = [table.table_name for table in cursor.tables (tableType="TABLE")]

# Print the table names in the Access db
for name in table_names:
    print (name)
    
    
# PostgreSQL database connection settings

pg_host = "localhost"
pg_port = 5432
pg_database = "world_port_index"
pg_user = "postgres"
pg_password = "password"

# Connect to PostgreSQL database

pg_connection = psycopg2.connect(
                host=pg_host,
                port=pg_port,
                dbname=pg_database,
                user=pg_user,
                password=pg_password
    )

pg_cursor = pg_connection.cursor()

# Iterate through each table

for table_name in table_names:
        access_conn = get_accessbase_conn()
        cursor = access_conn.cursor()
        
# Extract data from Access

access_query = f"SELECT * FROM [{table_name}]"
cursor.execute(access_query)
data_to_load = cursor.fetchall()

engine = create_engine('postgresql://postgres:password@localhost:5432/world_port_index')

# 1. Query the data to get the 5 nearest ports to Singapore's JURONG ISLAND port? (country =
# 'SG',port_name = 'JURONG ISLAND').Your answer should include the columns
# port_name and distance_in_meters only.


# Ans to Qtn 1

query1 = """

SELECT
    p.Main_port_name,
    (
        6371000 * 2 * ASIN(
            SQRT(
                POWER(SIN(RADIANS((p.Latitude_degrees + p.Latitude_minutes / 60) - (ji.Latitude_degrees + ji.Latitude_minutes / 60) ) / 2), 2) +
                COS(RADIANS((ji.Latitude_degrees + ji.Latitude_minutes / 60))) * COS(RADIANS((p.Latitude_degrees + p.Latitude_minutes / 60))) *
                POWER(SIN(RADIANS((p.Longitude_degrees + p.Longitude_minutes / 60) - (ji.Longitude_degrees + ji.Longitude_minutes / 60)) / 2), 2)
            )
        )
    ) AS distance_in_meters
FROM Wpi_data p
JOIN Wpi_data ji
ON p.Main_port_name != ji.Main_port_name
WHERE ji.Wpi_country_code = 'SG' AND ji.Main_port_name = 'JURONG ISLAND'
ORDER BY distance_in_meters
LIMIT 5;


"""
pd.read_sql(query1, engine)

nearest_five_ports_df = pd.read_sql(query1, engine)

nearest_five_ports_df.to_sql('nearest_five_ports_table', engine, if_exists='replace')

# 2.Execute the query to find the country with the largest number of ports with cargo_wharf

# Ans to Qtn 2 # Execute the query to find the country with the largest number of ports with cargo_wharf

query2 = """

SELECT Wpi_country_code,
    COUNT(*) AS port_count
FROM Wpi_data
WHERE Load offload wharves = 'Y'
GROUP BY Wpi_country_code
ORDER BY port_count DESC
LIMIT 1
  
"""

pd.read_sql(query2, engine)

largest_port_cargo_wharf_num_df = pd.read_sql(query2, engine)

largest_port_cargo_wharf_num_df.to_sql('largest_port_cargo_wharf_num_table', engine, if_exists='replace')

# Ans to Qtn 3: You received a distress call from the middle of the North Atlantic Ocean. The
#person on the line gave you a coordinates of lat: 32.610982, long: -38.706256 and
#asked for the nearest port with provisions, water, fuel_oil and diesel. Your answer
#should include the columns country, port_name, port_latitude and
#port_longitude only.

query3 = """

SELECT
    p.Wpi_country_code AS country,
    p.Main_port_name AS port_name,
    p.Latitude_degrees AS port_latitude,
    p.Longitude_degrees AS port_longitude,
    (
        6371000 * 2 * ASIN(
            SQRT(
                POWER(SIN(RADIANS(p.Latitude_degrees - distress.latitude) / 2), 2) +
                COS(RADIANS(distress.latitude)) * COS(RADIANS(p.Latitude_degrees)) *
                POWER(SIN(RADIANS(p.Longitude_degrees - distress.longitude) / 2), 2)
            )
        )
    ) AS distance_in_meters
FROM
    Wpi_data p
CROSS JOIN (
    SELECT
        32.610982 AS latitude,
        -38.706256 AS longitude
) distress
WHERE
    p.Supplies_provisions = 'Y' AND
    p.Supplies_water = 'Y' AND
    p.Supplies_fuel_oil = 'Y' AND
    p.Supplies_diesel_oil = 'Y'
ORDER BY
    distance_in_meters
LIMIT 1;

"""


pd.read_sql(query3, engine)

nearest_port_with_supplies_df = pd.read_sql(query3, engine)

nearest_port_with_supplies_df.to_sql('nearest_port_with_supplies_table', engine, if_exists='replace')


def load_query_to_db(query, table_name):
    df = pd.read_sql(query, engine)
    df.to_sql(table_name, engine, if_exists='replace')
    
load_query_to_db(query1,'nearest_five_ports_table')
load_query_to_db(query1,'largest_port_cargo_wharf_num_table')
load_query_to_db(query1,'nearest_port_with_supplies_table')

