import argparse
import os
from dataCollector import get_driver_data
from preprocessing import clean_data, split_stints
from modelTraining import train_degradation_model
from plotter import save_plots
# AGGIORNAMENTO 1: Importiamo la nuova funzione rinominata
from analysis import collect_result, results_to_dataframe, analyze_summary

def main():
    # Setup degli argomenti da riga di comando per testare gare diverse
    parser = argparse.ArgumentParser(description="Analisi Predittiva Usura Gomme F1")
    parser.add_argument("--year", type=int, required=True, help="Anno della gara")
    parser.add_argument("--gp", type=str, required=True, help="Nome del Gran Premio")
    parser.add_argument("--driver", type=str, required=True, help="Sigla del pilota (es. LEC)")
    args = parser.parse_args()

    # Creazione della cartella per i grafici e i risultati
    output_folder = f"plots/{args.year}_{args.gp}_{args.driver}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Recupero dati telemetrici
    laps_data = get_driver_data(args.year, args.gp, args.driver)
    if laps_data.empty:
        print("❌ Nessun dato trovato. Esco.")
        return

    # Preprocessing e pulizia dei dati
    df_clean = clean_data(laps_data)
    if df_clean.empty:
        print("❌ Nessun giro valido dopo la pulizia.")
        return

    # Suddivisione della gara in stint
    stints = split_stints(df_clean)
    print(f"📈 Trovati {len(stints)} stint validi. Elaborazione in corso...\n")

    results = []

    # Addestramento del modello e generazione dei plot per ogni stint
    for stint, stint_df in stints.items():
        compound = stint_df["Compound"].iloc[0]
        laps_count = len(stint_df)
        print(f"Stint {stint} | compound {compound} | laps {laps_count}")

        try:
            # Training del modello robusto
            model, mae, deg_rate, fuel_penalty, df_pred = train_degradation_model(stint_df)
            
            # Salvataggio dei grafici
            # Salvataggio dei grafici
            save_plots(
                df_pred, model, stint, compound, 
                mae, args.year, args.gp, args.driver, output_folder
            )
            
            # Raccolta dei risultati per l'analisi finale
            results = collect_result(
                results, args.year, args.gp, args.driver, 
                stint, compound, deg_rate, mae
            )
            print(f"   ✅ Stint {stint} completato | Degrado: {deg_rate:.3f} s/lap")
            
        except Exception as e:
            print(f"   ❌ Errore nello Stint {stint}: {e}")

    # Salvataggio del riassunto e generazione del grafico comparativo
    if results:
        results_df = results_to_dataframe(results)
        summary_path = os.path.join(output_folder, "degradation_summary.csv")
        results_df.to_csv(summary_path, index=False)
        print(f"\n📊 Riassunto salvato in: {summary_path}")
        
        # AGGIORNAMENTO 2: Chiamiamo la nuova funzione che stampa il testo e delega il grafico al plotter
        analyze_summary(results_df, output_folder)

if __name__ == "__main__":
    main()