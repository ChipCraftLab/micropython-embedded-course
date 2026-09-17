"""Lab 11: Addressable RGB LED (WS2812B / NeoPixel) control on GP18.

Demonstrates high-speed single-wire timing protocol, 24-bit GRB color
formatting, and smooth color wheel / rainbow animation cycles.
"""
from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

# Hardware configuration
PIN_NUM = 18       # Connect NeoPixel DIN to GP18
NUM_PIXELS = 8     # Number of RGB LEDs on your strip/ring

np = NeoPixel(Pin(PIN_NUM, Pin.OUT), NUM_PIXELS)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    pos = pos & 255
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

def clear():
    """Turn off all pixels."""
    for i in range(NUM_PIXELS):
        np[i] = (0, 0, 0)
    np.write()

print("Lab 11: Running NeoPixel RGB demonstration...")
try:
    while True:
        # Rainbow cycle animation
        for j in range(256):
            for i in range(NUM_PIXELS):
                pixel_index = (i * 256 // NUM_PIXELS) + j
                np[i] = wheel(pixel_index)
            np.write()
            sleep_ms(15)
except KeyboardInterrupt:
    clear()
    print("\nNeoPixel stopped and cleared.")
