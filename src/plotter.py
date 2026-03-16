import matplotlib.pyplot as plt

def save_plots(df, model, r2, stint, compound, folder):
    """
    Genera e salva i grafici del degrado per visualizzare l'output del modello ML
    sovrapposto ai dati reali della telemetria.
    """

    plt.figure(figsize=(10, 6))

    # Plot dei dati grezzi (in grigio, per far vedere l'effetto reale)
    plt.scatter(
        df["TyreLife"], df["LapTime_Sec"],
        color="gray", alpha=0.3, label="Dati Grezzi (Con Carburante)"
    )

    # Plot dei dati puliti dal peso del carburante (il target del modello)
    plt.scatter(
        df["TyreLife"], df["LapTime_FuelCorrected"],
        color="blue", alpha=0.7, label="Dati Corretti (Solo Degrado)"
    )

    # Calcolo della linea di tendenza del modello ML
    df_sorted = df.sort_values("TyreLife")
    y_pred = model.predict(df_sorted[["TyreLife", "TyreLife2", "TrackTemp"]])

    plt.plot(
        df_sorted["TyreLife"], y_pred,
        linewidth=3, color="red", label="Trend Predittivo (ML)"
    )

    plt.xlabel("Vita Gomma (Giri)")
    plt.ylabel("Tempo sul Giro (s)")
    plt.title(f"Stint {int(stint)} | Mescola {compound} | Test R2 = {r2:.3f}")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    # Salvataggio
    path = f"{folder}/Stint_{int(stint)}_{compound}.png"
    plt.savefig(path, dpi=300)
    plt.close()