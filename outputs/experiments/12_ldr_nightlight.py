"""Lab 12: Analog LDR Light Sensor and Automatic Nightlight with Hysteresis.

Uses ADC1 (GP27) connected to an LDR voltage divider, and controls an LED
on GP16. Demonstrates hysteresis (Schmitt trigger logic) to prevent rapid
flickering near the light/dark switching threshold.
"""
from machine import ADC, Pin
from time import sleep_ms

# Pin definitions
ldr = ADC(27)            # GP27 is ADC1
led = Pin(16, Pin.OUT)   # Indicator LED on GP16

# Hysteresis thresholds (0 - 65535 raw ADC scale)
# Lower value = darker environment (when LDR is pull-down)
# Adjust these values based on your room's ambient light level
DARK_THRESHOLD = 20000   # Below this, turn light ON
LIGHT_THRESHOLD = 25000  # Above this, turn light OFF

lamp_state = False

print("Lab 12: LDR Nightlight with Hysteresis active. Press Ctrl+C to stop.")
print("Monitoring ambient light level...")

try:
    while True:
        raw_val = ldr.read_u16()
        voltage = raw_val * 3.3 / 65535
        light_pct = (raw_val / 65535) * 100

        # Hysteresis switching logic
        if lamp_state and raw_val > LIGHT_THRESHOLD:
            lamp_state = False
            led.off()
            print("[STATE CHANGE] Ambient light restored -> Nightlight OFF")
        elif not lamp_state and raw_val < DARK_THRESHOLD:
            lamp_state = True
            led.on()
            print("[STATE CHANGE] Darkness detected -> Nightlight ON")

        status = "ON " if lamp_state else "OFF"
        bar = "=" * int(light_pct // 5)
        print("Raw: {:5d} | Volts: {:.2f}V | Light: {:5.1f}% | Lamp: {} [{:<20}]".format(
            raw_val, voltage, light_pct, status, bar
        ))
        sleep_ms(300)

except KeyboardInterrupt:
    led.off()
    print("\nNightlight experiment terminated.")
