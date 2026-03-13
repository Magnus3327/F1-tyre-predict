from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score
import numpy as np


def estimate_fuel_penalty(df):
    """
    Stima quanto il carburante rallenta il giro (s/kg)
    """

    X = df[['Fuel_Est']]
    y = df['LapTime_Sec']

    model = LinearRegression()
    model.fit(X, y)

    fuel_penalty = model.coef_[0]

    return fuel_penalty


def train_degradation_model(df):

    # -------------------------
    # STEP 1: fuel effect
    # -------------------------

    fuel_penalty = estimate_fuel_penalty(df)

    # -------------------------
    # STEP 2: fuel correction
    # -------------------------

    df = df.copy()

    df['LapTime_FuelCorrected'] = (
        df['LapTime_Sec'] + df['Fuel_Est'] * fuel_penalty
    )

    # -------------------------
    # STEP 3: tyre degradation
    # -------------------------

    features = [
        'TyreLife',
        'TyreLife2',
        'TrackTemp'
    ]

    X = df[features]
    y = df['LapTime_FuelCorrected']

    model = Ridge(alpha=1.0)

    model.fit(X, y)

    y_pred = model.predict(X)

    r2 = r2_score(y, y_pred)

    # degrado medio
    tyre_coef = model.coef_[0]
    tyre2_coef = model.coef_[1]

    avg_tyre_life = df['TyreLife'].mean()

    deg_rate = tyre_coef + 2 * tyre2_coef * avg_tyre_life

    return model, r2, deg_rate, fuel_penalty