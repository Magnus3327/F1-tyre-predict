import fastf1
import os

# Abilito la cache per evitare di riscaricare GB di dati a ogni esecuzione.
if not os.path.exists("cache"):
    os.makedirs("cache")
fastf1.Cache.enable_cache("cache")

def get_driver_data(year, gp, driver):
    """
    Scarica i dati dei giri per un pilota specifico in un determinato GP usando l'API FastF1,
    e unisce i dati meteorologici (TrackTemp) sincronizzandoli con i giri.
    """

    print(f"🔄 Scaricamento dati: {year} {gp} - Pilota: {driver}...")
    try:
        session = fastf1.get_session(year, gp, 'R') # 'R' indica la gara
        session.load(telemetry=False, weather=True) 
        
        # Estraggo i giri del pilota
        laps = session.laps.pick_drivers(driver).copy() # Copia per evitare problemi di riferimento con FastF1
        
        print("🌤️ Sincronizzazione dati meteo (TrackTemp)...")
        weather_data = laps.get_weather_data()

        laps['TrackTemp'] = weather_data['TrackTemp'].values

        print(f"✅ Dati estratti per {driver}: {len(laps)} giri totali.")
        return laps
    
    except Exception as e:
        print(f"❌ Errore nel recupero dati: {e}")
        return None