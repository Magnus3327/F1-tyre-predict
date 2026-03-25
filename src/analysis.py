import pandas as pd
from plotter import plot_summary_bar_chart 

def collect_result(results, year, gp, driver, stint, compound, deg_rate, mae):
    """
    Aggiorna la lista dei risultati con le metriche calcolate.
    """
    results.append({
        "Year": year,
        "GP": gp,
        "Driver": driver,
        "Stint": stint,
        "Compound": compound,
        "Degradation": deg_rate,
        "MAE_Sec": mae
    })
    return results

def results_to_dataframe(results):
    return pd.DataFrame(results)

def analyze_summary(df_results, output_folder):
    """
    Stampa un riepilogo testuale ordinato e delega il grafico al plotter.
    """
    if df_results.empty:
        print("⚠️ Nessun dato disponibile per l'analisi.")
        return

    print("\n📊 Riepilogo Degrado Cronologico (Singoli Stint):")
    summary_print = df_results[["Stint", "Compound", "Degradation", "MAE_Sec"]].copy()
    summary_print["Stint"] = summary_print["Stint"].astype(int)
    print(summary_print.to_string(index=False))

    print("\n📊 Media Globale per Mescola (Tutta la gara):")
    agg_summary = df_results.groupby("Compound").agg({
        "Degradation": "mean",
        "Stint": "count"
    }).rename(columns={"Stint": "Num_Stints"}).reset_index()
    print(agg_summary.to_string(index=False))

    plot_summary_bar_chart(df_results, output_folder)