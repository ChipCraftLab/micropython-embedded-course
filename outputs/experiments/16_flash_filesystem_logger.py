"""Lab 16: Non-Volatile Flash Storage and Event Logging using JSON.

Embedded microcontrollers must survive power resets without losing critical
calibration or historical state. This experiment demonstrates reading,
updating, and committing persistent JSON data to onboard flash memory.
"""
import json
import os
from machine import ADC, Pin
from time import sleep_ms, ticks_ms

CONFIG_FILE = "device_config.json"
LOG_FILE = "sensor_log.csv"

def init_storage():
    """Ensure initial configuration file exists on flash."""
    try:
        os.stat(CONFIG_FILE)
        print("Found existing configuration on flash.")
    except OSError:
        print("No config file found. Initializing default flash configuration...")
        default_config = {
            "device_id": "PICO2W-001",
            "boot_count": 0,
            "sample_rate_ms": 1000,
            "calibration_offset": 0.0
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f)

def update_boot_counter():
    """Load config, increment boot counter, and write back to flash."""
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    config["boot_count"] += 1

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

    print("Persistent Boot Count: {}".format(config["boot_count"]))
    return config

def log_sample(timestamp_ms, voltage):
    """Append a telemetry reading to CSV file on flash."""
    with open(LOG_FILE, "a") as f:
        f.write("{},{:.3f}\n".format(timestamp_ms, voltage))

# Hardware setup (reading onboard temperature or ADC0)
sensor = ADC(4)  # ADC4 connects to internal RP2040/RP2350 temperature sensor

print("Lab 16: Non-volatile Flash File System Storage Demo")
init_storage()
cfg = update_boot_counter()

print("Logging 5 sensor readings to '{}'...".format(LOG_FILE))
for i in range(5):
    raw = sensor.read_u16()
    volts = raw * 3.3 / 65535
    # Standard RP2040 temperature approximation formula
    temp_c = 27 - (volts - 0.706) / 0.001721
    uptime = ticks_ms()

    log_sample(uptime, temp_c)
    print("Logged entry {:d}: uptime={}ms temp={:.2f} C".format(i + 1, uptime, temp_c))
    sleep_ms(cfg["sample_rate_ms"])

print("\nVerifying stored log on flash:")
with open(LOG_FILE, "r") as f:
    lines = f.readlines()
    print("Total recorded entries: {}".format(len(lines)))
    for line in lines[-5:]:
        print("  -> " + line.strip())

print("\nFlash storage demo complete. Config and logs remain safe across power cuts!")
