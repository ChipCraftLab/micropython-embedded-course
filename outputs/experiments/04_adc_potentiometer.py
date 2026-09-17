"""Lab 04: Show a potentiometer value and estimated voltage."""
from machine import ADC
from time import sleep_ms

adc = ADC(26)  # GP26 is ADC0.

while True:
    raw = adc.read_u16()
    volts = raw * 3.3 / 65535
    bar = "#" * (raw * 20 // 65535)
    print("raw={:5d}  voltage={:.2f} V  {:<20}".format(raw, volts, bar))
    sleep_ms(250)
