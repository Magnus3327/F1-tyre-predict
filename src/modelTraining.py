import numpy as np
from sklearn.linear_model import HuberRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold, cross_val_score

# Costante fisica F1: si perdono circa 0.3 secondi ogni 10 kg di carburante.
# Poiché Fuel_Est è in kg, la penalità corrisponde a 0.03 s/kg.
# Applico questa correzione a priori per evitare problemi di multicollinearità nel modello.
FUEL_EFFECT_SEC_PER_KG = 0.03

def train_degradation_model(df):
    """
    Addestra un modello ibrido (Fisica + ML) per stimare il degrado degli pneumatici.
    Utilizza una K-Fold Cross-Validation Dinamica per adattarsi alla lunghezza 
    dello stint e l'HuberRegressor per gestire matematicamente gli outlier.
    """

    df = df.copy()

    # Correzione Fisica: sottraggo il vantaggio del carburante bruciato dal tempo sul giro
    df["LapTime_FuelCorrected"] = df["LapTime_Sec"] - (df["Fuel_Est"] * FUEL_EFFECT_SEC_PER_KG)

    # Definisco le feature per il ML (escluso il carburante, già gestito)
    X = df[["TyreLife", "TyreLife2", "TrackTemp"]]
    y = df["LapTime_FuelCorrected"]

    # Implementazione K-Fold Dinamica
    # Vogliamo assicurarci che in ogni fold ci siano almeno un minimo di giri (es. 5) nel test set per avere una metrica R2 statisticamente valida.
    min_test_laps = 5
    
    # Calcolo il numero di fold: minimo 2, massimo 5, basato sui giri a disposizione
    n_splits = max(2, min(8, len(df) // min_test_laps))
    
    # Divido lo stint in pieghe casuali. Uso shuffle=True per neutralizzare i bias temporali.
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    model = HuberRegressor()

    # Calcolo l'R2 medio sulle diverse pieghe (folds) per avere una metrica super-affidabile
    cv_scores = cross_val_score(model, X, y, cv=kf, scoring='r2')
    r2_mean = np.mean(cv_scores)

    # Addestramento finale del modello sull'intero set di dati dello stint
    # Una volta validata la stabilità, uso tutti i giri per estrarre i coefficienti finali
    model.fit(X, y)

    # Estraggo i coefficienti appresi dall'algoritmo
    tyre_coef = model.coef_[0]
    tyre2_coef = model.coef_[1]

    # Calcolo il degrado medio usando la derivata della curva (pesata sulla vita media della gomma)
    avg_life = df["TyreLife"].mean()
    deg_rate = tyre_coef + 2 * tyre2_coef * avg_life

    return model, r2_mean, deg_rate, FUEL_EFFECT_SEC_PER_KG, df