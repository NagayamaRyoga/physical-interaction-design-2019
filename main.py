#!/usr/bin/env python3
# coding: utf-8
import os
import time
import weather
import serial_led

LED_PIN = 18
NUM_LED = 15
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

def lerp(a, b, t):
    return (b - a) * t + a

def lerpColor(a, b, t):
    return [int(lerp(x, y, t)) for x, y in zip(a, b)]

def weatherColor(cloudiness, rain_3h):
    if rain_3h == None:
        return lerpColor(COLOR_SUNNY, COLOR_CLOUDY, cloudiness / 100)
    else:
        return lerpColor(COLOR_CLOUDY, COLOR_RAINY, min(rain_3h * 0.3, 1))

def buildLEDColor(forecasts, i):
    if i % 3 == 0:
        f = forecasts[i // 3]
        return weatherColor(f.cloudiness, f.rain_3h)

    a = weatherColor(forecasts[i // 3].cloudiness, forecasts[i // 3].rain_3h)
    b = weatherColor(forecasts[i // 3 + 1].cloudiness, forecasts[i // 3 + 1].rain_3h)
    print(i % 3 / 3)
    return lerpColor(a, b, (i % 3) / 3)

def buildLEDColors(forecasts):
    # From 06:00 ~ 24:00 (length of 7)
    forecasts = forecasts[1:8]

    # Returns the LED colors (Froms 06:00 ~ 24:00, 1h each, length of 19)
    return [buildLEDColor(forecasts, i) for i in range(19)]

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

    # Light the LED up
    led.send(buildLEDColors(response.forecasts))

    time.sleep(10)

if __name__ == "__main__":
    main()
