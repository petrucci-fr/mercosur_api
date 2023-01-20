from dotenv import load_dotenv
import os
import pyodbc
import pandas as pd


load_dotenv()


def get_data(query: str):

    # define DPlus database connection string
    CONNECTION_STRING = f"""
        DSN={{FreeTDS}};
        HOST={os.getenv('HOST')};
        DB={os.getenv('DB')};
        UID={os.getenv('UID')};
        PWD={os.getenv('PWD')};
        PORT={os.getenv('PORT')};
    """

    # DSN={{FreeTDS}};
    # DSN={os.getenv('DSN')};

    # instantiate connection and cursor objects
    connection = pyodbc.connect(CONNECTION_STRING)
    cursor = connection.cursor()

    # retrieve data and dump it in a dataframe
    records = cursor.execute(query).fetchall()
    columns = [column[0] for column in cursor.description]    
    df = pd.DataFrame.from_records(
        data=records,
        columns=columns
    )

    # close connection
    cursor.close()
    connection.close()
    
    return df