import pandas as pd

def clean_data(laps_data):
    """
    Esegue il preprocessing avanzato per l'analisi del degrado.
    - Filtra bandiere verdi e rimuove pit-stop.
    - Esclude la fase di warm-up (primi 2 giri di ogni set).
    - Applica un filtro statistico rigoroso contro il traffico (104%).
    - Gestisce la suddivisione per Stint.
    """
    print("🧹 Inizio preprocessing avanzato...")
    
    # 1. Filtro base: Solo giri con pista libera (Bandiera Verde = '1')
    # Rimuoviamo i giri di entrata e uscita dai box (PitInTime/PitOutTime non nulli)
    laps = laps_data[
        (laps_data['TrackStatus'] == '1') & 
        (pd.isnull(laps_data['PitOutTime'])) & 
        (pd.isnull(laps_data['PitInTime']))
    ].copy()
    
    # 2. Trasformazione tempi in secondi (Target variabile)
    laps['LapTime_Sec'] = laps['LapTime'].dt.total_seconds()
    
    # ---------------------------------------------------------
    # LOGICA DI PULIZIA SPECIFICA PER IL DEGRADO
    # ---------------------------------------------------------
    
    # A. Esclusione fase di WARM-UP
    # Scartiamo i primi 2 giri di vita della gomma (TyreLife 1 e 2)
    # in modo da analizzare solo quando la gomma è a temperatura d'esercizio.
    laps = laps[laps['TyreLife'] > 2.0]
    
    # B. Filtro Outlier per Stint (Traffico / Errori)
    # Applichiamo il filtro del 104% su ogni stint separatamente 
    # perché un tempo "lento" nello stint 1 potrebbe essere "veloce" nello stint 3.
    filtered_stints = []
    for stint_id in laps['Stint'].unique():
        stint_df = laps[laps['Stint'] == stint_id].copy()
        
        if not stint_df.empty:
            fastest_stint_lap = stint_df['LapTime_Sec'].min()
            soglia = fastest_stint_lap * 1.04
            stint_df = stint_df[stint_df['LapTime_Sec'] <= soglia]
            filtered_stints.append(stint_df)
    
    if not filtered_stints:
        print("⚠️ Attenzione: Nessun dato rimasto dopo i filtri.")
        return pd.DataFrame()

    # Ricreiamo il dataframe pulito
    df_clean = pd.concat(filtered_stints)
    
    # ---------------------------------------------------------
    
    # 5. Selezione delle feature finali per il modello ML
    # Includiamo Fuel_Est per correggere la pendenza del degrado nel report LaTeX
    features = ['Stint', 'Compound', 'TyreLife', 'TrackTemp', 'Fuel_Est', 'LapTime_Sec']
    df_final = df_clean[features].dropna()
    
    print(f"✅ Preprocessing concluso. Giri pronti per l'analisi: {len(df_final)}")
    return df_final