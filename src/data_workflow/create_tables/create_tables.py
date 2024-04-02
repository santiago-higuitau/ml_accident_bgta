import os
import sys
import psycopg2
from dotenv import load_dotenv
from urllib.parse import urlparse


from config.setup import SetupConfig
# from create_tables.dict_tables import TablesConfig

# Function Get Connection
def get_connection():
    """
    """
    # Obtener db str
    db_str = urlparse(SetupConfig.DBN_CONN_STR)

    # Create Connection
    connection_post = psycopg2.connect(
                host=db_str.hostname,
                port=db_str.port,
                user=db_str.username,
                password=db_str.password,
                dbname=db_str.path.replace('/', ''),
                sslmode='disable'
    )

    connection_post.autocommit = True

    return connection_post


# Función para ejecutar query
def execute_query(sql_query):
    """
    """
    # Create Cursor (Driver)
    connection_db = get_connection()
    cursor_db = connection_db.cursor()

    # Execute query
    cursor_db.execute(sql_query)

    # Close connection
    cursor_db.close()


# Función para crear tablas
def create_tble(sql_query):
    """
    """
    execute_query(sql_query)