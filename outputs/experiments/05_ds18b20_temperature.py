"""Lab 05: Read a DS18B20 thermometer on GP4."""
from machine import Pin
from time import sleep_ms
import ds18x20
import onewire

bus = ds18x20.DS18X20(onewire.OneWire(Pin(4)))
devices = bus.scan()

if not devices:
    raise RuntimeError("No DS18B20 found; check DQ, GND, 3V3 and the 4.7k resistor")

print("Found {} sensor(s)".format(len(devices)))
while True:
    bus.convert_temp()
    sleep_ms(750)  # A 12-bit conversion needs up to 750 ms.
    for device in devices:
        celsius = bus.read_temp(device)
        print("{}: {:.2f} C / {:.2f} F".format(device, celsius, celsius * 9 / 5 + 32))
