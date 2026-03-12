import pandas as pd

def clean_data(laps_data, compound='MEDIUM'):
    """Pulisce i dati eliminando pit-stop e giri anomali."""
    print("Inizio pulizia dati...")
    
    # Teniamo solo i giri con bandiera verde
    laps = laps_data.pick_track_status('1')
    
    # Rimuoviamo i giri di entrata e uscita dai box
    laps = laps[pd.isnull(laps['PitOutTime']) & pd.isnull(laps['PitInTime'])]
    
    # Filtriamo per mescola (es. 'SOFT', 'MEDIUM', 'HARD', 'INTERMEDIATE', 'WET')
    laps = laps[laps['Compound'] == compound].copy()
    
    # Trasformiamo il tempo del giro in secondi (float)
    laps['LapTime_Sec'] = laps['LapTime'].dt.total_seconds()
    
    # Selezioniamo le colonne fondamentali
    df = laps[['TyreLife', 'TrackTemp', 'LapTime_Sec']].dropna()
    
    print(f"Giri validi trovati: {len(df)}")
    return df