import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def save_plots(df, model, stint, compound, mae, year, gp, driver, outlier_mask, folder):
    """
    Genera e salva i grafici di regressione per singolo stint,
    evidenziando visivamente i giri classificati come outlier dal modello.
    """

    plt.figure(figsize=(10, 6))

    # Dati Grezzi (sfondo grigio per dare contesto sul peso del carburante)
    plt.scatter(df["TyreLife"], df["LapTime_Sec"], color="white", alpha=0.2, label="Dati Grezzi")

    # Dati Puliti: separati tra INLIER (giri buoni) e OUTLIER (giri ignorati)
    inlier_mask = ~outlier_mask

    plt.scatter(
        df["TyreLife"][inlier_mask], df["LapTime_FuelCorrected"][inlier_mask], 
        color="blue", alpha=0.7, label="Dati Validi (Inlier)"
    )
    plt.scatter(
        df["TyreLife"][outlier_mask], df["LapTime_FuelCorrected"][outlier_mask], 
        color="red", marker="x", s=60, alpha=0.8, label="Anomalie Ignorate (Outlier)"
    )

    # Generazione curva ideale
    x_smooth = np.linspace(df["TyreLife"].min(), df["TyreLife"].max(), 100)
    df_smooth = pd.DataFrame({"TyreLife": x_smooth, "TyreLife2": x_smooth ** 2})
    y_pred_smooth = model.predict(df_smooth)

    plt.plot(x_smooth, y_pred_smooth, linewidth=3, color="red", label="Trend ML (Usura Pura)")

    plt.xlabel("Vita Gomma (Giri)")
    plt.ylabel("Tempo sul Giro (s)")
    
    plt.suptitle(f"{year} {gp} Grand Prix - Pilota: {driver}", fontsize=14, fontweight='bold')
    plt.title(f"Stint {int(stint)} | Mescola: {compound} | Errore (MAE): {mae:.3f} s/giro", fontsize=11)
    
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    path = os.path.join(folder, f"Stint_{int(stint)}_{compound}.png")
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_summary_bar_chart(df_results, output_folder):
    """
    Genera un istogramma comparativo dei tassi di degrado estratti.
    """

    if df_results.empty:
        return

    plt.figure(figsize=(10, 6))
    
    year = df_results["Year"].iloc[0]
    gp = df_results["GP"].iloc[0]
    driver = df_results["Driver"].iloc[0]
    
    # Mappa colori per le mescole normalmente usate in F1
    colors = {"SOFT": "red", "MEDIUM": "yellow", "HARD": "white", "INTERMEDIATE": "green", "WET": "blue"}
    
    x_labels = [f"Stint {int(row['Stint'])}\n({row['Compound']})" for _, row in df_results.iterrows()]
    bar_colors = [colors.get(row['Compound'].upper(), "gray") for _, row in df_results.iterrows()]

    bars = plt.bar(x_labels, df_results["Degradation"], color=bar_colors, edgecolor="black")
    
    plt.suptitle(f"Analisi Degrado Gomme: {year} {gp} GP - Pilota: {driver}", fontsize=14, fontweight='bold')
    plt.title("Evoluzione del Degrado per Stint (Isolato dall'Effetto Carburante)", fontsize=11)
    plt.xlabel("Fase di Gara")
    plt.ylabel("Degrado Medio (Secondi/Giro)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar, (_, row) in zip(bars, df_results.iterrows()):
        yval = bar.get_height()
        mae = row['MAE_Sec']
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.002, f"{yval:.3f}s\n(MAE: {mae:.2f}s)", ha='center', va='bottom', fontweight='bold', fontsize=9)

    plt.ylim(0, df_results["Degradation"].max() * 1.2)
    
    plot_path = os.path.join(output_folder, "stint_comparison.png")
    plt.savefig(plot_path, dpi=300, facecolor='#f0f0f0', bbox_inches='tight') 
    plt.close()
    
    print(f"📈 Grafico comparativo salvato in: {plot_path}")