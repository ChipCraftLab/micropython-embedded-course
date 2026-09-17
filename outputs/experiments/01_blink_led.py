"""Lab 01: Blink the Pico W on-board LED."""
from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)

while True:
    led.on()
    sleep(0.15)
    led.off()
    sleep(0.85)
