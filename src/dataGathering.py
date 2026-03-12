import fastf1
import os

def cache_enable():
    """
    Abilita la cache per FastF1. 
    La cache è essenziale per evitare di scaricare i dati ogni volta, 
    migliorando notevolmente le prestazioni dopo il primo download.
    """

    cache_dir = '../cache'

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        
    fastf1.api.Cache.enable_cache(cache_dir)

def get_race_laps(year, grand_prix, driver_id):
    """
    Scarica e restituisce i dati dei giri e il meteo per un pilota specifico.
    """

    print(f"Downlaod: {year} {grand_prix} - Gara...")
    
    session = fastf1.get_session(year, grand_prix, 'R') #('R' = Race/Gara)
    
    # Caricho i dati della sessione con anche i dati meteo.
    session.load(telemetry=False, weather=True) 

    # Filtro per il pilota specifico
    driver_laps = session.laps.pick_driver(driver_id)
    
    # Aggiungo i dati meteo ai giri del pilota.
    # Questo facilita il lavoro nel file preprocessing.py
    driver_laps = driver_laps.get_weather_data()
    
    print(f"Successo: {len(driver_laps)} giri per {driver_id}.")
    
    return driver_laps