"""Lab 10: Count debounced button presses using a falling-edge interrupt."""
from machine import Pin
from time import sleep_ms, ticks_diff, ticks_ms

button = Pin(14, Pin.IN, Pin.PULL_UP)
presses = 0
last_event_ms = 0

def button_pressed(pin):
    # Keep interrupt handlers short: no print(), allocation, or sleep().
    global presses, last_event_ms
    now = ticks_ms()
    if ticks_diff(now, last_event_ms) > 200:
        presses += 1
        last_event_ms = now

button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)

while True:
    print("Valid presses:", presses)
    sleep_ms(500)
