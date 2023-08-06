# This script contains package functions for reading data from Snowflake

# import libraries
import sqlalchemy
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector as snowctx
import pandas as pd
import json

# Write a function for initialzing a connection to the datawarehouse 
def start_engine(account,user,password,role,warehouse='LOAD_WH',database='TOMO',schema='DBT_PRODUCTION_SRC'):
    '''Function to initialize a connection to Tomo's Snowflake DW.
    Inputs:
        account - Tomo's Snowflake account
        user - the username of the individual's snowflake account
        password - the password of the individual's snowflake account
        role - the user's Snowflake role (e.g. ACCOUNTADMIN)
        warehouse - the warehouse used for compute resources (default is LOAD_WH)
        database - The target data base for querying (default is TOMO)
        schema - the target schema for querying  (default is DBT_PRODUCCTION_SRC)
    Outputs: 
        Returns a SQL Alchemy engine for querying the Tomo DW
    '''
    # create engine from URL string. URL is a helper function to create a URL in the format Snowflake accepts for connections
    engine = create_engine(URL(
            account = account,
            user = user,
            password = password,
            role = role,
            warehouse = warehouse,
            database = database,
            schema =  schema
        ))

    return engine

# Function for reading a query from a sql file
def read_sql_file(sql_file,engine):
    '''Function to read a SQL file into a pandas dataframe
    Inputs:
        sql_file - a .sql file that includes the query you want to load
        engine - a SQL Alchemy database connection engine
    Outputs:
        returns a pandas dataframe that matches the output of the SQL query
    '''
    # Read the sql file
    query = open(sql_file, 'r')

    # initialize a connection with engine
    with engine.connect() as conn:
        df = pd.read_sql_query(query.read(),conn) # read the sql file to a dataframe

    query.close() # close the sql file 

    return df

# function for reading a query from a text string 
def read_sql_query(query, engine):
    '''
    Inputs:
        engine: A SQL alchemy engine connection
        query: A text string containing the SQL code for the query 
    Outputs:
        df: A pandas dataframe based on the SQL query
    '''

    # initialize a connection with engine
    with engine.connect() as conn:
        df = pd.read_sql_query(query,conn) # read the sql file to a dataframe

    return df
