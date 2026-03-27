import numpy as np
from sklearn.linear_model import HuberRegressor
from sklearn.model_selection import KFold, cross_val_score

# Costante fisica F1: 0.03 s persi per ogni kg di carburante
FUEL_EFFECT_SEC_PER_KG = 0.03

def train_degradation_model(df):
    """
    Addestra un modello HuberRegressor robusto per stimare l'usura degli pneumatici, gestendo gli outlier tramite validazione MAE.
    """

    df = df.copy()

    # Correzione fisica a priori
    df["LapTime_FuelCorrected"] = df["LapTime_Sec"] - (df["Fuel_Est"] * FUEL_EFFECT_SEC_PER_KG)

    X = df[["TyreLife", "TyreLife2"]]
    y = df["LapTime_FuelCorrected"]

    # K-Fold Dinamica proporzionata allo stint
    min_test_laps = 5
    n_splits = max(2, min(8, len(df) // min_test_laps))
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    model = HuberRegressor(max_iter=1000)

    # Calcolo dell'Errore Medio Assoluto (MAE)
    cv_scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_absolute_error')
    mae_mean = -np.mean(cv_scores)

    # Fitting finale sull'intero stint
    model.fit(X, y)

    # Calcolo del degrado medio pesato
    tyre_coef = model.coef_[0]
    tyre2_coef = model.coef_[1]
    avg_life = df["TyreLife"].mean()
    deg_rate = tyre_coef + 2 * tyre2_coef * avg_life

    # Estraiamo la maschera degli outlier identificati dalla Huber Loss
    outlier_mask = model.outliers_

    return model, mae_mean, deg_rate, FUEL_EFFECT_SEC_PER_KG, df, outlier_mask