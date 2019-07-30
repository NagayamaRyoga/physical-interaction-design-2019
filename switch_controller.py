import RPi.GPIO as GPIO

class Switch:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_on(self):
        return GPIO.input(self.pin) == GPIO.HIGH

class SwitchController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
    
    def __del__(self):
        GPIO.cleanup()

    def switch(self, pin):
        return Switch(pin)
    
if __name__== "__main__":
    import time
    sw = SwitchController()
    sw1 = sw.switch(4)
    sw2 = sw.switch(5)
    sw3 = sw.switch(6)
    
    while True:
        print("--------------------")
        print(sw1.is_on())
        print(sw2.is_on())
        print(sw3.is_on())

        time.sleep(0.1)

