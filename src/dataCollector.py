import fastf1
import pandas as pd
import os

def get_race_laps(year, grand_prix, driver_id):
    """
        Ottiene i dati dal database di FastF1.
        Salva i dati in una cartella cache, per velocizzare le successive operazioni.

        I dati di interesse sono:
        - Meteo
        - Dati del pilota
        - Dati del circuito
        - Dati della gomma (LapTime, TyreLife, mescola)
        - Dati sui tempi del pilota
    """
    # Abilitiamo la cache internamente se non lo hai fatto nel main
    
    if not os.path.exists("cache"):
        os.makedirs("cache")

    fastf1.Cache.enable_cache("cache")

    session = fastf1.get_session(year, grand_prix, 'R')   # R = Race
    session.load(telemetry=False, weather=True) 
    
    # Risoluzione automatica del pilota (es. da 16 a LEC)
    dr_info = session.get_driver(str(driver_id))
    abbr = dr_info['Abbreviation']
    
    # Recupero i dati del pilota
    driver_laps = session.laps.pick_drivers(abbr).copy()
    
    # Recupero meteo e li allineo con i dati del pilota
    weather_data = driver_laps.get_weather_data()
    # Inseriamo la temperatura assicurandoci che l'indice sia coerente
    driver_laps['TrackTemp'] = weather_data['TrackTemp'].to_list() 
    
    print(f"✅ Dati estratti per {abbr}: {len(driver_laps)} giri")
    return driver_laps, abbr