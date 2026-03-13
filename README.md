## F1 Tyre Predict

Progetto universitario per analizzare il degrado gomma in Formula 1 usando dati ufficiali cronometrici (FastF1) e modelli di machine learning.

Il flusso principale:

- **Raccolta dati** (`dataCollector.py`): scarica i dati del GP selezionato tramite FastF1.
- **Preprocessing** (`preprocessing.py`): pulisce i dati e costruisce le feature giro per giro.
- **Training modello** (`modelTraining.py`): stima il degrado gomma e altre metriche di performance.
- **Plot e salvataggio** (`plotter.py`): genera i grafici per ogni stint.
- **Analisi risultati** (`analysis.py`): costruisce un riepilogo in forma tabellare.
- **Entrypoint** (`main.py`): orchestration completa di una run.

---

## Requisiti

- Python 3.10+ (consigliato usare la stessa versione usata nel corso / nel progetto)
- Connessione internet (FastF1 scarica i dati da remoto alla prima esecuzione)

Le dipendenze Python sono elencate in `requirements.txt` (FastF1, pandas, scikit-learn, matplotlib, numpy, ecc.).

---

## Setup ambiente (virtualenv)

Da terminale, nella root del progetto:

```bash
cd "/Users/matteo/Università/UNI2026/IA/Progetto/F1_tyre_predict"

# Creazione (una sola volta)
python3 -m venv venv

# Attivazione (ogni nuova sessione)
source venv/bin/activate

# Installazione dipendenze
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Come lanciare una run

Lo script principale è `src/main.py` e richiede tre argomenti:

- `--year`: anno del campionato (es. `2024`)
- `--gp`: nome ufficiale del Gran Premio (es. `"Italian Grand Prix"`)
- `--driver`: sigla del pilota (es. `"LEC"`, `"VER"`, `"HAM"`, ecc.)

Esempio:

```bash
source venv/bin/activate
python src/main.py --year 2024 --gp "Italian Grand Prix" --driver "LEC"
```

Cosa succede:

- vengono scaricati (o letti da cache) i dati del GP selezionato,
- vengono filtrati e puliti i giri del pilota scelto,
- per ogni stint viene allenato un modello di degrado,
- vengono generati grafici e un file di riepilogo CSV.

---

## Output del modello

Per ogni run viene creata una cartella dentro `plots/` con nome:

```text
plots/<year>_<gp>_<driver>/
```

All’interno troverai:

- grafici `.png` del degrado per ogni stint,
- il file `degradation_summary.csv` con un riepilogo numerico (es. R², tasso di degrado, compound, ecc.).

Esempio (già testato):

- `plots/2024_Italian Grand Prix_LEC/degradation_summary.csv`

---

## Cache e `.gitignore`

Per evitare di inquinare la repo con file generati:

- la cache di FastF1 è salvata nella cartella `cache/`,
- l’ambiente virtuale è in `venv/`,
- i bytecode Python vanno in `src/__pycache__/`,
- i risultati dei modelli vengono salvati in `plots/`.

Il file `.gitignore` è configurato per ignorare:

- `cache/`
- `venv/`
- `src/__pycache__/`
- `.DS_Store` / `DS_STORE` alla radice
