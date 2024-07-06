import numpy as np
import os
import pickle
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer

class ModelTuner:
    def __init__(self, model, param_grid, dataset):
        self.model = model
        self.param_grid = param_grid
        self.dataset = dataset
        self.label_encoder = LabelEncoder()
        
        # Pre-procesamiento inicial
        self.dataset['ESTADO'] = self.label_encoder.fit_transform(self.dataset['ESTADO'])

    def encode_gender(self, X):
        X = X.copy()
        X['GENERO'] = X['GENERO'].map({'MASCULINO': 1, 'FEMENINO': 0})
        return X
    
    def create_column_transformer(self):
        categorical_features = self.dataset.select_dtypes(include=['object', 'category']).columns
        numerical_features = ['LATITUD', 'LONGITUD', 'EDAD', 'nroinfracciones']
        return ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numerical_features),
                ('cat', OneHotEncoder(), categorical_features)
            ]
        )
    
    def tune_model(self):
        initial_transformer = FunctionTransformer(self.encode_gender)
        pipeline = Pipeline([
            ('initial_preprocessing', initial_transformer),
            ('preprocessor', self.create_column_transformer()),
            ('classifier', self.model)
        ])
        
        random_search = RandomizedSearchCV(
            estimator=pipeline,
            param_distributions=self.param_grid,
            n_iter=4, # Definir 10 iteraciones
            cv=2,
            verbose=2,
            random_state=42,
            n_jobs=-1
        )
        
        X_train, X_test, y_train, y_test = train_test_split(self.dataset.drop('ESTADO', axis=1), self.dataset['ESTADO'], test_size=0.15, stratify=self.dataset['ESTADO'], random_state=42)
        random_search.fit(X_train, y_train)
        y_pred = random_search.predict(X_test)
        
        print(classification_report(self.label_encoder.inverse_transform(y_test), self.label_encoder.inverse_transform(y_pred)))
        print("Mejores parámetros:", random_search.best_params_)
        
        # Serializar y guardar el modelo en un archivo .pkl
        with open(f'{os.path.dirname(os.getcwd())}/src/model/best_model.pkl', 'wb') as file:
            pickle.dump(random_search.best_estimator_, file)
        print("Modelo guardado como best_model.pkl")