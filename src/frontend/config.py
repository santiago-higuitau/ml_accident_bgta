"""Module: Config Definition"""

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

# Instance Config
config = ConfigFront()