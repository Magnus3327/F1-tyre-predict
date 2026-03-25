import argparse
import os
from dataCollector import get_driver_data
from preprocessing import clean_data, split_stints
from modelTraining import train_degradation_model
from plotter import save_plots
from analysis import collect_result, results_to_dataframe, analyze_summary

def main():
    parser = argparse.ArgumentParser(description="Analisi Predittiva Usura Gomme F1")
    parser.add_argument("--year", type=int, required=True, help="Anno della gara")
    parser.add_argument("--gp", type=str, required=True, help="Nome del Gran Premio")
    parser.add_argument("--driver", type=str, required=True, help="Sigla pilota (es. LEC)")
    args = parser.parse_args()

    output_folder = f"plots/{args.year}_{args.gp}_{args.driver}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    laps_data = get_driver_data(args.year, args.gp, args.driver)
    if laps_data is None or laps_data.empty:
        print("❌ Nessun dato trovato. Esco.")
        return

    df_clean = clean_data(laps_data)
    if df_clean.empty:
        print("❌ Nessun giro valido dopo la pulizia.")
        return

    stints = split_stints(df_clean)
    print(f"📈 Trovati {len(stints)} stint validi. Elaborazione in corso...\n")

    results = []

    for stint, stint_df in stints.items():
        compound = stint_df["Compound"].iloc[0]
        print(f"Stint {stint} | compound {compound} | laps {len(stint_df)}")

        try:
            model, mae, deg_rate, _, df_pred = train_degradation_model(stint_df)
            
            save_plots(df_pred, model, stint, compound, mae, args.year, args.gp, args.driver, output_folder)
            
            results = collect_result(results, args.year, args.gp, args.driver, stint, compound, deg_rate, mae)
            print(f"   ✅ Stint {stint} completato | Degrado: {deg_rate:.3f} s/lap")
            
        except Exception as e:
            print(f"   ❌ Errore nello Stint {stint}: {e}")

    if results:
        results_df = results_to_dataframe(results)
        summary_path = os.path.join(output_folder, "degradation_summary.csv")
        results_df.to_csv(summary_path, index=False)
        print(f"\n📊 Riassunto salvato in: {summary_path}")
        
        analyze_summary(results_df, output_folder)

if __name__ == "__main__":
    main()