#!/usr/bin/env python3
# coding: utf-8
import os
import weather

API_KEY_NAME = "OPEN_WEATHER_MAP_API_KEY"

# Exceptions
class ApiKeyNotExistException(Exception):
    """Raised when the API key is not exists

    Attributes:
        message: str -- description
    """

    def __init__(self, message):
        self.message = message

def main():
    print("main")

    # Check if the API key exists
    if API_KEY_NAME not in os.environ:
        raise ApiKeyNotExistException("OpenWeatherMap API Key '{}' is not set".format(API_KEY_NAME))

    owm = weather.OpenWeatherMap(os.environ[API_KEY_NAME])
    owm.is_debug_log_enabled = True
    response = owm.fetch_forecast("Kyoto")

    for w in response.forecasts:
        print(w.timestamp, w.conditions[0].description)

if __name__ == "__main__":
    main()
