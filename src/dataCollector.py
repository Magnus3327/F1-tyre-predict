import fastf1
import os

# Abilita la cache per evitare di riscaricare i dati a ogni esecuzione.
if not os.path.exists("cache"):
    os.makedirs("cache")
fastf1.Cache.enable_cache("cache")

def get_driver_data(year, gp, driver):
    """
    Scarica i dati dei giri per un pilota specifico in un determinato GP.
    """
    print(f"🔄 Download dati telemetrici: {year} {gp} - Pilota: {driver}...")
    try:
        session = fastf1.get_session(year, gp, 'R')
        # Download solo telemetria (meteo disabilitato per evitare multicollinearità)
        session.load(telemetry=False, weather=False) 
        
        laps = session.laps.pick_drivers(driver).copy()
        print(f"✅ Dati estratti per {driver}: {len(laps)} giri totali.")
        
        return laps
    
    except Exception as e:
        print(f"❌ Errore nel recupero dati: {e}")
        return None