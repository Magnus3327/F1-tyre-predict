import pandas as pd

def clean_data(laps_data):
    """
    Pulisce i dati telemetrici rimuovendo anomalie e giri non validi. 
    Prepara le feature necessarie per l'addestramento.
    """

    print("🧹 Inizio preprocessing...")
    if laps_data.empty:
        return pd.DataFrame()

    df_raw = laps_data.copy()

    # Stima carburante consumato (circa 1.8 kg a giro)
    max_lap = df_raw["LapNumber"].max()
    df_raw["Fuel_Est"] = (max_lap - df_raw["LapNumber"]) * 1.8

    # Maschere di filtraggio per condizioni da corsa pulite
    is_green_flag = df_raw["TrackStatus"].astype(str).str.contains("1")
    is_not_pitting = df_raw["PitInTime"].isna() & df_raw["PitOutTime"].isna()
    is_warmed_up = df_raw["TyreLife"] > 2
    
    df = df_raw[is_green_flag & is_not_pitting & is_warmed_up].copy()

    # Conversione tempi in secondi
    df["LapTime_Sec"] = df["LapTime"].dt.total_seconds()
    
    # Feature engineering: termine quadratico per il degrado non lineare
    df["TyreLife2"] = df["TyreLife"] ** 2

    # Rimozione righe con valori mancanti
    df = df.dropna(subset=["LapTime_Sec", "TyreLife", "Compound"])
    
    print(f"✅ Giri utilizzabili per il modello: {len(df)}")
    return df

def split_stints(df):
    """
    Divide il DataFrame in stint separati, filtrando quelli troppo brevi o anomali.
    """
    
    stints = {}
    for stint, stint_df in df.groupby("Stint"):
        # Scarto outlier estremi in positivo (es. traffico pesante)
        fastest = stint_df["LapTime_Sec"].min()
        threshold = fastest * 1.04 
        stint_df = stint_df[stint_df["LapTime_Sec"] <= threshold]

        if len(stint_df) < 10:
            print(f"⚠️ Stint {int(stint)} ignorato: <10 giri (insufficienti).")
            continue
            
        stints[stint] = stint_df
    return stints