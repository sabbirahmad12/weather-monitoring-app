import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from config import TODAY_WEATHER_FILE, TOMORROW_WEATHER_FILE
import os

def plot_temperature_graph(city):
    try:
        # Get today's data
        today_data = pd.read_excel(TODAY_WEATHER_FILE) if os.path.exists(TODAY_WEATHER_FILE) else pd.DataFrame()
        if not today_data.empty:
            today_data = today_data[today_data['City'] == city]
        
        # Get tomorrow's data
        tomorrow_data = pd.read_excel(TOMORROW_WEATHER_FILE) if os.path.exists(TOMORROW_WEATHER_FILE) else pd.DataFrame()
        if not tomorrow_data.empty:
            tomorrow_data = tomorrow_data[tomorrow_data['City'] == city]
        
        if today_data.empty and tomorrow_data.empty:
            print(f"No data available for {city}")
            return
        
        # Create the plot
        plt.figure(figsize=(12, 6))
        
        # Plot today's data
        if not today_data.empty:
            today_data['Date'] = pd.to_datetime(today_data['Date'])
            plt.plot(today_data['Date'], today_data['Temperature (°C)'], 
                    marker='o', label='Today', color='blue')
        
        # Plot tomorrow's data
        if not tomorrow_data.empty:
            tomorrow_data['Date'] = pd.to_datetime(tomorrow_data['Date'])
            plt.plot(tomorrow_data['Date'], tomorrow_data['Temperature (°C)'], 
                    marker='s', label='Tomorrow', color='red')
        
        # Customize the plot
        plt.title(f'Temperature Trend for {city}')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.grid(True)
        plt.legend()
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Show the plot
        plt.show()
        
    except Exception as e:
        print(f"Error plotting temperature graph: {e}") 