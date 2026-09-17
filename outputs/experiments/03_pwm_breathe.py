"""Lab 03: Fade an external LED with PWM on GP16."""
from machine import Pin, PWM
from time import sleep_ms

STEPS = 100
DELAY_MS = 12
pwm = PWM(Pin(16))
pwm.freq(1_000)

while True:
    for step in range(STEPS + 1):
        pwm.duty_u16(step * 65535 // STEPS)
        sleep_ms(DELAY_MS)
    for step in range(STEPS, -1, -1):
        pwm.duty_u16(step * 65535 // STEPS)
        sleep_ms(DELAY_MS)
