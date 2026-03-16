import pandas as pd

def clean_data(laps_data):
    """
    Pulisce i dati telemetrici rimuovendo anomalie e giri non validi (SC, pit stop, ecc.).
    Prepara anche le feature necessarie per l'addestramento.
    """

    print("🧹 Inizio preprocessing...")
    if laps_data.empty:
        return pd.DataFrame()

    # Copia per evitare il SettingWithCopyWarning di Pandas
    df_raw = laps_data.copy()

    # Stima del carburante consumato: calcolo fatto sull'intera gara PRIMA dei filtri
    # In F1 si consumano circa 1.8 kg a giro.
    max_lap = df_raw["LapNumber"].max()
    df_raw["Fuel_Est"] = (max_lap - df_raw["LapNumber"]) * 1.8

    # Maschere di filtraggio per tenere solo i giri in condizioni normali da corsa
    is_green_flag = df_raw["TrackStatus"].astype(str).str.contains("1")
    is_not_pitting = df_raw["PitInTime"].isna() & df_raw["PitOutTime"].isna()
    is_warmed_up = df_raw["TyreLife"] > 2
    
    # Applico i filtri
    df = df_raw[is_green_flag & is_not_pitting & is_warmed_up].copy()

    # Converto il tempo sul giro in secondi (float) per darlo in pasto a scikit-learn
    df["LapTime_Sec"] = df["LapTime"].dt.total_seconds()
    
    # Feature engineering: aggiungo il termine quadratico per catturare il crollo prestazionale tipico di fine stint (il "cliff" della gomma)
    df["TyreLife2"] = df["TyreLife"] ** 2

    # Gestisco eventuali valori NaN sulla temperatura della pista con un'interpolazione
    if df["TrackTemp"].isnull().any():
        df["TrackTemp"] = df["TrackTemp"].interpolate(method="linear").bfill()

    # Rimuovo le righe con dati ancora mancanti e i giri palesemente anomali/lenti
    df = df.dropna(subset=["LapTime_Sec", "TyreLife", "TrackTemp", "Compound"])
    
    print(f"✅ Giri utilizzabili per il modello: {len(df)}")
    return df

def split_stints(df):
    """
    Divide il DataFrame principale in un dizionario di stint separati.
    Filtra anche gli stint con troppo pochi dati o giri anomali.
    """

    stints = {}
    for stint, stint_df in df.groupby("Stint"):
        # Filtro base per scartare giri troppo lenti (es. traffico o errori del pilota)
        # l'HuberRegressor penserà poi a gestire i rimanenti outlier, ma voglio evitare di dargli in pasto dati completamente fuori scala.

        fastest = stint_df["LapTime_Sec"].min()
        threshold = fastest * 1.04 
        stint_df = stint_df[stint_df["LapTime_Sec"] <= threshold]

        # Scarto gli stint troppo brevi
        if len(stint_df) < 10:
            print(f"⚠️ Stint {int(stint)} ignorato: solo {len(stint_df)} giri (insufficienti per il ML).")
            continue
            
        stints[stint] = stint_df
    return stints