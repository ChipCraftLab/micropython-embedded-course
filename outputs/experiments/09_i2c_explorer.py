"""Lab 09: Scan I2C bus 0 on GP0 (SDA) and GP1 (SCL)."""
from machine import I2C, Pin
from time import sleep_ms

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100_000)

while True:
    addresses = i2c.scan()
    if addresses:
        print("Found:", ", ".join("0x{:02X}".format(address) for address in addresses))
    else:
        print("No I2C devices: check power, ground, SDA and SCL")
    sleep_ms(2_000)
