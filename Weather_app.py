import requests

# Function to fetch weather data
def fetch_weather_data(city):
    # API URL with the city name
    url = f"https://api.weatherapi.com/v1/current.json?key=9f24b8be2e33494b8b7172938251203&q={city}"
    
    # Make the API request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response into a dictionary
        data = response.json()
        return data
    else:
        return None

# Function to extract and format weather information
def extract_weather_info(data):
    if data:
        # Extract the required information
        weather_info = {
            "city": data["location"]["name"],
            "region": data["location"]["region"],
            "country": data["location"]["country"],
            "localtime": data["location"]["localtime"],
            "temperature_c": data["current"]["temp_c"],
            "temperature_f": data["current"]["temp_f"],
            "humidity": data["current"]["humidity"],
            "cloud": data["current"]["cloud"],
            "feelslike_c": data["current"]["feelslike_c"],
            "feelslike_f": data["current"]["feelslike_f"],
            "wind_kph": data["current"]["wind_kph"],
            "wind_mph": data["current"]["wind_mph"],
            "wind_dir": data["current"]["wind_dir"],
            "wind_degree": data["current"]["wind_degree"],
            "windchill_c": data["current"]["windchill_c"],
            "windchill_f": data["current"]["windchill_f"],
            "heatindex_c": data["current"]["heatindex_c"],
            "heatindex_f": data["current"]["heatindex_f"],
            "dewpoint_c": data["current"]["dewpoint_c"],
            "dewpoint_f": data["current"]["dewpoint_f"],
            "vis_km": data["current"]["vis_km"],
            "vis_miles": data["current"]["vis_miles"],
            "uv": data["current"]["uv"],
            "gust_mph": data["current"]["gust_mph"],
            "gust_kph": data["current"]["gust_kph"]
        }
        return weather_info
    else:
        return None

# Function to display weather information
def display_weather_info(weather_info):
    if weather_info:
        print(f"City: {weather_info['city']}")
        print(f"Region: {weather_info['region']}")
        print(f"Country: {weather_info['country']}")
        print(f"Local Time: {weather_info['localtime']}")
        print(f"Temperature: {weather_info['temperature_c']}°C / {weather_info['temperature_f']}°F")
        print(f"Humidity: {weather_info['humidity']}%")
        print(f"Cloud Cover: {weather_info['cloud']}%")
        print(f"Feels Like: {weather_info['feelslike_c']}°C / {weather_info['feelslike_f']}°F")
        print(f"Wind Speed: {weather_info['wind_kph']} kph / {weather_info['wind_mph']} mph")
        print(f"Wind Direction: {weather_info['wind_dir']} ({weather_info['wind_degree']}°)")
        print(f"Wind Chill: {weather_info['windchill_c']}°C / {weather_info['windchill_f']}°F")
        print(f"Heat Index: {weather_info['heatindex_c']}°C / {weather_info['heatindex_f']}°F")
        print(f"Dew Point: {weather_info['dewpoint_c']}°C / {weather_info['dewpoint_f']}°F")
        print(f"Visibility: {weather_info['vis_km']} km / {weather_info['vis_miles']} miles")
        print(f"UV Index: {weather_info['uv']}")
        print(f"Wind Gust: {weather_info['gust_mph']} mph / {weather_info['gust_kph']} kph")
    else:
        print("Error: Unable to fetch weather data.")

# Main function to run the program
def main():
    city = input("Enter City Name: ")
    data = fetch_weather_data(city)
    weather_info = extract_weather_info(data)
    display_weather_info(weather_info)

# Run the program
if __name__ == "__main__":
    main()