from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

def train_degradation_model(df):
    """
    Addestra un modello multivariato per stimare il degrado degli pneumatici,
    tenendo conto simultaneamente del consumo di carburante. Utilizza una 
    suddivisione train/test per una valutazione scientificamente rigorosa.
    """
    df = df.copy()

    # 1. Definizione di tutte le feature per il modello multivariato
    features = ["TyreLife", "TyreLife2", "TrackTemp", "Fuel_Est"]
    X = df[features]
    y = df["LapTime_Sec"]

    # 2. Suddivisione cronologica Train/Test
    # Addestriamo sul primo 75% dei giri dello stint per prevedere il restante 25%.
    # Il parametro shuffle=False è fondamentale per i dati temporali (serie storiche)
    # per evitare il "data leakage" (sbirciare nel futuro durante l'addestramento).
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=False)

    # 3. Addestramento del modello Ridge (regolarizzato)
    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)

    # 4. Valutazione pura sui dati di test (mai visti dal modello)
    y_pred_test = model.predict(X_test)
    r2_test = r2_score(y_test, y_pred_test)

    # 5. Estrazione dei coefficienti
    # Il modello isola organicamente l'effetto del carburante insieme all'usura delle gomme
    tyre_coef = model.coef_[0]
    tyre2_coef = model.coef_[1]
    fuel_penalty = model.coef_[3] 

    # 6. Calcolo del tasso di degrado medio
    avg_life = df["TyreLife"].mean()
    deg_rate = tyre_coef + 2 * tyre2_coef * avg_life

    # 7. Creazione dei tempi sul giro corretti per il carburante (per i grafici)
    # Sottraiamo l'effetto isolato del carburante per visualizzare il puro degrado della gomma
    df["LapTime_FuelCorrected"] = df["LapTime_Sec"] - (df["Fuel_Est"] * fuel_penalty)

    return model, r2_test, deg_rate, fuel_penalty, df