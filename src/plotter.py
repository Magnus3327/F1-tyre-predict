import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def save_plots(df, model, stint, compound, mae, year, gp, driver, folder):
    """
    Genera e salva i grafici del degrado per visualizzare l'output del modello ML
    sovrapposto ai dati reali della telemetria, includendo contesto ed errore.
    La curva predittiva viene calcolata a temperatura costante per una visualizzazione fluida.
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

    # --- FIX: Generazione di una curva predittiva morbida ---
    # 1. Calcoliamo la temperatura media della pista in questo stint

    # 2. Creiamo 100 punti fittizi lungo la vita della gomma per una curva fluida
    x_smooth = np.linspace(df["TyreLife"].min(), df["TyreLife"].max(), 100)
    
    # 3. Prepariamo l'input per il modello mantenendo la temperatura costante
    df_smooth = pd.DataFrame({
        "TyreLife": x_smooth,
        "TyreLife2": x_smooth ** 2,
    })
    
    # 4. Predizione sulla curva ideale
    y_pred_smooth = model.predict(df_smooth)

    # Plot della nuova linea di tendenza
    plt.plot(
        x_smooth, y_pred_smooth,
        linewidth=3, color="red", label="Trend ML (Temp. Costante)"
    )
    # ---------------------------------------------------------

    plt.xlabel("Vita Gomma (Giri)")
    plt.ylabel("Tempo sul Giro (s)")
    
    # Contestualizzazione forte: GP, Pilota e Anno nel titolo principale
    plt.suptitle(f"{year} {gp} Grand Prix - Pilota: {driver}", fontsize=14, fontweight='bold')
    # Dettagli tecnici nel sottotitolo
    plt.title(f"Stint {int(stint)} | Mescola: {compound} | Errore (MAE): {mae:.3f} s/giro", fontsize=11)
    
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    # Salvataggio (uso bbox_inches='tight' per non tagliare il titolo grande)
    path = os.path.join(folder, f"Stint_{int(stint)}_{compound}.png")
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_summary_bar_chart(df_results, output_folder):
    """
    Genera un grafico a barre che confronta il degrado per ogni singolo stint della gara,
    includendo le informazioni di contesto e l'errore MAE sopra ogni barra.
    """

    if df_results.empty:
        return

    plt.figure(figsize=(10, 6))
    
    # Estrazione metadati dal dataframe per il titolo
    year = df_results["Year"].iloc[0]
    gp = df_results["GP"].iloc[0]
    driver = df_results["Driver"].iloc[0]
    
    # Mappatura completa dei colori classici Pirelli F1
    colors = {
        "SOFT": "red", 
        "MEDIUM": "yellow", 
        "HARD": "white",
        "INTERMEDIATE": "green",
        "WET": "blue"
    }
    
    x_labels = [f"Stint {int(row['Stint'])}\n({row['Compound']})" for _, row in df_results.iterrows()]
    bar_colors = [colors.get(row['Compound'].upper(), "gray") for _, row in df_results.iterrows()]

    bars = plt.bar(
        x_labels, 
        df_results["Degradation"], 
        color=bar_colors, 
        edgecolor="black"
    )
    
    # Titolo contestualizzato
    plt.suptitle(f"Analisi Degrado Gomme: {year} {gp} GP - Pilota: {driver}", fontsize=14, fontweight='bold')
    plt.title("Evoluzione del Degrado per Stint (Isolato dall'Effetto Carburante)", fontsize=11)
    plt.xlabel("Fase di Gara")
    plt.ylabel("Degrado Medio (Secondi/Giro)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Aggiungo i testi con i valori esatti in cima ad ogni barra
    for bar, (_, row) in zip(bars, df_results.iterrows()):
        yval = bar.get_height()
        mae = row['MAE_Sec']
        
        testo = f"{yval:.3f}s\n(MAE: {mae:.2f}s)"
        
        plt.text(
            bar.get_x() + bar.get_width() / 2, 
            yval + 0.002, 
            testo, 
            ha='center', va='bottom', fontweight='bold', fontsize=9
        )

    plt.ylim(0, df_results["Degradation"].max() * 1.2)
    
    plot_path = os.path.join(output_folder, "stint_comparison.png")
    plt.savefig(plot_path, dpi=300, facecolor='#f0f0f0', bbox_inches='tight') 
    plt.close()
    
    print(f"📈 Grafico comparativo salvato in: {plot_path}")