import argparse
import os

from dataCollector import get_race_laps
from preprocessing import clean_data
from modelTraining import train_degradation_model
from plotter import save_plots
from analysis import collect_result, results_to_dataframe


def main():
    # -------------------------
    # ARGUMENTS PARSING
    # -------------------------
    parser = argparse.ArgumentParser()

    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--gp", type=str, required=True)
    parser.add_argument("--driver", type=str, required=True)

    args = parser.parse_args()

    # -------------------------
    # OUTPUT FOLDER
    # -------------------------
    output_folder = f"plots/{args.year}_{args.gp}_{args.driver}"
    os.makedirs(output_folder, exist_ok=True)

    # -------------------------
    # DATA COLLECTION
    # -------------------------
    laps, abbr = get_race_laps(args.year, args.gp, args.driver)

    # -------------------------
    # PREPROCESSING
    # -------------------------
    df = clean_data(laps)

    if df.empty:
        print("❌ Nessun dato valido")
        return

    # -------------------------
    # STINT ANALYSIS
    # -------------------------
    results = []
    stints = df["Stint"].unique()

    print(f"📈 Trovati {len(stints)} stint validi. Elaborazione in corso...")

    for stint_id in stints:

        df_stint = df[df["Stint"] == stint_id]
        compound = df_stint["Compound"].iloc[0]

        print(f"Stint {int(stint_id)} | compound {compound} | laps {len(df_stint)}")

        model, r2, deg_rate, fuel_penalty, df_stint_mod = train_degradation_model(df_stint)
        save_plots(df_stint_mod, model, r2, stint_id, compound, output_folder)

        results = collect_result(results, args.year, args.gp, args.driver, stint_id, compound, deg_rate, r2)
        print(f"   ✅ Stint {int(stint_id)} completato | " f"Degrado: {deg_rate:.3f} s/lap" )

    # -------------------------
    # SAVE SUMMARY & ANALYZE
    # -------------------------
    results_df = results_to_dataframe(results)
    summary_path = os.path.join(output_folder, "degradation_summary.csv")
    results_df.to_csv(summary_path, index=False)
    print(f"\n📊 Summary salvato in: {summary_path}")

    # Chiamata alla nuova funzione di analisi
    from analysis import analyze_and_plot_summary
    analyze_and_plot_summary(results_df, output_folder)


if __name__ == "__main__":
    main()