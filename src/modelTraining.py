from sklearn.linear_model import HuberRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

# Costante fisica di dominio F1: ~0.3 secondi ogni 10 kg di carburante.
# Poiché Fuel_Est è espresso in kg, la penalità è 0.3 / 10 = 0.03 s/kg.
FUEL_EFFECT_SEC_PER_KG = 0.03

def train_degradation_model(df):
    """
    Addestra un modello ibrido (Fisica + ML Robusto) per stimare il degrado.
    Utilizza HuberRegressor, che è matematicamente immune agli outlier 
    (come bloccaggi, traffico o errori del pilota) grazie alla Huber Loss.
    """
    df = df.copy()

    # 1. Correzione Fisica (Domain Knowledge)
    # Sottraiamo l'effetto del carburante PRIMA di addestrare il modello ML.
    df["LapTime_FuelCorrected"] = df["LapTime_Sec"] - (df["Fuel_Est"] * FUEL_EFFECT_SEC_PER_KG)

    # 2. Definizione delle feature per il modello ML
    features = ["TyreLife", "TyreLife2", "TrackTemp"]
    X = df[features]
    
    # Il target è il tempo al netto del carburante
    y = df["LapTime_FuelCorrected"]

    # 3. Suddivisione cronologica Train/Test (75% - 25%)
    # Manteniamo shuffle=False perché vogliamo simulare una vera previsione temporale
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=True)

    # 4. Addestramento del modello Robusto
    # Sostituiamo Ridge con HuberRegressor
    model = HuberRegressor()
    model.fit(X_train, y_train)

    # 5. Valutazione sui dati di test (mai visti prima)
    y_pred_test = model.predict(X_test)
    r2_test = r2_score(y_test, y_pred_test)

    # 6. Estrazione dei coefficienti di degrado dal Machine Learning
    tyre_coef = model.coef_[0]
    tyre2_coef = model.coef_[1]

    # 7. Calcolo del tasso di degrado medio (secondi persi per ogni giro)
    avg_life = df["TyreLife"].mean()
    deg_rate = tyre_coef + 2 * tyre2_coef * avg_life

    # Restituiamo la costante fisica al posto del coefficiente stimato 
    return model, r2_test, deg_rate, FUEL_EFFECT_SEC_PER_KG, df