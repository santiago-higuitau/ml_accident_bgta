from src.config.setup import SetupConfig


# Diccionario SQL Query
class TablesConfig:
    # SQL Query Tabla Accidente
    sql_query_accidente = f"""
        CREATE TABLE IF NOT EXISTS {SetupConfig.TABLE_ACCIDENTE}(
            INSERTION_DATE TIMESTAMP NOT NULL DEFAULT current_timestamp,
            OBJECTID INT,
            FORMULARIO VARCHAR,
            CODIGO_ACCIDENTE BIGINT,
            FECHA_OCURRENCIA_ACC TIMESTAMP,
            HORA_OCURRENCIA_ACC VARCHAR,
            ANO_OCURRENCIA_ACC INT,
            MES_OCURRENCIA_ACC CHAR(30),
            DIA_OCURRENCIA_ACC CHAR(30),
            DIRECCION VARCHAR(250),
            GRAVEDAD CHAR(100),
            CLASE_ACC CHAR(50),
            LOCALIDAD CHAR(50),
            MUNICIPIO CHAR(100),
            FECHA_HORA_ACC TIMESTAMP,
            LATITUD FLOAT(4),
            LONGITUD FLOAT(4),
            CIV VARCHAR(100),
            PK_CALZADA VARCHAR(100)
        )
    """

    # SQL Query Tabla Lesionado
    sql_query_lesionado = f"""
        CREATE TABLE IF NOT EXISTS {SetupConfig.TABLE_LESIONADO}(
            INSERTION_DATE TIMESTAMP NOT NULL DEFAULT current_timestamp,
            CODIGO_ACCIDENTADO BIGINT,
            FORMULARIO VARCHAR,
            FECHA_OCURRENCIA_ACC TIMESTAMP,
            HORA_OCURRENCIA_ACC VARCHAR,
            ANO_OCURRENCIA_ACC INT,
            MES_OCURRENCIA_ACC CHAR(30),
            DIA_OCURRENCIA_ACC CHAR(30),
            FECHA_HORA_ACC TIMESTAMP,
            DIRECCION VARCHAR(250),
            CLASE_ACC CHAR(50),
            LOCALIDAD CHAR(50),
            CODIGO_VEHICULO INT,
            CONDICION CHAR(50),
            GENERO CHAR(30),
            EDAD INT
        )
    """

    # SQL Query Tabla Muerto
    sql_query_muerto = f"""
        CREATE TABLE IF NOT EXISTS {SetupConfig.TABLE_MUERTO}(
            INSERTION_DATE TIMESTAMP NOT NULL DEFAULT current_timestamp,
            CODIGO_ACCIDENTADO BIGINT,
            FORMULARIO VARCHAR,
            FECHA_OCURRENCIA_ACC TIMESTAMP,
            HORA_OCURRENCIA_ACC VARCHAR,
            ANO_OCURRENCIA_ACC INT,
            MES_OCURRENCIA_ACC CHAR(30),
            DIA_OCURRENCIA_ACC CHAR(30),
            FECHA_HORA_ACC TIMESTAMP,
            DIRECCION VARCHAR(250),
            CLASE_ACC CHAR(50),
            LOCALIDAD CHAR(50),
            CODIGO_VEHICULO INT,
            CONDICION CHAR(50),
            MUERTE_POSTERIOR CHAR(10),
            FECHA_POSTERIOR_MUERTE TIMESTAMP,
            GENERO CHAR(30),
            EDAD INT
        )
    """

    # SQL Query Tabla Actor Vial
    sql_query_actor_vial = f"""
        CREATE TABLE IF NOT EXISTS {SetupConfig.TABLE_ACTOR_VIAL}(
            INSERTION_DATE TIMESTAMP NOT NULL DEFAULT current_timestamp,
            FORMULARIO VARCHAR,
            CODIGO_ACCIDENTADO BIGINT,
            CODIGO_VICTIMA INT,
            CODIGO_VEHICULO INT,
            CONDICION CHAR(50),
            ESTADO CHAR(30),
            MUERTE_POSTERIOR CHAR(10),
            FECHA_MUERTE_POSTERIOR TIMESTAMP,
            GENERO CHAR(30),
            FECHA_NACIMIENTO TIMESTAMP,
            EDAD INT,
            CODIGO VARCHAR(50),
            CONDICION_VEHICULO CHAR(50)
        )
    """

    # SQL Query Tabla Causa
    sql_query_causa = f"""
        CREATE TABLE IF NOT EXISTS {SetupConfig.TABLE_CAUSA}(
            INSERTION_DATE TIMESTAMP NOT NULL DEFAULT current_timestamp,
            FORMULARIO VARCHAR,
            CODIGO_ACCIDENTE BIGINT,
            CODIGO_VEHICULO INT,
            CODIGO_CAUSA INT,
            NOMBRE VARCHAR(250),
            TIPO VARCHAR(30),
            TIPO_CAUSA VARCHAR(100),
            CODIGO VARCHAR(100),
            CODIGO_AC_VH VARCHAR(100)
        )
    """

    # SQL Query Tabla Vehiculo
    sql_query_vehiculo = f"""
        CREATE TABLE IF NOT EXISTS {SetupConfig.TABLE_VEHICULO}(
            INSERTION_DATE TIMESTAMP NOT NULL DEFAULT current_timestamp,
            FORMULARIO VARCHAR,
            PLACA VARCHAR(20),
            CODIGO_VEHICULO INT,
            CLASE CHAR(50),
            SERVICIO CHAR(50),
            MODALIDAD VARCHAR(150),
            EN_FUGA CHAR(10),
            CODIGO VARCHAR(30)
        )
    """

    # SQL Query Tabla Via
    sql_query_via = f"""
        CREATE TABLE IF NOT EXISTS {SetupConfig.TABLE_VIA}(
            INSERTION_DATE TIMESTAMP NOT NULL DEFAULT current_timestamp,
            FORMULARIO VARCHAR,
            CODIGO_ACCIDENTE BIGINT,
            CODIGO_VIA INT,
            GEOMETRICA_A VARCHAR(30),
            GEOMETRICA_B VARCHAR(30),
            GEOMETRICA_C VARCHAR(30),
            UTILIZACION VARCHAR(50),
            CALZADAS VARCHAR(30),
            CARRILES VARCHAR(30),
            MATERIAL VARCHAR(30),
            ESTADO VARCHAR(20),
            CONDICIONES VARCHAR(100),
            ILUMINACION_A VARCHAR(50),
            ILUMINACION_B VARCHAR(50),
            AGENTE_TRANSITO CHAR(20),
            SEMAFORO VARCHAR(50),
            VISUAL VARCHAR(100),
            CODIGO VARCHAR(100)
        )
    """