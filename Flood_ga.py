import random
import requests

# ---------- CONFIG ----------
API_KEY = "4f6153bc8eff9c3be4e2742cc30f7a48"  # 🔑 Replace with your OpenWeatherMap API key
POP_SIZE = 20
GENS = 50
MUT_RATE = 0.2

# ---------- Flood Risk Levels ----------
def classify_risk(score):
    if score < 80:
        return "Low Flood Risk 🌤️"
    elif score < 150:
        return "Medium Flood Risk ⚡"
    else:
        return "High Flood Risk 🌊"

# ---------- Fitness Function ----------
def fitness(weights, features):
    # Weighted sum of features
    return sum(w * f for w, f in zip(weights, features))

# ---------- GA Functions ----------
def create_individual():
    return [random.uniform(0, 1) for _ in range(4)]

def mutate(ind):
    i = random.randint(0, len(ind) - 1)
    ind[i] = random.uniform(0, 1)
    return ind

def crossover(p1, p2):
    point = random.randint(1, len(p1) - 1)
    return p1[:point] + p2[point:]

def genetic_algorithm(features):
    population = [create_individual() for _ in range(POP_SIZE)]
    
    for _ in range(GENS):
        scored = [(fitness(ind, features), ind) for ind in population]
        scored.sort(reverse=True)  # maximize fitness
        population = [ind for _, ind in scored[:POP_SIZE//2]]
        
        # Next generation
        children = []
        while len(children) < POP_SIZE:
            p1, p2 = random.sample(population, 2)
            child = crossover(p1, p2)
            if random.random() < MUT_RATE:
                child = mutate(child)
            children.append(child)
        population = children
    
    best_score, best_weights = max([(fitness(ind, features), ind) for ind in population], key=lambda x: x[0])
    return best_weights, best_score

# ---------- Get Weather Data ----------
def get_weather(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    r = requests.get(url).json()
    
    temp = r["main"]["temp"]
    humidity = r["main"]["humidity"]
    rainfall = r.get("rain", {}).get("1h", 0)  # rainfall (last 1h)
    
    # Soil moisture not in API → simulate (30–80 range)
    soil_moisture = random.randint(30, 80)
    
    return [temp, humidity, rainfall, soil_moisture]

# ---------- Main Run ----------
if __name__ == "__main__":
    location = input("Enter location (city name): ")
    
    try:
        features = get_weather(location)
        print(f"\n🌍 Weather API gave: {features} → [Temp, Humidity, Rainfall, Soil Moisture]")
        
        best_weights, best_score = genetic_algorithm(features)
        
        print(f"\n✅ GA ran and evolved weights → {best_weights}")
        print(f"✅ Best fitness score → {best_score:.2f}")
        print(f"✅ Flood Risk calculated → {classify_risk(best_score)}")
    
    except Exception as e:
        print("⚠️ Error fetching weather:", e)
