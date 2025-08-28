# AgriFloodGen — GA + OpenWeather (50% Demo Ready)

This starter project lets you **fetch real weather data** from OpenWeather and run a **Genetic Algorithm (GA)** to evolve flood-risk thresholds. It also supports **offline mode** with a sample JSON, so you can demo without internet/API key.

## ✅ What you can show this week (50% demo)
- Live console output of **Soil Moisture/Water Level style** values (here: weather-based features).
- A GA **evolving thresholds** and printing **best thresholds + risk level**.
- **Logs saved** to `runs/summary.csv`.

---

## 1) Install Python (if needed)
Check your Python version:
```bash
python --version
# or
python3 --version
```

## 2) Create & Activate Virtual Env
```bash
cd AgriFloodGen-GA
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

## 3) Install dependencies
```bash
pip install -r requirements.txt
```

## 4) Set up your API key
- Create a (free) OpenWeather account and copy your API key.
- Create a file named `.env` in this folder with this content (replace the key):
```
OPENWEATHER_API_KEY=YOUR_KEY_HERE
```

## 5) Run in **online mode** (real API)
```bash
python main.py --city "Chennai,IN"
```
You should see current weather features, GA evolution progress, and final thresholds + risk.

## 6) Run in **offline mode** (no internet needed)
```bash
python main.py --city "Chennai,IN" --offline
```
This uses `sample_data/current_sample.json` bundled here for a guaranteed demo.

---

## Output & Logs
- JSON run logs: `runs/run_YYYYMMDD_HHMMSS.json`
- Summary CSV (appends each run): `runs/summary.csv`

## Next steps (after demo)
- Replace thresholds-based GA with a dataset-driven fitness (historical flood labels).
- Integrate ESP32 readings over Serial/WiFi and feed into the Python classifier.
