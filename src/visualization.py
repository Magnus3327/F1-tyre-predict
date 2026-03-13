import matplotlib.pyplot as plt
import os

def save_plots(df, model, r2):
    """Crea e salva i grafici dei risultati."""
    plt.figure(figsize=(10, 6))
    
    # Dati reali
    plt.scatter(df['TyreLife'], df['LapTime_Sec'], color='blue', label='Dati Reali')
    
    # Predizione del trend (usando la media della temperatura per la linea)
    X_plot = df[['TyreLife', 'TrackTemp']].sort_values(by='TyreLife')
    y_plot = model.predict(X_plot)
    
    plt.plot(X_plot['TyreLife'], y_plot, color='red', label='Trend di Degrado (ML)')
    
    plt.title(f'Analisi Degrado Gomme (R²: {r2:.2f})')
    plt.xlabel('Età della Gomma (Giri)')
    plt.ylabel('Tempo sul Giro (Secondi)')
    plt.legend()
    plt.grid(True)
    
    plots_dir = 'plots'
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
        
    percorso_file = os.path.join(plots_dir, 'degrado_gomme.png')
    plt.savefig(percorso_file)
    print("Grafico salvato in plots/degrado_gomme.png")