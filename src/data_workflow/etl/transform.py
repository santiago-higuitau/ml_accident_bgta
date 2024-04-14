import pandas as pd
import math
from datetime import datetime, timedelta
import pytz


def logic_to_support_negative_values(date_value):
    """
    """
    try:
        if date_value >= 0:
            return datetime.fromtimestamp(math.floor(date_value))
        else:
            base_date = datetime(1970, 1, 1)
            difference_to_bd = timedelta(seconds=abs(date_value))
            return (base_date - difference_to_bd).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('America/Bogota')).replace(tzinfo=None)

    except:
        return datetime(1975, 1, 1, 1, 0)



def transform_date(dataset:pd.DataFrame, col_date:str):
    """
    """
    # Create Dataframe Aux
    df_aux = dataset.copy()

    # Date to replace NAs - Timestamp format
    date_for_na = datetime(1975, 1, 1, 1, 0).timestamp() * 1000

    # Replace NAs
    df_aux[col_date] = (df_aux[col_date].fillna(date_for_na) / 1000).map(lambda d: logic_to_support_negative_values(d))

    return df_aux


def transform_all_dates(dataset:pd.DataFrame):
    """
    """
    # Create Dataframe Aux
    df_aux = dataset.copy()

    # Get dates
    dates_dataset = [fecha for fecha in df_aux.columns if 'FECHA' in fecha]

    # Set each date in dataset
    for date in dates_dataset:
        df_aux = transform_date(df_aux, date)

    return df_aux


# Servicio de transformación
def data_transformation_service(dataset: pd.DataFrame):
    """
    """
    # Df Aux
    df_aux = dataset.copy()

    # Transform Dates
    return transform_all_dates(df_aux)