"""Lab 06: Measure distance with an HC-SR04 using GP3 trigger and GP2 echo."""
from machine import Pin, time_pulse_us
from time import sleep_ms, sleep_us

trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)
trigger.off()

while True:
    trigger.on()
    sleep_us(10)
    trigger.off()
    duration_us = time_pulse_us(echo, 1, 30_000)
    if duration_us < 0:
        print("No echo (error {})".format(duration_us))
    else:
        distance_cm = duration_us * 0.0343 / 2
        print("{:.1f} cm".format(distance_cm))
    sleep_ms(500)
