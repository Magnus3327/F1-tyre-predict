import pandas as pd

def clean_data(laps_data):
    """
        Pulisce i dati del pilota, rimuovendo i giri non validi.
        Crea le feature necessarie per il modello.
    """

    print("🧹 Inizio preprocessing...")
    if laps_data.empty:
        return pd.DataFrame()

    # Creiamo subito una copia pulita per evitare SettingWithCopyWarning
    df_raw = laps_data.copy()

    # Calcola il carburante sull'intera gara PRIMA dei filtri
    max_lap = df_raw["LapNumber"].max()
    df_raw["Fuel_Est"] = (max_lap - df_raw["LapNumber"]) * 1.8

    # Definiamo i criteri di filtraggio
    is_green_flag = df_raw["TrackStatus"].astype(str).str.contains("1")
    is_not_pitting = df_raw["PitInTime"].isna() & df_raw["PitOutTime"].isna()
    is_warmed_up = df_raw["TyreLife"] > 2

    # Applichiamo i filtri in un colpo solo
    laps = df_raw[is_green_flag & is_not_pitting & is_warmed_up].copy()

    # Ora possiamo usare .loc in sicurezza
    laps.loc[:, "LapTime_Sec"] = laps["LapTime"].dt.total_seconds()

    # Filtro outlier per Stint:
        # 1- Se lo stint ha meno di 3 giri, non lo considero poiché non ci sono abbastanza dati per trainare il modello
        # 2- Non vengono considerati gli outlier che sono più veloci del 4% del tempo più veloce dello stint 
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

    # Feature Engineering
    # TyreLife2 è il quadrato di TyreLife per considerare la curvatura della curva di degrado
    # Fuel_Est è la stima del consumo di carburante per il giro corrente
    # Si assume un consumo di 1.8 kg/lap, per un analisi più accurata bisognerebbe usare i dati di consumo di carburante del pilota
    df.loc[:, "TyreLife2"] = df["TyreLife"] ** 2
    df.loc[:, "Fuel_Est"] = (df["LapNumber"].max() - df["LapNumber"]) * 1.8

    # --- PROTEZIONE CRASH TrackTemp ---
    # Se TrackTemp non è presente, si assume una temperatura di 30°C
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