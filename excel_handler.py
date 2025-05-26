import pandas as pd
import os
from config import TODAY_WEATHER_FILE, TOMORROW_WEATHER_FILE

def save_data_to_excel(data, is_today=True):
    try:
        # Select file based on data type
        file_path = TODAY_WEATHER_FILE if is_today else TOMORROW_WEATHER_FILE
        
        # Create assets directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Create DataFrame from data
        df = pd.DataFrame([data])
        
        # Append to existing file or create new one
        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            df = pd.concat([existing_df, df], ignore_index=True)
        
        # Save to Excel
        df.to_excel(file_path, index=False)
        return True
    except Exception as e:
        print(f"Error saving data to Excel: {e}")
        return False

def load_data_from_excel(is_today=True):
    file_path = TODAY_WEATHER_FILE if is_today else TOMORROW_WEATHER_FILE
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        return pd.DataFrame()

def clear_excel_data(is_today=True):
    try:
        file_path = TODAY_WEATHER_FILE if is_today else TOMORROW_WEATHER_FILE
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error clearing Excel data: {e}")
        return False

def get_latest_data(city=None, is_today=True):
    try:
        file_path = TODAY_WEATHER_FILE if is_today else TOMORROW_WEATHER_FILE
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            if not df.empty:
                if city:
                    df = df[df['City'] == city]
                if df.empty:
                    return None
                return df.iloc[-1].to_dict()
        return None
    except Exception as e:
        print(f"Error reading latest data: {e}")
        return None 