import requests
from datetime import datetime, timedelta
from config import API_KEY, CITIES

def get_weather_data(city):
    try:
        lat, lon = CITIES[city]
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            return {
                "City": city,
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Temperature (°C)": round(data['main']['temp'], 1),
                "Feels Like (°C)": round(data['main']['feels_like'], 1),
                "Humidity (%)": data['main']['humidity'],
                "Pressure (hPa)": data['main']['pressure'],
                "Wind Speed (m/s)": data['wind']['speed'],
                "Condition": data['weather'][0]['main'],
                "Description": data['weather'][0]['description'],
                "Icon": data['weather'][0]['icon']
            }
        return None
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

def get_next_day_weather(city):
    try:
        lat, lon = CITIES[city]
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            # Get tomorrow's date
            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow_date = tomorrow.strftime("%Y-%m-%d")
            
            # Find the forecast for tomorrow
            for item in data['list']:
                if item['dt_txt'].startswith(tomorrow_date):
                    return {
                        "City": city,
                        "Date": item['dt_txt'],
                        "Temperature (°C)": round(item['main']['temp'], 1),
                        "Feels Like (°C)": round(item['main']['feels_like'], 1),
                        "Humidity (%)": item['main']['humidity'],
                        "Pressure (hPa)": item['main']['pressure'],
                        "Wind Speed (m/s)": item['wind']['speed'],
                        "Condition": item['weather'][0]['main'],
                        "Description": item['weather'][0]['description'],
                        "Icon": item['weather'][0]['icon']
                    }
        return None
    except Exception as e:
        print(f"Error fetching next day weather data: {e}")
        return None

def get_weather_icon_url(icon_code):
    return f"http://openweathermap.org/img/wn/{icon_code}@2x.png" 