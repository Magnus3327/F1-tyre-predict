import matplotlib.pyplot as plt
import os

def save_plots(df, model, r2, deg_rate, stint_id, compound, driver_abbr, output_folder):
    """
    Genera e salva i grafici di analisi del degrado per lo stint specifico.
    """
    plt.figure(figsize=(12, 7))
    
    # 1. Plot dei dati reali (Scatter)
    plt.scatter(df['TyreLife'], df['LapTime_Sec'], color='blue', alpha=0.6, label='Dati Reali (Telemetry)')
    
    # 2. Plot della predizione del modello (Trend Line)
    # Per mostrare il trend, usiamo le feature reali dello stint
    # Questo mostrerà come il modello ha "inseguito" i dati
    y_pred = model.predict(df[['TyreLife', 'TrackTemp', 'Fuel_Est']])
    
    # Ordiniamo per TyreLife per evitare zig-zag nel grafico
    sort_idx = df['TyreLife'].argsort()
    plt.plot(df['TyreLife'].iloc[sort_idx], y_pred[sort_idx], color='red', linewidth=2, 
             label=f'Trend ML (Degrado: {deg_rate:.3f} s/lap)')
    
    # 3. Formattazione estetica
    plt.title(f"Analisi Degrado: {driver_abbr} | Stint {int(stint_id)} [{compound}]\n$R^2$ Score: {r2:.3f}", 
              fontsize=14, fontweight='bold')
    plt.xlabel('Età della Gomma (Giri)', fontsize=12)
    plt.ylabel('Tempo sul Giro (Secondi)', fontsize=12)
    
    # Aggiungiamo una griglia tecnica
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper left', frameon=True, shadow=True)
    
    # 4. Salvataggio organizzato
    # Il percorso è già gestito dal main (es. plots/2023_Monza_LEC/)
    filename = f"Stint_{int(stint_id)}_{compound}.png"
    percorso_completo = os.path.join(output_folder, filename)
    
    plt.savefig(percorso_completo, dpi=300, bbox_inches='tight')
    plt.close() # Libera memoria dopo il salvataggio