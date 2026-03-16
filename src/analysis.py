import pandas as pd
import matplotlib.pyplot as plt
import os

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

def analyze_and_plot_summary(df_results, output_folder):
    """
    Calcola le medie raggruppate per mescola e genera un grafico a barre.
    """

    if df_results.empty:
        print("⚠️ Nessun dato disponibile per l'analisi.")
        return

    # Aggrego i dati per mescola per ottenere i valori medi del GP
    summary = df_results.groupby("Compound").agg({
        "Degradation": "mean",
        "R2": "mean",
        "Stint": "count"
    }).rename(columns={"Stint": "Num_Stints"}).reset_index()

    print("\n📊 Sommario Degrado Medio per Mescola:")
    print(summary.to_string(index=False))

    # Setup del grafico a barre
    plt.figure(figsize=(8, 5))
    
    # Mappatura completa dei colori classici Pirelli F1
    colors = {
        "SOFT": "red", 
        "MEDIUM": "yellow", 
        "HARD": "white",
        "INTERMEDIATE": "green",
        "WET": "blue"
    }
    
    # Mappiamo i colori (usando il grigio come fallback di sicurezza solo per errori/test)
    bar_colors = [colors.get(c.upper(), "gray") for c in summary["Compound"]]

    bars = plt.bar(
        summary["Compound"], 
        summary["Degradation"], 
        color=bar_colors, 
        edgecolor="black"
    )
    
    plt.title("Confronto Degrado Medio per Mescola\n(Isolato dall'Effetto Carburante)")
    plt.xlabel("Mescola (Compound)")
    plt.ylabel("Degrado Medio (Secondi/Giro)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Aggiungo i testi con i valori esatti in cima ad ogni barra
    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2, 
            yval + 0.005, 
            f"{yval:.3f}s", 
            ha='center', va='bottom', fontweight='bold'
        )

    # Imposto uno sfondo grigio chiaro per non far "sparire" la barra della mescola Hard (bianca)
    plot_path = os.path.join(output_folder, "compound_comparison.png")
    plt.savefig(plot_path, dpi=300, facecolor='#f0f0f0') 
    plt.close()
    
    print(f"📈 Grafico comparativo salvato in: {plot_path}")