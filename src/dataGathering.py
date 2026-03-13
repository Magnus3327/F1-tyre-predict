import fastf1
import os

def cache_enable():
    """Abilita la cache per FastF1."""
    cache_dir = '../../cache'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    fastf1.Cache.enable_cache(cache_dir)

def get_race_laps(year, grand_prix, driver_id):
    """Scarica e restituisce i dati dei giri e il meteo per un pilota specifico."""
    print(f"Download: {year} {grand_prix} - Gara...")
    session = fastf1.get_session(year, grand_prix, 'R')
    session.load(telemetry=False, weather=True) 

    # 1. Estraiamo il DataFrame con i dati del pilota (TrackStatus, LapTime, ecc.)
    driver_laps = session.laps.pick_drivers(driver_id).copy()
    
    # 2. Estraiamo il DataFrame separato che contiene solo il meteo
    weather_data = driver_laps.get_weather_data()
    
    # 3. CORREZIONE: Invece di sovrascrivere, aggiungiamo solo la colonna che ci serve!
    # Usiamo .values per assicurarci che i dati si allineino perfettamente riga per riga
    driver_laps['TrackTemp'] = weather_data['TrackTemp'].values
    
    print(f"Successo: {len(driver_laps)} giri per {driver_id}.")
    return driver_laps