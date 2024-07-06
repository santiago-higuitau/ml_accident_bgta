
import os
import pickle
from datetime import datetime, time
import locale
import sys
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

sys.path.append(os.getcwd())
from src.frontend.config import config
from src.model.model import ModelTuner

with open(f'{os.getcwd()}/src/model/best_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Establecer la configuración regional a español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Set up initial
st.set_page_config(layout='wide')
st.title('Clasificador de Accidentes por Localidad en :violet[Bogotá]')
st.divider()

# Inicializar Session
if 'input_data' not in st.session_state:
    st.session_state.input_data = {
        "ANO_OCURRENCIA_ACC": datetime.now().year,
        "MES_OCURRENCIA_ACC": datetime.now().strftime('%B').upper(),
        "DIA_OCURRENCIA_ACC": datetime.now().strftime('%A').upper(),
        "GRAVEDAD": "SOLO DANOS",
        "TIPO_CAUSA": "CONDUCTOR",
        "nroinfracciones": 0.0,
        "CLASE_ACC": "CHOQUE",
        "LOCALIDAD": "SUBA",
        "LATITUD": 4.652290,
        "LONGITUD": -74.108810,
        "CONDICION_ACCIDENTADO": "CONDUCTOR",
        "EDAD": 0.0,
        "GENERO": "MASCULINO",
        "CLASE_DE_VEHICULO": "VEHICULOS COMERCIALES",
        "TIPO_DE_SERVICIO": "PUBLICO",
        "PARTE_DEL_DIA": config.categorizar_parte_del_dia(datetime.now().time())
    }

# Set Columnas
col_1, col_2 = st.columns(2)

# Set col 1
actual_date = datetime.now()
with col_1:
    ############################## SELECCIONAR FECHA OCURRENCIA ##############################
    date_selected = st.date_input("Selecciona una fecha de ocurrencia", actual_date)

    # Calculate Ano, mes y dia de ocurrencia
    config.update_session_state("ANO_OCURRENCIA_ACC", date_selected.year)
    config.update_session_state("MES_OCURRENCIA_ACC", date_selected.strftime('%B').upper())
    config.update_session_state("DIA_OCURRENCIA_ACC", date_selected.strftime('%A').upper())

    # Show
    st.write(f'Año de ocurrencia: {st.session_state.input_data["ANO_OCURRENCIA_ACC"]}')
    st.write(f'Mes de ocurrencia: {st.session_state.input_data["MES_OCURRENCIA_ACC"]}')
    st.write(f'Día de ocurrencia: {st.session_state.input_data["DIA_OCURRENCIA_ACC"]}')
    #st.divider()

    ############################## SELECCIONAR HORA OCURRENCIA ##############################
    # Set hour and minute
    hour = actual_date.hour
    minute = actual_date.minute

    hour_selected = st.time_input("Seleccione una hora de ocurrencia", time(hour, minute))
    # Calculate part of the day
    part_of_day = config.categorizar_parte_del_dia(hour_selected)
    st.write(f'Parte del día seleccionado {part_of_day}')
    #st.divider()

    ############################## SELECCIONAR LOCALIDAD ##############################
    # Seleccionar Una Localidad
    localidad_acc = st.selectbox("Localidad", 
                                config.localidades,
                                index=None,
                                placeholder="Seleccionar una localidad...")
    #st.divider()

    ############################# SELECCIONAR GRAVEDAD ACCIDENTE #############################
    # Seleccionar Gravedad Accidente
    gravedad_acc = st.selectbox("Gravedad del Accidente", 
                                ('SOLO DANOS', 'CON HERIDOS', 'CON MUERTOS'),
                                index=None,
                                placeholder="Seleccionar la gravedad del accidente...")
    #st.divider()

    ############################# SELECCIONAR TIPO CAUSA ACCIDEN #############################
    tipo_acc = st.selectbox("Tipo de Causa Accidente", 
                            ('CONDUCTOR', 'VEHICULO-VIA', 'PASAJERO', 'PEATON'),
                            index=None,
                            placeholder="Seleccionar el tipo de causa del accidente...")
    #st.divider()

    # Seleccionar tipo de vehiculo
    clase_vehiculo = st.selectbox("Clase de Vehiculo", 
                                ['VEHICULOS COMERCIALES', 'VEHICULOS PERSONALES',
                                'TRANSPORTE PUBLICO', 'OTROS'],
                                index=None,
                                placeholder="Seleccionar la clase de vehículo...")
    #st.divider()

    # Seleccionar tipo de servicio
    tipo_de_servicio = st.selectbox("Tipo de servicio del Vehiculo", 
                                    ['PUBLICO', 'PARTICULAR', 'OTRO'],
                                    index=None,
                                    placeholder="Seleccionar el tipo de servicio del vehículo...")
    

    # Número de infracciones:
    nro_infra = st.number_input('Número de Infracciones', value=0, placeholder="Ingrese el número de infracciones...")
    #st.divider()

    ############################# SELECCIONAR CLASE DE ACCIDENTE #############################
    clase_acc = st.selectbox("Clase de Accidente", 
                            ('CHOQUE', 'ATROPELLO', 'SIN INFORMACION', 'AUTOLESION',
                            'VOLCAMIENTO', 'OTRO', 'CAIDA DE OCUPANTE', 'INCENDIO'),
                            index=None,
                            placeholder="Seleccionar la clase de accidente...")
    #st.divider()

    ############################# SELECCIONAR CONDICIÓN ACCIDENTADO #############################
    condicion_accidentado = st.selectbox("Condición Accidentado", 
                                        ('CONDUCTOR', 'PEATON', 'MOTOCICLISTA', 'PASAJERO', 'CICLISTA'),
                                        index=None,
                                        placeholder="Seleccionar la condición del accidentado...")
    #st.divider()

    # Edad accidentado:
    edad_accidentado = st.number_input('Edad', value=0, placeholder="Ingrese la edad del accidentado...")
    #st.divider()

    # Gen o Sexo del accidentado:
    gen_accidentado = st.selectbox("Género", ["MASCULINO", "FEMENINO"],
                                index=None,
                                placeholder="Ingrese el género del accidentado...")
    #st.divider()

with col_2:
    st.write("Seleccionar la coordenada del accidente")
    bogota_coords = [4.652290, -74.108810]
    LATITUD = bogota_coords[0]
    LONGITUD = bogota_coords[1]

    # Crear el mapa inicial centrado en Bogotá
    m = folium.Map(location=bogota_coords, zoom_start=12)
    marker = folium.Marker(location=[LATITUD, LONGITUD], draggable=True, popup='Haga clic para seleccionar la ubicación')
    marker.add_to(m)

    # Renderizar el mapa inicial y obtener datos de clic
    map_data = st_folium(m, width=900, height=700)

    # Verificar si se ha hecho clic en el mapa
    try:
        LATITUD = map_data['last_clicked'].get('lat', LATITUD)
        LONGITUD = map_data['last_clicked'].get('lng', LONGITUD)
        st.write(f"Latitud seleccionada: {LATITUD}")
        st.write(f"Longitud seleccionada: {LONGITUD}")
    except:
        st.write(f"Latitud por defecto: {LATITUD}")
        st.write(f"Longitud por defecto: {LONGITUD}")
    st.divider()

    # Hace Predicción

    # Datos de entrada:
    input_data = st.session_state.input_data

    _, col_med, _ = st.columns(3)
    with col_med:
        if st.button("Predecir"):            
            # Make request
            input_df = pd.DataFrame([input_data])
            prediction = model.predict(input_df)
        dict_set_predict = config.dict_set_predict
    try:
        st.success(f"La predicción es: {dict_set_predict[prediction[0]]}")
    except:
        st.write("")
