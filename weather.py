#!/usr/bin/env python3
# coding: utf-8
import datetime
import json
import urllib.request

def celsius(kelvin):
    return kelvin - 273.15

class City:
    """OpenWeatherMap city information object

    Attributes:
        id: int -- City ID
        name: str -- City name
        latitude: float -- City geo location, latitude
        longitude: float -- City geo location, longitude
        country: str -- Country code (GB, JP etc.)
        timezone: int -- Shift in seconds from UTC
    """
    def __init__(self, city):
        self.id = int(city["id"])
        self.name = str(city["name"])
        self.latitude = float(city["coord"]["lat"])
        self.longitude = float(city["coord"]["lon"])
        self.country = str(city["country"])
        self.timezone = int(city["timezone"])

class Weather:
    """Weather information object

    Attributes:
        timestamp: datetime.datetime -- Timestamp
        conditions: [Weather.Condition] -- List of weather conditions
        temperature: float -- Temperature [Celsius].
        temperature_min: float -- Minimum temperature [Celsius] at the moment of calculation.
        temperature_max: float -- Maximum temperature [Celsius] at the moment of calculation.
        pressure: float -- Atmospheric pressure on the sea level [hPa]
        pressure_sea_level: float -- Atmospheric pressure on the sea level [hPa]
        pressure_ground_level: float -- Atmospheric pressure on the ground level [hPa]
        humidity: float -- Humidity [%]
        cloudiness: float -- Cloudiness [%]
        wind_speed: float -- Wind speed [m/s].
        wind_direction: float -- Wind direction [degrees]
        rain_3h: float? -- Rain volume [mm] for last 3 hours
        snow_3h: float? -- Snow volume [mm] for last 3 hours
    """

    class Condition:
        """Weather condition information

        Attributes:
            id: int -- Weather condition id
            group: str -- Group of weather parameters (Rain, Snow, Extreme etc.)
            description: str -- Weather condition
        """

        def __init__(self, condition):
            self.id = int(condition["id"])
            self.group = str(condition["main"])
            self.description = str(condition["description"])

    def __init__(self, weather):
        self.timestamp = datetime.datetime.utcfromtimestamp(weather["dt"])
        self.conditions = [Weather.Condition(cond) for cond in weather["weather"]]
        self.temperature = celsius(kelvin=float(weather["main"]["temp"]))
        self.temperature_min = celsius(kelvin=float(weather["main"]["temp_min"]))
        self.temperature_max = celsius(kelvin=float(weather["main"]["temp_max"]))
        self.pressure = float(weather["main"]["pressure"])
        self.pressure_sea_level = float(weather["main"]["sea_level"])
        self.pressure_ground_level = float(weather["main"]["grnd_level"])
        self.humidity = float(weather["main"]["humidity"])
        self.cloudiness = float(weather["clouds"]["all"])
        self.wind_speed = float(weather["wind"]["speed"])
        self.wind_direction = float(weather["wind"]["deg"])
        self.rain_3h = float(weather["rain"]["3h"]) if "rain" in weather and "3h" in weather["rain"] else None
        self.snow_3h = float(weather["snow"]["3h"]) if "snow" in weather and "3h" in weather["snow"] else None

class Forecast:
    """Result of OpenWeatherMap forecast API result

    See:
        https://openweathermap.org/forecast5

    Attributes:
        city: City -- City information
        forecasts: [Weather] -- List of forecast information
    """

    def __init__(self, response):
        self.city = City(response["city"])
        self.forecasts = [Weather(item) for item in response["list"]]

class OpenWeatherMap:
    """OpenWeatherMap request helper

    Attributes:
        API_ENDPOINT: str -- API endpoint url

        key: str -- OpenWeatherMap API key
        is_debug_log_enabled: bool -- True if the debug log is enabled
    """

    API_ENDPOINT = "https://api.openweathermap.org/data/2.5/"

    def __init__(self, key):
        self.key = key
        self.is_debug_log_enabled = False

    def debug_log(self, s):
        if (self.is_debug_log_enabled):
            print(s)

    def fetch_forecast(self, city_name):
        params = { "q": city_name, "APPID": self.key }
        params = urllib.parse.urlencode(params)
        url = "{}{}?{}".format(self.API_ENDPOINT, "forecast", params)

        self.debug_log("OpenWeatherMap.fetch_weather({}) -- request url {}".format(city_name, url))

        response = urllib.request.urlopen(url)
        forecast = json.load(response)

        self.debug_log("OpenWeatherMap.fetch_weather({}) -- succeeded".format(city_name))
        return Forecast(forecast)
