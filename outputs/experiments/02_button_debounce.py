"""Lab 02: Read a button on GP15 using the internal pull-up."""
from machine import Pin
from time import sleep_ms

button = Pin(15, Pin.IN, Pin.PULL_UP)
last_state = button.value()

while True:
    state = button.value()
    if state != last_state:
        sleep_ms(25)  # Wait out mechanical contact bounce.
        state = button.value()
        if state != last_state:
            last_state = state
            if state == 0:
                print("Button pressed")
            else:
                print("Button released")
    sleep_ms(5)
