import os
import sys
from dotenv import load_dotenv


PARENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PARENT_FOLDER)


class SetupConfig:

    # Load environment variable
    load_dotenv(f'{PARENT_FOLDER}/.env')

    # Define variables: POSTGRESQL
    POST_HOST = os.environ.get('POST_HOST')
    POST_PORT = os.environ.get('POST_PORT')
    POST_DB_NAME = os.environ.get('POST_DB_NAME')
    POST_USER = os.environ.get('POST_USER')
    POST_PASSWORD = os.environ.get('POST_PASSWORD')
    IF_EXISTS = os.environ.get('IF_EXISTS')
    DBN_CONN_STR = f'postgresql+psycopg2://{POST_USER}:{POST_PASSWORD}@{POST_HOST}:{POST_PORT}/{POST_DB_NAME}'

    # Other variables
    BATCH_SIZE = os.environ.get('BATCH_SIZE')
    NRO_LAYERS = os.environ.get('NRO_LAYERS')

    # Name Tables
    TABLE_ACCIDENTE = os.environ.get('TABLE_ACCIDENTE')
    TABLE_LESIONADO = os.environ.get('TABLE_LESIONADO')
    TABLE_MUERTO = os.environ.get('TABLE_MUERTO')
    TABLE_ACTOR_VIAL = os.environ.get('TABLE_ACTOR_VIAL')
    TABLE_CAUSA = os.environ.get('TABLE_CAUSA')
    TABLE_VEHICULO = os.environ.get('TABLE_VEHICULO')
    TABLE_VIA = os.environ.get('TABLE_VIA')