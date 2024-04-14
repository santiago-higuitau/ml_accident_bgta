import requests
import pandas as pd
from sqlalchemy import create_engine



from src.config.setup import SetupConfig
from src.data_workflow.create_tables.create_tables import create_tble

# Load Service data
def load_service(sql_query: str, table: str, data_transformed: pd.DataFrame, if_exists: str):
    """
    """
    #0. Create Tble Historical IF NO EXISTS
    create_tble(sql_query)

    #1. Get database URL and create an SQLAlchemy engine
    db_pg_url = SetupConfig.DBN_CONN_STR
    engine_pg = create_engine(db_pg_url)

    #2. Ingest Data
    data_transformed.to_sql(table, engine_pg, if_exists=if_exists, index=False)
    print(f'Data Ingested successfully!')