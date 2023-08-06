# This script contains package functions for writing data to Snowflake

import sqlalchemy
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector as snowctx
import pandas as pd
import json

def upload_data_to_snowflake(engine, df, table_name, schema, chunksize=None, if_exists='append'):
    '''
    Function for uploading contents of a pandas dataframe to Snowflake table
    Inputs:
        engine:  A SQL Alchemy database connection 
        df: A pandas dataframe in the format of the table
        table_name: Name of the target table where the data will be uploaded
        schema: Name of the target schema wher eteh data will be uploaded

    Outputs:
        None
    '''
    df.to_sql(name=table_name, con=engine, schema=schema, index=False, chunksize=chunksize, if_exists=if_exists)
    print("Data successfully uploaded")

    return None