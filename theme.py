# Professional Color Themes
from tkinter import ttk

class Theme:
    # Modern Light Theme
    LIGHT = {
        'bg': '#F5F5F5',
        'fg': '#FFFFFF',
        'accent': '#0078D4',
        'secondary': 'red',
        'text': '#FFFFFF',
        'button': '#0C5898',
        'button_hover': 'red',
        'success': '#107C10',
        'warning': '#FFB900',
        'error': '#D13438',
        'frame_bg': '#80BFF5',
        'label_bg': '#80BFF5',
        'entry_bg': '#FFFFFF',
        'border': 'red'
    }

    # Professional Blue Theme
    BLUE = {
        'bg': '#F0F8FF',
        'fg': '#FFFFFF',
        'accent': '#2B6CB0',
        'secondary': '#EBF8FF',
        'text': '#FFFFFF',
        'button': '#0C5898',
        'button_hover': '#0C5898',
        'success': '#38A169',
        'warning': '#ECC94B',
        'error': '#E53E3E',
        'frame_bg': '#68BAFF',
        'label_bg': '#68BAFF',
        'entry_bg': '#FFFFFF',
        'border': '#BEE3F8'
    }

    # Weather Condition Colors
    WEATHER_COLORS = {
        "Clear": "#FFD700",      # Gold
        "Clouds": "#0C61D2",     # Sky Blue
        "Rain": "#4169E1",       # Royal Blue
        "Drizzle": "#1E90FF",    # Dodger Blue
        "Thunderstorm": "#4B0082", # Indigo
        "Snow": "#F0F8FF",       # Alice Blue
        "Mist": "#E6E6FA",       # Lavender
        "Fog": "#DCDCDC",        # Gainsboro
        "Haze": "#F5F5F5",       # White Smoke
        "Smoke": "#A9A9A9",      # Dark Gray
        "Dust": "#DEB887",       # Burlywood
        "Sand": "#F4A460",       # Sandy Brown
        "Ash": "#808080",        # Gray
        "Squall": "#4682B4",     # Steel Blue
        "Tornado": "#8B0000"     # Dark Red
    }

    # Font Styles
    FONTS = {
        'title': ('Segoe UI', 16, 'bold'),
        'subtitle': ('Segoe UI', 14, 'bold'),
        'normal': ('Segoe UI', 12),
        'small': ('Segoe UI', 10),
        'button': ('Segoe UI', 11, 'bold')
    }

    @staticmethod
    def apply_theme(root, theme_name='LIGHT'):
        theme = getattr(Theme, theme_name.upper())
        
        # Configure ttk styles
        style = ttk.Style()
        style.configure('.',
            background=theme['bg'],
            foreground=theme['fg'],
            fieldbackground=theme['entry_bg'],
            troughcolor=theme['secondary'],
            selectbackground=theme['accent'],
            selectforeground=theme['fg'],
            insertcolor=theme['fg']
        )
        
        # Configure specific widget styles
        style.configure('TFrame', background=theme['frame_bg'])
        style.configure('TLabel', 
            background=theme['label_bg'],
            foreground=theme['text'],
            font=Theme.FONTS['normal']
        )
        
        # Configure button styles with the new color
        style.configure('TButton',
            background=theme['button'],
            foreground='white',
            font=Theme.FONTS['button'],
            padding=5
        )
        style.map('TButton',
            background=[('active', theme['button_hover'])],
            foreground=[('active', 'white')]
        )
        
        style.configure('TLabelframe', 
            background=theme['frame_bg'],
            foreground=theme['text']
        )
        style.configure('TLabelframe.Label',
            background=theme['frame_bg'],
            foreground=theme['text'],
            font=Theme.FONTS['subtitle']
        )
        
        # Configure root window
        root.configure(bg=theme['bg'])
        
        return theme 