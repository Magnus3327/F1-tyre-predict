import fastf1
import pandas as pd

def get_driver_laps(year, gp, driver):

    fastf1.Cache.enable_cache("cache")

    session = fastf1.get_session(year, gp, "R")
    session.load()

    laps = session.laps.pick_driver(driver)

    print(f"✅ Dati estratti per {driver}: {len(laps)} giri")

    return laps

def get_race_laps(year, grand_prix, driver_id):
    """Scarica i dati e unisce il meteo ai giri del pilota."""
    # Abilitiamo la cache internamente se non lo hai fatto nel main
    fastf1.Cache.enable_cache("cache")
    
    session = fastf1.get_session(year, grand_prix, 'R')
    session.load(telemetry=False, weather=True) 
    
    # Risoluzione automatica del pilota (es. da 16 a LEC)
    dr_info = session.get_driver(str(driver_id))
    abbr = dr_info['Abbreviation']
    
    driver_laps = session.laps.pick_drivers(abbr).copy()
    
    # Recupero meteo e allineamento dati
    weather_data = driver_laps.get_weather_data()
    # Inseriamo la temperatura assicurandoci che l'indice sia coerente
    driver_laps['TrackTemp'] = weather_data['TrackTemp'].to_list() 
    
    print(f"✅ Dati estratti per {abbr}: {len(driver_laps)} giri")
    return driver_laps, abbr