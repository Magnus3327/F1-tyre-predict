import pandas as pd
# Importiamo la nuova funzione dal plotter
from plotter import plot_summary_bar_chart 

def collect_result(results, year, gp, driver, stint, compound, deg_rate, r2):
    """
    Aggiorna la lista dei risultati con le metriche calcolate nell'ultimo stint.
    """

    results.append({
        "Year": year,
        "GP": gp,
        "Driver": driver,
        "Stint": stint,
        "Compound": compound,
        "Degradation": deg_rate,
        "R2": r2
    })
    return results

def results_to_dataframe(results):
    """
    Converte i dizionari in un DataFrame strutturato.
    """
    return pd.DataFrame(results)

def analyze_summary(df_results, output_folder):
    """
    Stampa un riepilogo testuale ordinato per stint e delega la creazione
    del grafico al modulo plotter.
    """

    if df_results.empty:
        print("⚠️ Nessun dato disponibile per l'analisi.")
        return

    # Stampa dettagliata stint per stint (Cronologica)
    print("\n📊 Riepilogo Degrado Cronologico (Singoli Stint):")

    # Formattiamo la colonna Stint per non avere i decimali nella stampa
    summary_print = df_results[["Stint", "Compound", "Degradation", "R2"]].copy()
    summary_print["Stint"] = summary_print["Stint"].astype(int)
    print(summary_print.to_string(index=False))

    # Stampa aggregata media per mescola (Opzionale ma utile)
    print("\n📊 Media Globale per Mescola (Tutta la gara):")
    agg_summary = df_results.groupby("Compound").agg({
        "Degradation": "mean",
        "Stint": "count"
    }).rename(columns={"Stint": "Num_Stints"}).reset_index()
    print(agg_summary.to_string(index=False))

    # Deleghiamo il rendering grafico al modulo Plotter
    plot_summary_bar_chart(df_results, output_folder)