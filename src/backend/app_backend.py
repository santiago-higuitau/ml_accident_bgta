"""Model Service"""

import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle

# Cargar el modelo y el pipeline entrenados
sys.path.append(os.getcwd())
with open(f'{os.getcwd()}/model/best_model.pkl', 'rb') as file:
    model = pickle.load(file)

app = FastAPI()

class PredictionRequest(BaseModel):
    ANO_OCURRENCIA_ACC: int
    MES_OCURRENCIA_ACC: str
    DIA_OCURRENCIA_ACC: str
    GRAVEDAD: str
    TIPO_CAUSA: str
    nroinfracciones: float
    CLASE_ACC: str
    LOCALIDAD: str
    LATITUD: float
    LONGITUD: float
    CONDICION_ACCIDENTADO: str
    EDAD: float
    GENERO: str
    CLASE_DE_VEHICULO: str
    TIPO_DE_SERVICIO: str
    PARTE_DEL_DIA: str

def preprocess_input(data: dict):
    df = pd.DataFrame([data])
    df['GENERO'] = df['GENERO'].map({'MASCULINO': 1, 'FEMENINO': 0})
    return df

@app.post("/predict")
def predict(request: PredictionRequest):
    data = request.dict()
    df = preprocess_input(data)
    prediction = model.predict(df)
    return {"prediction": prediction[0]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
