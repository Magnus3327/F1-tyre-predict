import fastf1
import os

def cache_enable():
    """Abilita la cache FastF1."""
    cache_dir = 'cache'
    os.makedirs(cache_dir, exist_ok=True)
    fastf1.Cache.enable_cache(cache_dir)


def get_race_laps(year, grand_prix, driver_id):
    """
    Scarica i dati della gara e aggiunge:
    - temperatura pista
    - fuel stimato
    """

    print(f"📡 Recupero dati: {year} {grand_prix}")

    session = fastf1.get_session(year, grand_prix, 'R')
    session.load(telemetry=False, weather=True)

    dr_info = session.get_driver(str(driver_id))
    abbr = dr_info['Abbreviation']

    driver_laps = session.laps.pick_drivers(abbr).copy()

    # WEATHER
    weather_data = driver_laps.get_weather_data()
    driver_laps['TrackTemp'] = weather_data['TrackTemp'].values

    # -----------------------------------
    # Fuel model migliorato
    # -----------------------------------

    # consumo medio stimato F1
    fuel_per_lap = 1.8

    driver_laps['Fuel_Est'] = 110 - driver_laps['LapNumber'] * fuel_per_lap

    driver_laps['Fuel_Est'] = driver_laps['Fuel_Est'].clip(lower=0)

    print(f"✅ Dati estratti per {abbr}: {len(driver_laps)} giri")

    return driver_laps, abbr