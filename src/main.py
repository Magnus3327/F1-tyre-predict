import argparse
import os
import sys
from dataGathering import get_race_laps, cache_enable
from preprocessing import clean_data
from modelTraining import train_degradation_model
from visualization import save_plots

def cliManager():
    """Gestisce l'interfaccia a linea di comando (CLI) per l'utente."""
    parser = argparse.ArgumentParser(description='F1 Tyre Degradation Analysis Tool')
    parser.add_argument('--year', type=int, required=True, help='Anno del GP (es. 2023)')
    parser.add_argument('--gp', type=str, required=True, help='Nome del GP (es. Monza)')
    parser.add_argument('--driver', type=str, required=True, help='Numero o Sigla Pilota (es. 16 o LEC)')
    
    return parser.parse_args()

def main():
    # 1. GESTIONE ARGOMENTI (CLI)
    args = cliManager()

    # 2. SETUP AMBIENTE
    cache_enable()
    
    # Definiamo la cartella di output dinamica: plots/2023_Monza_LEC
    # Usiamo os.path.join per garantire compatibilità tra diversi OS
    output_folder = os.path.join('plots', f"{args.year}_{args.gp.replace(' ', '_')}_{args.driver.upper()}")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📁 Creata cartella di output: {output_folder}")

    # 3. PIPELINE DI ANALISI
    print(f"\n🚀 Avvio analisi per {args.driver.upper()} - {args.gp} {args.year}")
    
    try:
        # A. DOWNLOAD DATI
        # get_race_laps dovrà restituire anche la sigla ufficiale (abbr) se inseriamo il numero
        raw_data, abbr = get_race_laps(args.year, args.gp, args.driver)
        
        # B. PREPROCESSING (Pulizia, Warm-up, Outliers)
        clean_df = clean_data(raw_data)
        
        if clean_df.empty:
            print("❌ Errore: Nessun dato valido trovato dopo la pulizia.")
            return

        # C. ANALISI PER STINT
        stints = clean_df['Stint'].unique()
        print(f"📈 Trovati {len(stints)} stint validi. Elaborazione in corso...")

        for stint_id in stints:
            df_stint = clean_df[clean_df['Stint'] == stint_id].copy()
            
            # Filtro minimo per avere una regressione sensata (almeno 5 giri)
            if len(df_stint) >= 5:
                compound = df_stint['Compound'].iloc[0]
                
                # D. TRAINING (Calcolo degrado e coefficienti)
                model, r2, deg_rate, fuel_penalty = train_degradation_model(df_stint)

                print(
                    f"   ✅ Stint {stint_id} ({compound}) completato."
                    f" Degrado: {deg_rate:.3f} s/lap | Fuel penalty: {fuel_penalty:.3f} s/kg"
                    )
                
                # E. VISUALIZZAZIONE
                # Passiamo la cartella specifica a save_plots
                save_plots(df_stint, model, r2, deg_rate, stint_id, compound, abbr, output_folder)

                print(f"Stint {stint_id} | compound {compound} | laps {len(df_stint)}")
                
                print(f"   ✅ Stint {stint_id} ({compound}) completato. Degrado: {deg_rate:.3f} s/lap")
            else:
                print(f"   ⚠️ Stint {stint_id} saltato: troppi pochi giri ({len(df_stint)}).")

        print(f"\n✨ Analisi completata con successo! I grafici sono in: {output_folder}")

    except Exception as e:
        print(f"❌ Errore durante l'esecuzione: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()