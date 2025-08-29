import pandas as pd
from ga import GeneticAlgorithm
from weather import get_weather_data

def classify_risk(score):
    if score > 200:
        return "High Flood Risk ⚠️"
    elif score > 100:
        return "Medium Flood Risk ⚡"
    else:
        return "Low Flood Risk ✅"

def main():
    # Load dataset
    dataset = pd.read_csv("Merged_Flood_Prediction.csv", low_memory=False)


    # Get live weather
    weather_data = get_weather_data()
    print(f"\n Weather API gave: "
      f"[{weather_data[0]} (temp), {weather_data[1]} (humidity), "
      f"{weather_data[2]} (rainfall), {weather_data[3]} (soil moisture)]")

    # Run GA
    ga = GeneticAlgorithm(
        population_size=10,
        generations=20,
        mutation_rate=0.1,
        dataset=dataset
    )
    best_solution, best_score = ga.run(weather_data)

    print("\n Best Solution (weights):", best_solution)
    print("Best Score:", best_score)
    print("Flood Risk Level:", classify_risk(best_score))

if __name__ == "__main__":
    main()
