import matplotlib.pyplot as plt
import os

def save_plots(df, model, stint, compound, folder):
    """
    Genera e salva i grafici del degrado per visualizzare l'output del modello ML
    sovrapposto ai dati reali della telemetria.
    """

    plt.figure(figsize=(10, 6))

    # Plot dei dati grezzi
    plt.scatter(
        df["TyreLife"], df["LapTime_Sec"],
        color="gray", alpha=0.3, label="Dati Grezzi (Con Carburante)"
    )

    # Plot dei dati puliti dal peso del carburante
    plt.scatter(
        df["TyreLife"], df["LapTime_FuelCorrected"],
        color="blue", alpha=0.7, label="Dati Corretti (Solo Degrado)"
    )

    # Linea di tendenza del modello ML
    df_sorted = df.sort_values("TyreLife")
    y_pred = model.predict(df_sorted[["TyreLife", "TyreLife2", "TrackTemp"]])

    plt.plot(
        df_sorted["TyreLife"], y_pred,
        linewidth=3, color="red", label="Trend Predittivo (ML)"
    )

    plt.xlabel("Vita Gomma (Giri)")
    plt.ylabel("Tempo sul Giro (s)")
    plt.title(f"Stint {int(stint)} | Mescola {compound}")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    # Salvataggio
    path = os.path.join(folder, f"Stint_{int(stint)}_{compound}.png")
    plt.savefig(path, dpi=300)
    plt.close()


def plot_summary_bar_chart(df_results, output_folder):
    """
    Genera un grafico a barre che confronta il degrado per ogni singolo stint della gara in ordine cronologico.
    """

    if df_results.empty:
        return

    plt.figure(figsize=(10, 6))
    
    # Mappatura completa dei colori classici Pirelli F1
    colors = {
        "SOFT": "red", 
        "MEDIUM": "yellow", 
        "HARD": "white",
        "INTERMEDIATE": "green",
        "WET": "blue"
    }
    
    # Creiamo etichette uniche per l'asse X (es. "Stint 1\n(MEDIUM)")
    x_labels = [f"Stint {int(row['Stint'])}\n({row['Compound']})" for _, row in df_results.iterrows()]
    
    # Mappiamo i colori riga per riga basandoci sulla mescola di quello stint
    bar_colors = [colors.get(row['Compound'].upper(), "gray") for _, row in df_results.iterrows()]

    bars = plt.bar(
        x_labels, 
        df_results["Degradation"], 
        color=bar_colors, 
        edgecolor="black"
    )
    
    plt.title("Evoluzione del Degrado Gomma per Stint\n(Isolato dall'Effetto Carburante)")
    plt.xlabel("Fase di Gara")
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

    # Sfondo grigio chiaro per far risaltare la barra bianca (HARD)
    plot_path = os.path.join(output_folder, "stint_comparison.png")
    plt.savefig(plot_path, dpi=300, facecolor='#f0f0f0') 
    plt.close()
    
    print(f"📈 Grafico comparativo salvato in: {plot_path}")