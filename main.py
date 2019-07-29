#!/usr/bin/env python3
# coding: utf-8
import os
import time
import weather
import serial_led

LED_PIN = 18
NUM_LED = 9
API_KEY_NAME = "OPEN_WEATHER_MAP_API_KEY"

COLOR_SUNNY = [0xff, 0x00, 0x00]
COLOR_CLOUDY = [0xa0, 0xa0, 0xa0]
COLOR_RAINY = [0x00, 0x00, 0xff]

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

    # fetch the weather forecast data
    owm = weather.OpenWeatherMap(os.environ[API_KEY_NAME])
    owm.is_debug_log_enabled = True
    response = owm.fetch_forecast("Kyoto")
    
    # Setup the serial LED
    led = serial_led.SerialLED("./serial-led-pi/serialled.so", LED_PIN, NUM_LED)
    
    # Build the colors
    def lerp(a, b, t):
        return (b - a) * t + a

    def lerpColor(a, b, t):
        return [int(lerp(x, y, t)) for x, y in zip(a, b)]
        
    def weatherColor(cloudiness, rain_1h):
        if rain_1h == None:
            return lerpColor(COLOR_SUNNY, COLOR_CLOUDY, cloudiness / 100)
        else:
            return lerpColor(COLOR_CLOUDY, COLOR_RAINY, max(rain_1h * 1, 1))
    
    led.send([weatherColor(w.cloudiness, w.rain_3h / 3 if w.rain_3h else None)
        for w in response.forecasts[:NUM_LED]])

    for w in response.forecasts[:NUM_LED]:
        print(w.timestamp, w.conditions[0].description, w.cloudiness, w.rain_3h)

    time.sleep(10)

if __name__ == "__main__":
    main()
