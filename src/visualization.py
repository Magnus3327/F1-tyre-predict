import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np


def save_plots(df, model, r2, deg_rate, stint_id, compound, driver, output_folder):

    plt.figure(figsize=(12,7))

    plt.scatter(
        df['TyreLife'],
        df['LapTime_Sec'],
        alpha=0.6,
        label="Real Laps"
    )

    # --------------------------
    # trend prediction
    # --------------------------

    tyre_range = np.linspace(
        df['TyreLife'].min(),
        df['TyreLife'].max(),
        50
    )

    avg_temp = df['TrackTemp'].mean()
    avg_fuel = df['Fuel_Est'].mean()
    avg_lap = df['LapNumber'].mean()

    X_plot = pd.DataFrame({
        "TyreLife": tyre_range,
        "TyreLife2": tyre_range**2,
        "TrackTemp": avg_temp,
        "Fuel_Est": avg_fuel,
        "LapNumber": avg_lap
    })

    y_plot = model.predict(X_plot)

    plt.plot(
        tyre_range,
        y_plot,
        linewidth=3,
        label=f"Degradation {deg_rate:.3f} s/lap"
    )

    plt.title(
        f"{driver} | Stint {int(stint_id)} | {compound}\nR² = {r2:.3f}"
    )

    plt.xlabel("Tyre Age (laps)")
    plt.ylabel("Lap Time (s)")

    plt.grid(True)
    plt.legend()

    filename = f"Stint_{int(stint_id)}_{compound}.png"

    path = os.path.join(output_folder, filename)

    plt.savefig(path, dpi=300, bbox_inches="tight")

    plt.close()