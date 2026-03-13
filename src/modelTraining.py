from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
import numpy as np


def train_degradation_model(df):

    features = [
        'TyreLife',
        'TyreLife2',
        'TrackTemp',
        'Fuel_Est',
        'LapNumber'
    ]

    X = df[features]
    y = df['LapTime_Sec']

    model = Ridge(alpha=1.0)

    model.fit(X, y)

    y_pred = model.predict(X)

    r2 = r2_score(y, y_pred)

    # --------------------------
    # degrado medio stimato
    # --------------------------

    tyre_coef = model.coef_[0]
    tyre2_coef = model.coef_[1]

    avg_tyre_life = df['TyreLife'].mean()

    deg_rate = tyre_coef + 2 * tyre2_coef * avg_tyre_life

    return model, r2, deg_rate