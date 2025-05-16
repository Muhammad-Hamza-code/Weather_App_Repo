import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io
from datetime import datetime

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecast App")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Modern color palette
        self.colors = {
            "dark_teal": "#034C53",
            "medium_teal": "#007074",
            "light_teal": "#4D9E9E",
            "coral": "#F38C79",
            "light_coral": "#FFC1B4",
            "white": "#FFFFFF",
            "black": "#000000",
            "light_gray": "#F0F0F0"
        }
        
        # Configure style with new colors
        self.style = ttk.Style()
        
        # Main window background
        self.root.configure(bg=self.colors["dark_teal"])
        
        # Style configurations
        self.style.configure('TFrame', background=self.colors["dark_teal"])
        self.style.configure('TLabel', 
                           background=self.colors["dark_teal"],
                           foreground=self.colors["white"],
                           font=('Helvetica', 10))
        self.style.configure('Header.TLabel', 
                           font=('Helvetica', 24, 'bold'),
                           background=self.colors["dark_teal"],
                           foreground=self.colors["coral"])
        self.style.configure('Subheader.TLabel',
                           font=('Helvetica', 14),
                           background=self.colors["dark_teal"],
                           foreground=self.colors["light_coral"])
        self.style.configure('City.TLabel',
                           font=('Helvetica', 20, 'bold'),
                           background=self.colors["medium_teal"],
                           foreground=self.colors["white"])
        self.style.configure('Metric.TLabel', 
                           font=('Helvetica', 12),
                           background=self.colors["medium_teal"],
                           foreground=self.colors["white"])
        self.style.configure('Condition.TLabel',
                           font=('Helvetica', 16),
                           background=self.colors["medium_teal"],
                           foreground=self.colors["white"])
        self.style.configure('TButton', 
                           background=self.colors["coral"],
                           foreground=self.colors["black"],
                           font=('Helvetica', 12, 'bold'),
                           borderwidth=1,
                           padding=8)
        self.style.configure('TLabelframe', 
                           background=self.colors["dark_teal"],
                           foreground=self.colors["coral"],
                           bordercolor=self.colors["medium_teal"],
                           font=('Helvetica', 14, 'bold'))
        self.style.configure('TLabelframe.Label', 
                           background=self.colors["dark_teal"],
                           foreground=self.colors["coral"])
        self.style.map('TButton',
                     background=[('active', self.colors["light_coral"])])
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with app name and subtitle
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, 
                 text="Weather Forecast", 
                 style='Header.TLabel').pack(side=tk.LEFT)
        
        ttk.Label(header_frame, 
                 text="Real-time weather data for any location",
                 style='Subheader.TLabel').pack(side=tk.LEFT, padx=10)
        
        # Search frame with modern look
        search_frame = ttk.LabelFrame(main_frame, text="Search Location", padding=15)
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        search_inner_frame = ttk.Frame(search_frame)
        search_inner_frame.pack(fill=tk.X)
        
        ttk.Label(search_inner_frame, 
                 text="Enter City:", 
                 font=('Helvetica', 12)).pack(side=tk.LEFT, padx=(0, 10))
        
        self.city_entry = ttk.Entry(search_inner_frame, font=('Helvetica', 14))
        self.city_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 15))
        self.city_entry.bind('<Return>', lambda event: self.fetch_and_display_weather())
        
        search_btn = ttk.Button(search_inner_frame, 
                              text="Get Weather", 
                              command=self.fetch_and_display_weather)
        search_btn.pack(side=tk.LEFT)
        
        # Weather info frame
        self.weather_frame = ttk.LabelFrame(main_frame, 
                                          text="Current Weather",
                                          style='TLabelframe',
                                          padding=15)
        self.weather_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initially empty weather info
        self.clear_weather_info()
        
    def clear_weather_info(self):
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
            
        empty_label = ttk.Label(
            self.weather_frame, 
            text="Enter a city name and click 'Get Weather' to see current conditions",
            style='Subheader.TLabel'
        )
        empty_label.pack(expand=True)
        
    def fetch_weather_data(self, city):
        url = f"https://api.weatherapi.com/v1/current.json?key=9f24b8be2e33494b8b7172938251203&q={city}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")
            return None
    
    def extract_weather_info(self, data):
        if not data:
            return None
            
        try:
            location = data.get("location", {})
            current = data.get("current", {})
            condition = current.get("condition", {})
            
            localtime = location.get("localtime", "")
            try:
                dt = datetime.strptime(localtime, "%Y-%m-%d %H:%M")
                localtime = dt.strftime("%A, %B %d %Y %I:%M %p")
            except:
                pass
            
            return {
                "city": location.get("name", "N/A"),
                "region": location.get("region", "N/A"),
                "country": location.get("country", "N/A"),
                "localtime": localtime,
                "temperature_c": current.get("temp_c", "N/A"),
                "temperature_f": current.get("temp_f", "N/A"),
                "condition": condition.get("text", "N/A"),
                "icon": condition.get("icon", ""),
                "humidity": current.get("humidity", "N/A"),
                "cloud": current.get("cloud", "N/A"),
                "feelslike_c": current.get("feelslike_c", "N/A"),
                "feelslike_f": current.get("feelslike_f", "N/A"),
                "wind_kph": current.get("wind_kph", "N/A"),
                "wind_mph": current.get("wind_mph", "N/A"),
                "wind_dir": current.get("wind_dir", "N/A"),
                "uv": current.get("uv", "N/A"),
                "gust_kph": current.get("gust_kph", "N/A"),
                "vis_km": current.get("vis_km", "N/A"),
                "pressure_mb": current.get("pressure_mb", "N/A")
            }
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process weather data: {str(e)}")
            return None
    
    def display_weather_info(self, weather_info):
        # Clear previous weather info
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
            
        if not weather_info:
            self.clear_weather_info()
            return
            
        # Main content frame with custom background
        content_frame = ttk.Frame(self.weather_frame, style='TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header with city info
        header_text = f"{weather_info['city']}, {weather_info['region']}, {weather_info['country']}"
        header = ttk.Label(content_frame, 
                         text=header_text, 
                         style='City.TLabel')
        header.pack(pady=(0, 10))
        
        # Local time
        local_time = ttk.Label(content_frame, 
                             text=f"Local Time: {weather_info['localtime']}", 
                             style='Subheader.TLabel')
        local_time.pack(pady=(0, 20))
        
        # Current conditions row
        conditions_row = ttk.Frame(content_frame)
        conditions_row.pack(fill=tk.X, pady=(0, 30))
        
        # Temperature display
        temp_frame = ttk.Frame(conditions_row)
        temp_frame.pack(side=tk.LEFT, padx=20)
        
        temp_text = f"{weather_info['temperature_c']}°C"
        temp_label = ttk.Label(temp_frame, 
                             text=temp_text, 
                             font=('Helvetica', 36, 'bold'),
                             background=self.colors["medium_teal"],
                             foreground=self.colors["white"])
        temp_label.pack()
        
        feels_like = ttk.Label(temp_frame,
                             text=f"Feels like: {weather_info['feelslike_c']}°C",
                             style='Metric.TLabel')
        feels_like.pack()
        
        # Condition and icon
        cond_frame = ttk.Frame(conditions_row)
        cond_frame.pack(side=tk.LEFT, padx=20)
        
        # Display weather icon
        if weather_info['icon']:
            try:
                icon_url = "https:" + weather_info['icon']
                response = requests.get(icon_url, stream=True, timeout=5)
                if response.status_code == 200:
                    image_data = response.content
                    image = Image.open(io.BytesIO(image_data))
                    image = image.resize((100, 100), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    
                    icon_label = ttk.Label(cond_frame, image=photo)
                    icon_label.image = photo
                    icon_label.pack()
            except Exception as e:
                print(f"Error loading weather icon: {e}")
        
        condition_label = ttk.Label(cond_frame, 
                                 text=weather_info['condition'], 
                                 style='Condition.TLabel')
        condition_label.pack()
        
        # Weather metrics - two columns
        metrics_frame = ttk.Frame(content_frame)
        metrics_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Left column metrics
        left_metrics = ttk.Frame(metrics_frame)
        left_metrics.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)
        
        self.create_metric_panel(left_metrics, "💧 Humidity", f"{weather_info['humidity']}%")
        self.create_metric_panel(left_metrics, "☁️ Cloud Cover", f"{weather_info['cloud']}%")
        self.create_metric_panel(left_metrics, "☀️ UV Index", weather_info['uv'])
        self.create_metric_panel(left_metrics, "🎈 Pressure", f"{weather_info['pressure_mb']} mb")
        
        # Right column metrics
        right_metrics = ttk.Frame(metrics_frame)
        right_metrics.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)
        
        self.create_metric_panel(right_metrics, "🌬️ Wind", 
                               f"{weather_info['wind_kph']} kph ({weather_info['wind_dir']})")
        self.create_metric_panel(right_metrics, "💨 Wind Gust", f"{weather_info['gust_kph']} kph")
        self.create_metric_panel(right_metrics, "👁️ Visibility", f"{weather_info['vis_km']} km")
        
    def create_metric_panel(self, parent, label, value):
        panel = ttk.Frame(parent, style='TFrame')
        panel.pack(fill=tk.X, pady=5)
        
        lbl = ttk.Label(panel, 
                      text=label,
                      style='Metric.TLabel',
                      anchor='w')
        lbl.pack(fill=tk.X)
        
        val = ttk.Label(panel, 
                      text=value,
                      font=('Helvetica', 14, 'bold'),
                      background=self.colors["light_teal"],
                      foreground=self.colors["white"],
                      anchor='w')
        val.pack(fill=tk.X)
        
    def fetch_and_display_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return
            
        # Show loading state
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
            
        loading_label = ttk.Label(
            self.weather_frame, 
            text="Fetching weather data...",
            style='Subheader.TLabel'
        )
        loading_label.pack(expand=True)
        self.root.update()
        
        data = self.fetch_weather_data(city)
        if data:
            weather_info = self.extract_weather_info(data)
            self.display_weather_info(weather_info)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()