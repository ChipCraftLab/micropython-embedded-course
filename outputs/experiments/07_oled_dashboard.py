"""Lab 07: Display a counter on a 128x64 SSD1306 I2C OLED."""
from machine import I2C, Pin
from time import sleep_ms
import ssd1306

OLED_ADDRESS = 0x3C
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400_000)
addresses = i2c.scan()
print("I2C addresses:", [hex(address) for address in addresses])

if OLED_ADDRESS not in addresses:
    raise RuntimeError("OLED not found at 0x3C; inspect the scan result and wiring")

display = ssd1306.SSD1306_I2C(128, 64, i2c, addr=OLED_ADDRESS)
count = 0
while True:
    display.fill(0)
    display.text("Pico 2 W", 0, 0)
    display.text("I2C dashboard", 0, 16)
    display.text("Count: {}".format(count), 0, 40)
    display.show()
    count += 1
    sleep_ms(500)
