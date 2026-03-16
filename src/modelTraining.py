from sklearn.linear_model import HuberRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

# Costante fisica F1: si perdono circa 0.3 secondi ogni 10 kg di carburante.
# Poiché Fuel_Est è in kg, la penalità corrisponde a 0.03 s/kg.
# Applico questa correzione a priori per evitare problemi di multicollinearità nel modello.
FUEL_EFFECT_SEC_PER_KG = 0.03

def train_degradation_model(df):
    """
    Addestra un modello ibrido (Fisica + ML) per stimare il degrado degli pneumatici.
    Ho scelto l'HuberRegressor perché, usando la Huber Loss, è matematicamente
    robusto contro gli outlier (es. piccoli bloccaggi o traffico) rispetto a OLS/Ridge.
    """

    df = df.copy()

    # Correzione Fisica: sottraggo il vantaggio del carburante bruciato dal tempo sul giro
    df["LapTime_FuelCorrected"] = df["LapTime_Sec"] - (df["Fuel_Est"] * FUEL_EFFECT_SEC_PER_KG)

    # Definisco le feature per il ML (escluso il carburante, già gestito)
    X = df[["TyreLife", "TyreLife2", "TrackTemp"]]
    y = df["LapTime_FuelCorrected"]

    # Suddivisione Train/Test.
    # Uso shuffle=True per estrarre campioni da tutto lo stint. 
    # È fondamentale per evitare bias dovuti al "warm-up" delle gomme, specialmente su piste fredde.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=True, random_state=42)

    # Addestramento del HuberRegressor
    model = HuberRegressor()
    model.fit(X_train, y_train)

    # Valutazione sui dati di test (R2 può essere negativo se c'è molta varianza/traffico)
    y_pred_test = model.predict(X_test)
    r2_test = r2_score(y_test, y_pred_test)

    # Estraggo i coefficienti appresi dall'algoritmo
    tyre_coef = model.coef_[0]
    tyre2_coef = model.coef_[1]

    # Calcolo il degrado medio usando la derivata della curva (pesata sulla vita media della gomma)
    avg_life = df["TyreLife"].mean()
    deg_rate = tyre_coef + 2 * tyre2_coef * avg_life

    return model, r2_test, deg_rate, FUEL_EFFECT_SEC_PER_KG, df