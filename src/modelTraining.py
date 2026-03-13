from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

def train_degradation_model(df):
    """
    Addestra il modello di regressione multivariata per isolare il degrado della gomma.
    Ritorna: modello, r2, e il degrado puro (secondi/giro).
    """
    # 1. Definiamo le features (X) e il target (y)
    # Includiamo il carburante per depurare l'effetto dell'usura
    features = ['TyreLife', 'TrackTemp', 'Fuel_Est']
    X = df[features]
    y = df['LapTime_Sec']

    # 2. Addestramento del modello
    model = LinearRegression()
    model.fit(X, y)

    # 3. Predizione e Valutazione
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    # 4. Estrazione del Degradation Rate (Coefficiente di TyreLife)
    # Rappresenta quanto tempo si perde per ogni giro di invecchiamento gomma
    deg_rate = model.coef_[0]
    
    # Estrazione dell'effetto carburante (per curiosità tecnica nel report)
    # Rappresenta quanto tempo si guadagna per ogni kg di benzina bruciato
    fuel_effect = model.coef_[2]

    return model, r2, deg_rate