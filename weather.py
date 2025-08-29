import requests

def get_weather_data():
    # Example: replace with your OpenWeatherMap API Key
    API_KEY = "4f6153bc8eff9c3be4e2742cc30f7a48"

    CITY = "Chennai,IN"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    temp = response["main"]["temp"]
    humidity = response["main"]["humidity"]
    rainfall = response.get("rain", {}).get("1h", 0)  
    soil_moisture = 50  # Dummy value (replace with real if available)

    return [temp, humidity, rainfall, soil_moisture]
