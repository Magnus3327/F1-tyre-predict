# 🏎️ F1 Tyre Predict

Progetto universitario per l'analisi predittiva del degrado degli pneumatici in Formula 1. 
Il software utilizza i dati telemetrici e cronometrici ufficiali (tramite l'API FastF1) per addestrare modelli di Machine Learning (es. Regressione Robusta di Huber) capaci di isolare il puro consumo della mescola dall'effetto del consumo di carburante e dalle variabili esterne di pista.

---

## 🏗️ Architettura del Progetto

Il flusso di elaborazione (pipeline) è modulare e suddiviso nei seguenti script:

- 📥 **`dataCollector.py`**: Gestisce l'ingestion dei dati tramite FastF1, occupandosi del download della telemetria e della sincronizzazione dei dati meteorologici (es. `TrackTemp`).
- 🧹 **`preprocessing.py`**: Pulisce i dati rimuovendo anomalie (Safety Car, pit-stop, giri lenti) e costruisce le feature polinomiali necessarie al modello.
- 🧠 **`modelTraining.py`**: Implementa il modello ibrido (Fisica + ML) per stimare il reale tasso di degrado della gomma, mitigando il rumore dei dati tramite campionamento stocastico e loss function robuste.
- 📊 **`plotter.py`**: Genera le visualizzazioni grafiche sovrapponendo i dati reali alla linea di tendenza calcolata dall'algoritmo.
- 📈 **`analysis.py`**: Aggrega i risultati degli stint ed estrae insight comparativi tra le diverse mescole.
- 🚀 **`main.py`**: Entrypoint e orchestratore centrale dell'intera esecuzione.

---

## ⚙️ Requisiti

- **Python 3.10+** (si consiglia di mantenere la versione utilizzata durante lo sviluppo del progetto).
- Connessione a Internet attiva (necessaria per il download remoto dei dati FastF1 alla prima esecuzione).

Le dipendenze Python necessarie (tra cui `fastf1`, `pandas`, `scikit-learn`, `matplotlib`, `numpy`) sono elencate all'interno del file `requirements.txt`.

---

## 🛠️ Setup dell'Ambiente

Si raccomanda l'utilizzo di un ambiente virtuale (virtualenv) per evitare conflitti di dipendenze. Esegui i seguenti comandi da terminale nella root del progetto:

'''
   python3 -m venv venv
   
   # Su macOS/Linux:
   source venv/bin/activate
   # Su Windows:
   venv\Scripts\activate

   pip install --upgrade pip
   pip install -r requirements.txt
'''

---

## 🚀 Come lanciare una simulazione

Lo script principale `src/main.py` può essere eseguito da riga di comando passando tre argomenti obbligatori:

- `--year`: Anno del campionato (es. 2024)
- `--gp`: Nome ufficiale del Gran Premio (es. "Italian Grand Prix")
- `--driver`: Sigla o numero del pilota (es. "LEC", "VER", "HAM")

**Esempio di esecuzione:**
python src/main.py --year 2024 --gp "Italian Grand Prix" --driver "LEC"

**Flusso di esecuzione automatico:**
1. Download dei dati della sessione (o lettura rapida dalla cache locale se già scaricati).
2. Pulizia e filtraggio dei giri validi del pilota selezionato.
3. Addestramento del modello predittivo di degrado per ogni stint valido.
4. Generazione automatica dei grafici e salvataggio del report in formato CSV.

---

## 📂 Output del Modello

Alla fine di ogni esecuzione, il sistema creerà automaticamente una cartella specifica per la gara analizzata all'interno della directory `plots/`:

`plots/<year>_<gp>_<driver>/`

All'interno di questa directory troverai:
- **Grafici `.png`**: Curve di degrado modellate dal Machine Learning per ogni singolo stint.
- **`compound_comparison.png`**: Un grafico a barre generato in automatico che confronta il degrado medio registrato tra le diverse mescole (Soft, Medium, Hard).
- **`degradation_summary.csv`**: Un riepilogo tabellare con le metriche estratte (es. R², tasso di degrado in secondi/giro, numero di stint analizzati).

---

## 🚫 Cache e `.gitignore`

Il progetto genera file temporanei e cartelle di supporto che non devono essere tracciati su Git. Il file `.gitignore` è già configurato per escludere:

- `cache/`: Contiene i GB di dati raw scaricati da FastF1.
- `venv/`: L'ambiente virtuale locale.
- `src/__pycache__/`: Bytecode compilato di Python.
- `plots/`: I risultati grafici generati a ogni run.
- File di sistema come `.DS_Store` / `DS_STORE`.
