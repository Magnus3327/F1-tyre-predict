import pandas as pd

def clean_data(laps_data):
    print("🧹 Inizio preprocessing...")
    if laps_data.empty:
        return pd.DataFrame()

    # Creiamo subito una copia pulita per evitare SettingWithCopyWarning
    df_raw = laps_data.copy()

    # 1. Definiamo i criteri di filtraggio
    is_green_flag = df_raw["TrackStatus"].astype(str).str.contains("1")
    is_not_pitting = df_raw["PitInTime"].isna() & df_raw["PitOutTime"].isna()
    is_warmed_up = df_raw["TyreLife"] > 2

    # Applichiamo i filtri in un colpo solo
    laps = df_raw[is_green_flag & is_not_pitting & is_warmed_up].copy()

    # Ora possiamo usare .loc in sicurezza
    laps.loc[:, "LapTime_Sec"] = laps["LapTime"].dt.total_seconds()

    # 2. Filtro outlier per Stint
    filtered = []
    for stint in laps["Stint"].unique():
        stint_df = laps[laps["Stint"] == stint].copy()
        if len(stint_df) < 3:
            continue
        
        fastest = stint_df["LapTime_Sec"].min()
        threshold = fastest * 1.04
        stint_df = stint_df[stint_df["LapTime_Sec"] <= threshold]
        filtered.append(stint_df)

    if not filtered:
        print("⚠️ Nessun dato rimasto dopo i filtri!")
        return pd.DataFrame()

    df = pd.concat(filtered).copy()

    # 3. Feature Engineering
    df.loc[:, "TyreLife2"] = df["TyreLife"] ** 2
    df.loc[:, "Fuel_Est"] = (df["LapNumber"].max() - df["LapNumber"]) * 1.8

    # --- PROTEZIONE CRASH TrackTemp ---
    if "TrackTemp" not in df.columns:
        df["TrackTemp"] = 30.0
    
    # 4. Selezione finale
    features = [
        "Stint", "Compound", "TyreLife", "TyreLife2", 
        "TrackTemp", "Fuel_Est", "LapNumber", "LapTime_Sec"
    ]
    
    df = df[features].dropna(subset=["LapTime_Sec"]).ffill().bfill() 

    print(f"✅ Giri utilizzabili per il modello: {len(df)}")
    return df