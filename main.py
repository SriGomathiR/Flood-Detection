# main.py
import argparse
from weather import load_api_key, get_current_weather
from ga import ThresholdGA, GAConfig, classify_risk

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", type=str, required=True, help="City name, e.g., Bengaluru,IN")
    parser.add_argument("--offline", action="store_true", help="Use offline sample JSON")
    args = parser.parse_args()

    # Load OpenWeather API key
    api_key = load_api_key()

    # Fetch current weather
    feats, raw = get_current_weather(args.city, api_key, offline=args.offline)

    # Evolve thresholds using GA for humidity, temperature, and wind
    ga = ThresholdGA(GAConfig())
    best_th = ga.evolve(feats, progress=False)

    # Classify flood risk
    label, frac = classify_risk(feats, best_th)

    # Print report
    print("\n--- Flood Risk Report ---")
    print(f"City         : {args.city}")
    print(f"Temperature  : {feats['temp_c']:.1f} °C")
    print(f"Humidity     : {feats['humidity']:.0f} %")
    print(f"Rainfall     : {feats['rain_1h']:.2f} mm (last 1h)")
    print(f"Wind Speed   : {feats['wind_speed']:.1f} m/s")
    print(f"Cloud Cover  : {feats['clouds_pct']:.0f} %")
    print()
    print(f"Flood Risk   : {label}  (match: {frac*100:.1f}% of rules)")

if __name__ == "__main__":
    main()
