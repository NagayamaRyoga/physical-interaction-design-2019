#!/usr/bin/env python3
# coding: utf-8
from ctypes import cdll

class SetupFailedException(Exception):
    def __init__(self, message):
        self.message = message

class SerialLED:
    def __init__(self, libraryPath, pin, numLEDs):
        self.libraryPath = libraryPath
        self.pin = pin
        self.numLEDs = numLEDs

        # Load a native shared library
        self.serialled = cdll.LoadLibrary(libraryPath)

        # Setting up the native library (must be sudo-ed)
        if self.serialled.ledSetup(self.pin, self.numLEDs) == -1:
            raise SetupFailedException("`{}` must execute as a root".format(self.libraryPath))

    def __del__(self):
        # Clean the native library
        self.serialled.ledCleanup()

    def send(self, colors):
        for i in range(min(len(colors), self.numLEDs)):
            color = colors[i]
            r = min(max(color[0], 0), 255)
            g = min(max(color[1], 0), 255)
            b = min(max(color[2], 0), 255)

            # Set the color of i-th LED (not transmit yet)
            self.serialled.ledSetColor(i, r, g, b)

        # Transmit the color data
        self.serialled.ledSend()

    def clear(self):
        self.serialled.ledClearAll()

def test():
    import time
    led = SerialLED("./serial-led-pi/serialled.so", 18, 9)
    led.send([
        [0xff, 0xff, 0xff],
        [0xff, 0x00, 0x00],
        [0x00, 0xff, 0x00],
        [0x00, 0x00, 0xff],
        [0xff, 0xff, 0x00],
        [0xff, 0x00, 0xff],
        [0x00, 0xff, 0xff],
        [0x00, 0x00, 0x00],
        [0xff, 0xff, 0xff],
        ])

    time.sleep(5)
    led.clear();

if __name__ == "__main__":
    test()
