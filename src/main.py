from dataGathering import get_race_laps
from preprocessing import clean_data
from modelTraining import train_tyre_model
from visualization import save_plots

def main():
    cache_enable()  # Abilita la cache per FastF1

    # 1. Raccolta dati (es. Leclerc a Monza 2023)
    raw_data = get_race_laps(2023, 'Monza', 'LEC')
    
    # 2. Trasformazione
    clean_df = clean_data(raw_data, compound='MEDIUM')
    
    if len(clean_df) > 5:
        # 3. Addestramento
        model, mse, r2 = train_tyre_model(clean_df)
        print(f"Modello addestrato. MSE: {mse:.4f}, R2: {r2:.4f}")
        
        # 4. Visualizzazione
        save_plots(clean_df, model, r2)
    else:
        print("Dati insufficienti per l'addestramento.")

if __name__ == "__main__":
    main()