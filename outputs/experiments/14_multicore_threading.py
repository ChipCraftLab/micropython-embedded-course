"""Lab 14: True Dual-Core Multithreading on RP2040 / RP2350 using _thread.

The Raspberry Pi Pico architecture features two 32-bit cores (Core 0 and Core 1).
MicroPython exposes this through the `_thread` module.
- Core 1 runs an independent heartbeat LED blinking thread.
- Core 0 runs a main task monitoring button inputs and calculating throughput.
"""
import _thread
from machine import Pin
from time import sleep_ms, ticks_diff, ticks_ms

# Thread synchronization flag
thread_running = True

def core1_heartbeat():
    """Worker task executed entirely on Core 1."""
    led = Pin("LED", Pin.OUT)
    print("[Core 1] Heartbeat task launched on secondary processor.")
    while thread_running:
        led.on()
        sleep_ms(80)
        led.off()
        sleep_ms(80)
        led.on()
        sleep_ms(80)
        led.off()
        sleep_ms(600)
    led.off()
    print("[Core 1] Thread stopping.")

print("Lab 14: Launching Core 1 background task...")
_thread.start_new_thread(core1_heartbeat, ())

# Main program running on Core 0
button = Pin(15, Pin.IN, Pin.PULL_UP)
cycle_count = 0
start_time = ticks_ms()

print("[Core 0] Main monitor running. Press button on GP15 or press Ctrl+C to exit.")

try:
    while True:
        cycle_count += 1
        btn_state = "PRESSED" if button.value() == 0 else "RELEASED"
        elapsed_sec = ticks_diff(ticks_ms(), start_time) / 1000.0

        if cycle_count % 10 == 0:
            print("[Core 0] Elapsed: {:.1f}s | Loops: {:6d} | Button GP15: {}".format(
                elapsed_sec, cycle_count, btn_state
            ))
        sleep_ms(100)

except KeyboardInterrupt:
    print("\nStopping threads...")
    thread_running = False
    sleep_ms(500)
    print("Dual-core demo complete.")
