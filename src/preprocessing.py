import pandas as pd

def clean_data(laps_data, compound='MEDIUM'):
    """Pulisce i dati eliminando pit-stop e giri anomali (outlier)."""
    print("Inizio pulizia dati...")
    
    # 1. Teniamo solo i giri con bandiera verde
    laps = laps_data[laps_data['TrackStatus'] == '1'].copy()
    
    # 2. Rimuoviamo i giri di entrata e uscita dai box
    laps = laps[pd.isnull(laps['PitOutTime']) & pd.isnull(laps['PitInTime'])]
    
    # 3. Filtriamo per mescola
    laps = laps[laps['Compound'] == compound].copy()
    
    # 4. Trasformiamo il tempo del giro in secondi (float)
    laps['LapTime_Sec'] = laps['LapTime'].dt.total_seconds()
    
    # ---------------------------------------------------------
    # FIX OUTLIER: Gestione dei giri anomali (Traffico/Warm-up)
    # ---------------------------------------------------------
    # A. Scartiamo sempre il primo giro di vita della gomma (gomme fredde)
    laps = laps[laps['TyreLife'] > 1.0]
    
    # B. Filtro del 104%:
    if not laps.empty: # Controllo di sicurezza per evitare errori se il dataset è vuoto
        fastest_lap = laps['LapTime_Sec'].min()
        soglia = fastest_lap * 1.04
        laps = laps[laps['LapTime_Sec'] <= soglia]
    # ---------------------------------------------------------
    
    # 5. Selezioniamo le colonne fondamentali e rimuoviamo i valori nulli
    df = laps[['TyreLife', 'TrackTemp', 'LapTime_Sec']].dropna()
    
    print(f"Giri validi trovati dopo il filtro outlier: {len(df)}")
    return df