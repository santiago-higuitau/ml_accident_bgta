import requests
import pandas as pd
import math
import json
import threading
import concurrent.futures


from config.setup import SetupConfig



# Function to build endpoint
def build_endpoint(batch_size:int, offset:int, layer:int):
    """
    Construir endpoint para realizar peticiones y obtener datos.

    Args:
    - batch_size: El tamaño del lote
    - offset: El número de pasos hacia adelante que nos moveremos
    - layer: id de la capa a la cual accederemos
    """
    assert batch_size <= SetupConfig.BATCH_SIZE, f"El tamaño del lote no puede ser superior a {SetupConfig.BATCH_SIZE}"
    return f'https://services2.arcgis.com/NEwhEo9GGSHXcRXV/arcgis/rest/services/AccidentalidadAnalisis/FeatureServer/{layer}/query?where=1%3D1&outFields=*&outSR=4326&resultOffset={offset}&resultRecordCount={batch_size}&f=json'


# Function to fetch total nro rows
def fetch_total_nro_rows_of_the_layer(layer):
    """
    Obtener el número total de registros de la capa elegida.

    Args:
    - Layer: La capa elegida

    Layers:
    - Accidente: 0
    - Lesionado: 1
    - Muerto: 2
    - Actor Vial: 3
    - Causa: 4
    - Vehiculo: 5
    - Via: 6

    Return:
    - Número total de registros del conjunto de datos de la capa seleccionada!
    """
    assert layer <= SetupConfig.NRO_LAYERS, f"La capa ingresada no está disponible, por favor revisar la documentación de la función para ver las capas disponibles!"
    
    # Set endpoint
    end_point_recount = f'https://services2.arcgis.com/NEwhEo9GGSHXcRXV/arcgis/rest/services/AccidentalidadAnalisis/FeatureServer/{layer}/query?where=1%3D1&outFields=*&returnCountOnly=true&outSR=4326&f=json'

    # Make request and decode response
    total_rows_response = requests.get(end_point_recount)
    total_rows_json = total_rows_response.json()
    
    return total_rows_json['count']


# Funciones para extraer datos desde la API
thread_local = threading.local()

# Definir la sesión
def get_session():
    """
    Devuelve una sesión de requests. Si no existe una sesión previamente en el hilo actual,
    crea una nueva y la almacena en un contexto local para reutilizarla en futuras solicitudes.
    """
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


# Hacer peticiones a la API
def make_request_to_api(endpoint):
    """
    Realiza una solicitud HTTP GET a una URL específica utilizando la sesión obtenida por get_session().
    Retorna el contenido de la respuesta como un objeto JSON. Maneja los errores de conexión y decodificación de JSON.
    
    Args:
        url (str): La URL a la que se va a realizar la solicitud HTTP.
        
    Returns:
        dict: El contenido de la respuesta como un objeto JSON.
    """
    try:
        # Obtener session
        session = get_session()

        with session.get(endpoint) as response:
            try:
                return response.json() # Retornar respuesta decodificada como json
            except json.JSONDecodeError as e:
                print(f'Error al decodificar JSON en la respuesta: {e}')
                
    except (requests.ConnectionError, requests.Timeout) as e:
        print(f'Error de conexión al procesar la solicitud: {e}')


# Obtener el listado total de endpoints a consultar
def get_total_endpoints(layer:int, batch_size:int=2000, offset_initial:int=0):
    """
    Obtener el lista de endpoints a consultar, dado que tenemos una restricción de 2000 mil registros por petición.

    Args:
    - layer: La capa a consultar
    - batch_size: El número de registros a recuperar por petición; por defecto se configura el tope superior permitido (2000)
    - offset_initial: El registro desde donde se empezará a extraer la información; por defecto se configura el indice del registro inicial del conjunto de datos

    Return:
    - Una lista con el total de endpoints a consultar o usar
    """
    try:
        # Obtener Nro Total de filas
        nro_total_rows_layer = fetch_total_nro_rows_of_the_layer(layer)

        # Nro Requests
        nro_requests = math.ceil(nro_total_rows_layer / batch_size)

        # Get pages
        list_endpoints = []
        for nro in range(nro_requests):
            # Build Endpoint
            end_point_layer = build_endpoint(batch_size, offset_initial, layer)

            # Add enpoint
            list_endpoints.append(end_point_layer)

            offset_initial += batch_size

        return list_endpoints
    
    except Exception as e:
        print(f'No se pudo recuperar la lista de endpoints: {e}')


def extract_data_raw_service(layer:int, batch_size:int=2000, offset_initial:int=0):
    """
    Obtener el conjunto de datos completo de la capa elegida desde la API disponible

    Args:
    - Layer: La capa elegida
    - batch_size: El tamaño del lote, por defecto 2000 (El límite superior aceptado)
    - offset_initial: El registro desde donde comenzaremos a hacer la extracción (Por defecto empezamos desde el primer registro)
    
    Layers:
    - Accidente: 0
    - Lesionado: 1
    - Muerto: 2
    - Actor Vial: 3
    - Causa: 4
    - Vehiculo: 5
    - Via: 6

    Return:
    - El conjunto total de datos extraído desde la capa; entrega un dataframe como estructura de datos.
    """
    import warnings
    warnings.filterwarnings("ignore", message="The behavior of .* is deprecated")
    
    # Get List of the endpoints
    list_endpoints = get_total_endpoints(layer, batch_size, offset_initial)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor: # Limitamos a 10 hilos concurrentes
        responses = executor.map(make_request_to_api, list_endpoints)

    # Extract data
    df_consolidated = pd.DataFrame()

    for content_json in responses:
        try:
            if content_json:
                # Build Dataframe
                cols_df = content_json['features'][0]['attributes'].keys()
                data_df = pd.DataFrame([feature['attributes'].values() for feature in content_json['features']], columns=cols_df)

                # Insertar data df en df consolidated
                #data_df.fillna('missing', inplace=True)
                df_consolidated = pd.concat([df_consolidated, data_df])
        
        except KeyError as e:
            print(f"Error de clave en el resultado: {e}")

        except Exception as e:
            print(f'Error al procesar el resultado: {e}')

    return df_consolidated.reset_index(drop=True)