# 🏎️ F1-Tyre-Analysis

Progetto universitario di Ingegneria Informatica per l'analisi predittiva e la stima del degrado degli pneumatici in Formula 1 tramite tecniche di **Physics-Informed Machine Learning**.

Il software utilizza i dati telemetrici ufficiali (tramite l'API `FastF1`) per isolare il puro consumo della mescola dall'effetto del consumo di carburante e dal rumore statistico della pista, fornendo metriche accurate per il supporto alle decisioni strategiche.

---

## 🧠 Metodologia Scientifica

A differenza dei modelli di regressione standard, **F1-Tyre-Analysis** adotta un approccio ibrido per garantire la coerenza fisica dei risultati:

1. **Physics-Informed (PIML):** Il modello integra una conoscenza fisica a priori (penalità deterministica di 0.03s per ogni kg di carburante a bordo) per risolvere il problema della multicollinearità tra l'alleggerimento della vettura e l'usura della gomma.
2. **Regressione Robusta (Huber):** Utilizza una *Huber Loss function* per gestire gli outlier. Questo approccio permette all'algoritmo di ignorare matematicamente i giri anomali (traffico, bloccaggi, errori di guida) senza che questi distorcano la curva di degrado reale.
3. **Validazione MAE:** Il sistema è validato tramite *Mean Absolute Error* (MAE) con K-Fold Cross-Validation dinamica. A differenza dell'R², il MAE offre una valutazione lineare dell'errore espressa direttamente in secondi/giro, garantendo un'interpretazione ingegneristica immediata.

---

## 🏗️ Architettura del Progetto

La pipeline è modulare e suddivisa nei seguenti script:

- 📥 **`dataCollector.py`**: Gestisce l'ingestion dei dati tramite `FastF1`. Ottimizzato per scaricare solo la telemetria necessaria, riducendo l'uso di banda e memoria.
- 🧹 **`preprocessing.py`**: Pulisce i dati rimuovendo anomalie (Safety Car, pit-stop, giri non a regime) e genera le feature polinomiali (`TyreLife`²) per catturare il "cliff" prestazionale.
- 🧠 **`modelTraining.py`**: Il cuore algoritmico. Applica la correzione del carburante e addestra il regressore Huber per estrarre il coefficiente di degrado puro.
- 📊 **`plotter.py`**: Genera visualizzazioni professionali sovrapponendo i dati reali corretti al trend predittivo calcolato.
- 📈 **`analysis.py`**: Aggrega i risultati degli stint, calcola le medie per mescola e genera il riepilogo statistico finale.
- 🚀 **`main.py`**: Entrypoint e orchestratore centrale dell'esecuzione.

---

## ⚙️ Requisiti e Setup

### Prerequisiti
- **Python 3.10+**
- Connessione a Internet (per il primo download dei dati di gara).

### Installazione
Si raccomanda l'uso di un ambiente virtuale:

```
python -m venv venv

# Attivazione (Linux/macOS)
source venv/bin/activate

# Attivazione (Windows) venv\Scripts\activate

pip install -r requirements.txt
```
---

### 🚀 Guida all'Uso
Lo script main.py accetta tre argomenti obbligatori da riga di comando:

```
python src/main.py --year 2024 --gp "Italian Grand Prix" --driver "LEC"
```

### Parametri:
- year: Anno del campionato.
- gp: Nome del Gran Premio (es. "Monaco Grand Prix" o "Italian Grand Prix").
- driver: Sigla del pilota (es. "LEC", "SAI", "VER").

---

### Output e Risultati

I risultati vengono salvati automaticamente nella directory plots/<year>_<gp>_<driver>/:
- Grafici degli Stint (Stint_X_Compound.png) Visualizzazione dei tempi sul giro reali (grigi), i dati corretti dal carburante (blu) e la parabola di degrado stimata dal ML (rossa).
- stint_comparison.png: Istogramma comparativo che mostra il tasso di degrado (s/giro) e l'errore MAE per ogni fase della gara.
- degradation_summary.csv: Tabella esportabile con i coefficienti di degrado e le metriche di errore calcolate per ogni stint.

--- 

### Autore: Matteo Miglio