import matplotlib.pyplot as plt

def save_plots(df, model, r2, stint, compound, folder):
    """
    Salva i grafici del degrado della gomma per ogni stint.
    """
    plt.figure(figsize=(10, 6))

    # 1. Dati grezzi (in grigio per mostrare il rumore e l'effetto carburante)
    plt.scatter(
        df["TyreLife"], df["LapTime_Sec"],
        color="gray", alpha=0.3, label="Dati Grezzi (Con Carburante)"
    )

    # 2. Dati corretti dal modello (in blu - solo degrado puro)
    plt.scatter(
        df["TyreLife"], df["LapTime_FuelCorrected"],
        color="blue", alpha=0.7, label="Dati Corretti (Senza Carburante)"
    )

    # 3. Linea di tendenza (Trend ML)
    df_sorted = df.sort_values("TyreLife")
    
    # Passiamo tutte e 4 le feature al modello per ottenere la linea di previsione accurata
    y_pred = model.predict(df_sorted[["TyreLife", "TyreLife2", "TrackTemp", "Fuel_Est"]])

    plt.plot(
        df_sorted["TyreLife"], y_pred,
        linewidth=3, color="red", label="Modello ML (Degrado)"
    )

    plt.xlabel("Vita Gomma (giri)")
    plt.ylabel("Tempo sul Giro (s)")
    # Nota: l'R2 ora riflette l'accuratezza predittiva sui dati di test!
    plt.title(f"Stint {stint} | {compound} | Test R2={r2:.3f}")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    path = f"{folder}/Stint_{int(stint)}_{compound}.png"
    plt.savefig(path, dpi=300)
    plt.close()