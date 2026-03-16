import pandas as pd


def collect_result(results, year, gp, driver, stint, compound, deg_rate, r2):
    """
        Salva i risultati di ogni stint in un dataframe.
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
    return pd.DataFrame(results)

import pandas as pd
import matplotlib.pyplot as plt
import os

def collect_result(results, year, gp, driver, stint, compound, deg_rate, r2):
    """
    Salva i risultati di ogni stint in una lista di dizionari.
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
    Converte la lista dei risultati in un DataFrame Pandas.
    """
    return pd.DataFrame(results)

def analyze_and_plot_summary(df_results, output_folder):
    """
    Analizza i risultati aggregati e genera un grafico a barre per confrontare 
    il degrado medio tra le diverse mescole. 
    Ideale per l'estrazione di insight per la relazione finale.
    """
    if df_results.empty:
        print("⚠️ Nessun risultato da analizzare.")
        return

    # Raggruppiamo per mescola e calcoliamo la media del degrado e dell'R2
    summary = df_results.groupby("Compound").agg({
        "Degradation": "mean",
        "R2": "mean",
        "Stint": "count" # Conta quanti stint sono stati fatti con questa mescola
    }).rename(columns={"Stint": "Num_Stints"}).reset_index()

    print("\n📊 Sommario Degrado Medio per Mescola:")
    print(summary.to_string(index=False))

    # Creazione del grafico a barre comparativo
    plt.figure(figsize=(8, 5))
    
    # Colori standard F1 per le mescole
    colors = {"SOFT": "red", "MEDIUM": "yellow", "HARD": "white"}
    
    # Mappiamo i colori (usando il grigio come default per mescole anomale es. INTERMEDIATE)
    bar_colors = [colors.get(c.upper(), "gray") for c in summary["Compound"]]

    # Creiamo il grafico a barre
    bars = plt.bar(summary["Compound"], summary["Degradation"], color=bar_colors, edgecolor="black")
    
    plt.title("Confronto Degrado Medio per Mescola\n(Isolato dall'Effetto Carburante)")
    plt.xlabel("Mescola (Compound)")
    plt.ylabel("Degrado Medio (Secondi persi per giro)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Aggiungiamo i valori esatti sopra ogni barra per maggiore chiarezza
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.005, 
                 f"{yval:.3f}s", ha='center', va='bottom', fontweight='bold')

    # Salvataggio del grafico
    plot_path = os.path.join(output_folder, "compound_comparison.png")
    # Impostiamo uno sfondo leggermente grigio per far risaltare la barra bianca della mescola Hard
    plt.savefig(plot_path, dpi=300, facecolor='#f0f0f0') 
    plt.close()
    
    print(f"📈 Grafico comparativo salvato in: {plot_path}")