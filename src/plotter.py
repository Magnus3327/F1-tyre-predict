import matplotlib.pyplot as plt

def save_plots(df, model, r2, stint, compound, folder):
    plt.figure(figsize=(10, 6))

    # 1. Punti Originali (in grigio/trasparente per mostrare il rumore)
    plt.scatter(
        df["TyreLife"],
        df["LapTime_Sec"],
        color="gray", alpha=0.3, label="Raw Data (With Fuel)"
    )

    # 2. Punti Corretti dal Modello (in blu - la tua base di training)
    plt.scatter(
        df["TyreLife"],
        df["LapTime_FuelCorrected"],
        color="blue", alpha=0.7, label="Fuel Corrected Data"
    )

    # 3. Linea di Trend (Trend ML)
    df_sorted = df.sort_values("TyreLife")
    y_pred = model.predict(df_sorted[["TyreLife", "TyreLife2", "TrackTemp"]])

    plt.plot(
        df_sorted["TyreLife"],
        y_pred,
        linewidth=3, color="red", label="ML Degradation Model"
    )

    plt.xlabel("Tyre Life (laps)")
    plt.ylabel("Lap Time (s)")
    plt.title(f"Stint {stint} | {compound} | R2={r2:.3f}")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    path = f"{folder}/Stint_{stint}_{compound}_Advanced.png"
    plt.savefig(path, dpi=300)
    plt.close()