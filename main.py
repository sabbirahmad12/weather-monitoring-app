import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
from weather_utils import get_weather_data, get_next_day_weather, get_weather_icon_url
from excel_handler import save_data_to_excel, clear_excel_data, get_latest_data
from graph_plotter import plot_temperature_graph
from config import CITIES, REFRESH_INTERVAL
from theme import Theme
import matplotlib.pyplot as plt
import pandas as pd

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Monitoring System")
        self.root.geometry("1000x750")
        self.root.minsize(1000, 750)
        
        # Apply theme
        self.theme = Theme.apply_theme(root, 'BLUE')
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # City selection
        self.city_var = tk.StringVar()
        self.create_city_selection()
        
        # Weather display frame
        self.weather_frame = ttk.LabelFrame(self.main_frame, text="Weather Forecast", padding="10")
        self.weather_frame.pack(fill=tk.X, pady=10)
        
        # Create frames for current and next day weather
        self.current_frame = ttk.LabelFrame(self.weather_frame, text="Today's Weather", padding="10")
        self.current_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        
        self.next_day_frame = ttk.LabelFrame(self.weather_frame, text="Tomorrow's Weather", padding="10")
        self.next_day_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)
        
        # Create weather displays for both frames
        self.create_weather_display(self.current_frame, is_current=True)
        self.create_weather_display(self.next_day_frame, is_current=False)
        
        # Buttons frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        # Create buttons
        self.create_buttons()
        
        # Status bar
        self.status_var = tk.StringVar(value="Select a city to view weather data")
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var)
        self.status_bar.pack(fill=tk.X, pady=5)
        
        # Initialize with default values
        self.initialize_default_values()
    
    def create_city_selection(self):
        city_frame = ttk.Frame(self.main_frame)
        city_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(city_frame, text="Select City:", font=Theme.FONTS['subtitle']).pack(side=tk.LEFT, padx=5)
        city_combo = ttk.Combobox(city_frame, textvariable=self.city_var, values=list(CITIES.keys()), 
                                 state="readonly", font=Theme.FONTS['normal'])
        city_combo.pack(side=tk.LEFT, padx=5)
        city_combo.bind('<<ComboboxSelected>>', lambda e: self.fetch_weather())
    
    def create_weather_display(self, parent_frame, is_current):
        # Center frame for icon and condition
        center_frame = ttk.Frame(parent_frame)
        center_frame.pack(expand=True)
        
        # Weather icon
        icon_label = ttk.Label(center_frame)
        icon_label.pack(pady=5)
        
        # Weather condition with color
        condition_label = ttk.Label(center_frame, text="--", font=Theme.FONTS['title'])
        condition_label.pack(pady=2)
        
        description_label = ttk.Label(center_frame, text="--", font=Theme.FONTS['normal'])
        description_label.pack(pady=2)
        
        # Weather details
        details_frame = ttk.Frame(parent_frame)
        details_frame.pack(fill=tk.X, pady=5)
        
        # Create weather detail labels
        self.create_weather_labels(details_frame, is_current)
        
        # Store references to labels
        if is_current:
            self.current_icon = icon_label
            self.current_condition = condition_label
            self.current_description = description_label
        else:
            self.next_icon = icon_label
            self.next_condition = condition_label
            self.next_description = description_label
    
    def create_weather_labels(self, parent_frame, is_current):
        # Temperature
        ttk.Label(parent_frame, text="Temperature:", font=Theme.FONTS['small']).pack(anchor=tk.W)
        temp_label = ttk.Label(parent_frame, text="--", font=Theme.FONTS['normal'])
        temp_label.pack(anchor=tk.W)
        
        # Feels Like
        ttk.Label(parent_frame, text="Feels Like:", font=Theme.FONTS['small']).pack(anchor=tk.W)
        feels_label = ttk.Label(parent_frame, text="--", font=Theme.FONTS['normal'])
        feels_label.pack(anchor=tk.W)
        
        # Humidity
        ttk.Label(parent_frame, text="Humidity:", font=Theme.FONTS['small']).pack(anchor=tk.W)
        humidity_label = ttk.Label(parent_frame, text="--", font=Theme.FONTS['normal'])
        humidity_label.pack(anchor=tk.W)
        
        # Pressure
        ttk.Label(parent_frame, text="Pressure:", font=Theme.FONTS['small']).pack(anchor=tk.W)
        pressure_label = ttk.Label(parent_frame, text="--", font=Theme.FONTS['normal'])
        pressure_label.pack(anchor=tk.W)
        
        # Wind Speed
        ttk.Label(parent_frame, text="Wind Speed:", font=Theme.FONTS['small']).pack(anchor=tk.W)
        wind_label = ttk.Label(parent_frame, text="--", font=Theme.FONTS['normal'])
        wind_label.pack(anchor=tk.W)
        
        # Store references to labels
        if is_current:
            self.current_temp = temp_label
            self.current_feels = feels_label
            self.current_humidity = humidity_label
            self.current_pressure = pressure_label
            self.current_wind = wind_label
        else:
            self.next_temp = temp_label
            self.next_feels = feels_label
            self.next_humidity = humidity_label
            self.next_pressure = pressure_label
            self.next_wind = wind_label
    
    def initialize_default_values(self):
        # Current weather
        self.current_condition.config(text="--")
        self.current_description.config(text="--")
        self.current_temp.config(text="--")
        self.current_feels.config(text="--")
        self.current_humidity.config(text="--")
        self.current_pressure.config(text="--")
        self.current_wind.config(text="--")
        
        # Next day weather
        self.next_condition.config(text="--")
        self.next_description.config(text="--")
        self.next_temp.config(text="--")
        self.next_feels.config(text="--")
        self.next_humidity.config(text="--")
        self.next_pressure.config(text="--")
        self.next_wind.config(text="--")
    
    def create_buttons(self):
        # Configure button style
        style = ttk.Style()
        style.configure('TButton',
            background='#0C5898',
            foreground='black'
        )
        
        # Fetch button
        self.fetch_btn = ttk.Button(self.button_frame, text="Fetch Weather", 
                                  command=self.fetch_weather)
        self.fetch_btn.pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        self.refresh_btn = ttk.Button(self.button_frame, text="Refresh", 
                                    command=self.refresh_weather)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Graph button
        self.graph_btn = ttk.Button(self.button_frame, text="Show Graph", 
                                  command=self.show_graph)
        self.graph_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        self.clear_btn = ttk.Button(self.button_frame, text="Clear Data", 
                                  command=self.clear_data)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
    
    def fetch_weather(self):
        city = self.city_var.get()
        if not city:
            messagebox.showwarning("Warning", "Please select a city first")
            return
            
        self.status_var.set(f"Fetching weather data for {city}...")
        self.root.update()
        
        # Get current weather
        current_data = get_weather_data(city)
        if current_data:
            self.update_weather_display(current_data, is_current=True)
            # Save to Excel
            save_data_to_excel(current_data, is_today=True)
        
        # Get next day weather
        next_day_data = get_next_day_weather(city)
        if next_day_data:
            self.update_weather_display(next_day_data, is_current=False)
            # Save to Excel
            save_data_to_excel(next_day_data, is_today=False)
        
        if current_data and next_day_data:
            self.status_var.set(f"Weather data updated for {city}")
        else:
            messagebox.showerror("Error", f"Failed to fetch weather data for {city}")
            self.status_var.set("Error fetching weather data")
    
    def update_weather_display(self, data, is_current):
        # Update weather icon
        self.update_weather_icon(data["Icon"], is_current)
        
        # Update condition with color
        condition = data["Condition"]
        color = Theme.WEATHER_COLORS.get(condition, self.theme['text'])
        
        if is_current:
            self.current_condition.config(text=condition, foreground=color)
            self.current_description.config(text=data["Description"].title())
            self.current_temp.config(text=f"{data['Temperature (°C)']}°C")
            self.current_feels.config(text=f"{data['Feels Like (°C)']}°C")
            self.current_humidity.config(text=f"{data['Humidity (%)']}%")
            self.current_pressure.config(text=f"{data['Pressure (hPa)']} hPa")
            self.current_wind.config(text=f"{data['Wind Speed (m/s)']} m/s")
        else:
            self.next_condition.config(text=condition, foreground=color)
            self.next_description.config(text=data["Description"].title())
            self.next_temp.config(text=f"{data['Temperature (°C)']}°C")
            self.next_feels.config(text=f"{data['Feels Like (°C)']}°C")
            self.next_humidity.config(text=f"{data['Humidity (%)']}%")
            self.next_pressure.config(text=f"{data['Pressure (hPa)']} hPa")
            self.next_wind.config(text=f"{data['Wind Speed (m/s)']} m/s")
    
    def update_weather_icon(self, icon_code, is_current):
        try:
            response = requests.get(get_weather_icon_url(icon_code))
            image = Image.open(BytesIO(response.content))
            # Resize the image to make it larger
            image = image.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            if is_current:
                self.current_icon.configure(image=photo)
                self.current_icon.image = photo
            else:
                self.next_icon.configure(image=photo)
                self.next_icon.image = photo
        except Exception as e:
            print(f"Error loading weather icon: {e}")
    
    def show_graph(self):
        city = self.city_var.get()
        if not city:
            messagebox.showwarning("Warning", "Please select a city first")
            return
            
        # Get today's data
        today_data = get_latest_data(city, is_today=True)
        tomorrow_data = get_latest_data(city, is_today=False)
        
        if not today_data and not tomorrow_data:
            messagebox.showinfo("Info", f"No weather data available for {city}")
            return
        
        # Create the plot
        plt.figure(figsize=(12, 6))
        
        # Plot today's data
        if today_data:
            plt.plot([today_data['Date']], [today_data['Temperature (°C)']], 
                    marker='o', label='Today', color='blue')
        
        # Plot tomorrow's data
        if tomorrow_data:
            plt.plot([tomorrow_data['Date']], [tomorrow_data['Temperature (°C)']], 
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
    
    def clear_data(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all weather data?"):
            today_cleared = clear_excel_data(is_today=True)
            tomorrow_cleared = clear_excel_data(is_today=False)
            
            if today_cleared or tomorrow_cleared:
                self.status_var.set("Weather data cleared")
                messagebox.showinfo("Success", "All weather data has been cleared")
                # Reset display to default values
                self.initialize_default_values()
            else:
                self.status_var.set("No data to clear")
    
    def refresh_weather(self):
        city = self.city_var.get()
        if not city:
            messagebox.showwarning("Warning", "Please select a city first")
            return
            
        self.status_var.set(f"Refreshing weather data for {city}...")
        self.root.update()
        
        # Get current weather
        current_data = get_weather_data(city)
        if current_data:
            self.update_weather_display(current_data, is_current=True)
        
        # Get next day weather
        next_day_data = get_next_day_weather(city)
        if next_day_data:
            self.update_weather_display(next_day_data, is_current=False)
        
        if current_data and next_day_data:
            self.status_var.set(f"Weather data refreshed for {city}")
        else:
            messagebox.showerror("Error", f"Failed to refresh weather data for {city}")
            self.status_var.set("Error refreshing weather data")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()