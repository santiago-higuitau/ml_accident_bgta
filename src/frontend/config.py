"""Module: Config Definition"""

import os
import zipfile
import pickle
from datetime import time, datetime
import streamlit as st

# Configuration Class
class ConfigFront:
    """Class Config Definition"""
    def __init__(self):
        self.endpoint = 'FAST API'
        self.localidades = ['FONTIBON', 'CIUDAD BOLIVAR', 'ENGATIVA', 'KENNEDY', 'SUBA',
                            'RAFAEL URIBE URIBE', 'LOS MARTIRES', 'SANTA FE', 'USAQUEN',
                            'TEUSAQUILLO', 'BARRIOS UNIDOS', 'BOSA', 'CHAPINERO', 'TUNJUELITO',
                            'ANTONIO NARINO', 'PUENTE ARANDA', 'SAN CRISTOBAL', 'USME',
                            'CANDELARIA', 'SUMAPAZ']
        self.dict_set_predict = {
            0: 'HERIDO',
            1: 'ILESO',
            2: 'MUERTO'
        }

    # Methods
    def categorizar_parte_del_dia(self, hora_ocurrencia: time):
        """
        Categoriza la parte del día en función de la hora de ocurrencia.
        """
        if hora_ocurrencia < time(6, 0):
            return 'MADRUGADA'
        elif hora_ocurrencia < time(12, 0):
            return 'MANANA'
        elif hora_ocurrencia < time(18, 0):
            return 'TARDE'
        else:
            return 'NOCHE'

    # Función para actualizar estado de sesión
    def update_session_state(self, key, value):
        st.session_state.input_data[key] = value
    
    def load_model_from_zip(self, zip_path, model_filename):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extract(model_filename)
        with open(model_filename, 'rb') as file:
            model = pickle.load(file)
        os.remove(model_filename)
        return model

# Instance Config
config = ConfigFront()