import fastf1
import os

def cache_enable():
    """Abilita la cache per FastF1 in una cartella dedicata."""
    # Usiamo un percorso relativo alla radice del progetto per coerenza
    cache_dir = 'cache'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    fastf1.Cache.enable_cache(cache_dir)

def get_race_laps(year, grand_prix, driver_id):
    """
    Scarica i dati, gestisce il mapping del pilota e calcola il carburante stimato.
    """
    print(f"📡 Recupero dati: {year} {grand_prix}...")
    session = fastf1.get_session(year, grand_prix, 'R')
    session.load(telemetry=False, weather=True) 

    # 1. Identificazione Pilota (Mapping Numero -> Sigla)
    # get_driver risolve automaticamente '16' in 'LEC'
    dr_info = session.get_driver(str(driver_id))
    abbr = dr_info['Abbreviation']
    
    # 2. Estrazione giri (usando il metodo aggiornato pick_drivers)
    driver_laps = session.laps.pick_drivers(abbr).copy()
    
    # 3. Integrazione Meteo
    weather_data = driver_laps.get_weather_data()
    driver_laps['TrackTemp'] = weather_data['TrackTemp'].values
    
    # 4. FISICA: Stima Carburante Istante per Istante
    # Partiamo da 110kg (limite max) e scaliamo in base alla lunghezza della gara
    total_race_laps = session.total_laps
    # Fuel cala linearmente ogni giro
    driver_laps['Fuel_Est'] = 110 - (driver_laps['LapNumber'] * (110 / total_race_laps))
    
    print(f"✅ Dati estratti per {abbr}: {len(driver_laps)} giri.")
    
    # Restituiamo il DataFrame e la sigla ufficiale per il sistema di cartelle
    return driver_laps, abbr