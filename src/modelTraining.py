from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score

def estimate_fuel_penalty(df):
    X = df[["Fuel_Est"]]
    y = df["LapTime_Sec"]
    model = LinearRegression()
    model.fit(X, y)
    return model.coef_[0]

def train_degradation_model(df):
    fuel_penalty = estimate_fuel_penalty(df)
    df = df.copy()

    # Creazione della colonna necessaria per il plot
    df["LapTime_FuelCorrected"] = (
        df["LapTime_Sec"] +
        df["Fuel_Est"] * fuel_penalty
    )

    features = ["TyreLife", "TyreLife2", "TrackTemp"]
    X = df[features]
    y = df["LapTime_FuelCorrected"]

    model = Ridge(alpha=1.0)
    model.fit(X, y)

    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)

    tyre_coef = model.coef_[0]
    tyre2_coef = model.coef_[1]
    avg_life = df["TyreLife"].mean()
    deg_rate = tyre_coef + 2 * tyre2_coef * avg_life

    # AGGIORNAMENTO: Restituiamo anche il df modificato
    return model, r2, deg_rate, fuel_penalty, df