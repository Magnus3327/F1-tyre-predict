import fastf1
import pandas as pd
import os

def test_organico_f1(year, gp, driver_id):
    # 1. Setup rapido cache
    cache_dir = './cache'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    fastf1.Cache.enable_cache(cache_dir)

    # 2. Caricamento sessione
    print(f"Caricamento dati {year} {gp}...")
    session = fastf1.get_session(year, gp, 'R')
    session.load(telemetry=False, weather=False)

    # 3. IDENTIFICAZIONE PILOTA (Mapping Numero -> Sigla)
    # get_driver accetta il numero (es. 16) e restituisce un dizionario
    dr_info = session.get_driver(str(driver_id))
    abbr = dr_info['Abbreviation']
    print(f"\n✅ Pilota identificato: {dr_info['FullName']} [{abbr}] - Team: {dr_info['TeamName']}")

    # 4. SCOPERTA ORGANICA DEI COMPOUND (C1-C5)
    # Esaminiamo i risultati della sessione: FastF1 memorizza qui i set disponibili
    print("\n--- ANALISI MESCOLE PIRELLI DISPONIBILI ---")
    
    # Recuperiamo tutti i giri della gara per vedere i nomi usati
    laps = session.laps.pick_drivers(abbr).copy()
    compounds_in_gara = laps['Compound'].unique()
    
    # Pirelli comunica i compound (C1-C5) tramite i messaggi ufficiali o i metadati
    # Se laps['Compound'] restituisce nomi generici, ecco come "leggerli" 
    # incrociando i dati con la lista dei set di gomme
    for comp in compounds_in_gara:
        # Cerchiamo il primo giro fatto con questa mescola per vedere i dettagli tecnici
        sample_lap = laps[laps['Compound'] == comp].iloc[0]
        # Spesso nelle gare recenti 'Compound' contiene già il valore reale
        print(f"Mescola trovata: {comp}")

    # 5. CALCOLO CARBURANTE ISTANTE PER ISTANTE
    # Ingegneria: 110kg iniziali, consumo basato sul numero di giri totali della gara
    total_race_laps = session.total_laps
    laps['Fuel_Est'] = 110 - (laps['LapNumber'] * (110 / total_race_laps))

    # 6. SOMMARIO DEGLI STINT (Media 1, Hard 1, ecc.)
    print("\n--- STORIA DELLA GARA (STINT PER STINT) ---")
    # Identifichiamo i cambi gomme
    stints = laps[['Stint', 'Compound', 'TyreLife', 'LapNumber', 'Fuel_Est']].drop_duplicates(subset=['Stint'])
    print(stints.to_string(index=False))

    # 7. VISUALIZZAZIONE DATI RAW PER MACHINE LEARNING
    print("\n--- ESEMPIO DATI PRONTI PER IL MODELLO ---")
    # Queste sono le colonne che passerai alla regressione lineare
    cols = ['LapNumber', 'Stint', 'Compound', 'TyreLife', 'Fuel_Est']
    print(laps[cols].head(10).to_string(index=False))

if __name__ == "__main__":
    # Puoi cambiare anno, pista e numero pilota qui
    test_organico_f1(2023, 'Monza', '16')