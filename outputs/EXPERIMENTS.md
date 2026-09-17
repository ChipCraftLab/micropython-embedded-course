# Experiment Instructions & Laboratory Index (Labs 01 – 16)

This reference card lists parts, wiring, principles, and student challenges for all 16 embedded experiments.

---

## 01 — On-board LED Heartbeat
* **Parts:** Raspberry Pi Pico / Pico 2 / Pico 2 W, USB cable.
* **Wiring:** None required. On Pico W / Pico 2 W, the LED is addressed as `"LED"`.
* **Script:** `experiments/01_blink_led.py`
* **Concepts:** Digital output, push-pull driver, logic levels (3.3V / 0V), non-reallocating loops.
* **Challenge:** Implement a realistic double-pulse human heartbeat rhythm.

---

## 02 — Button Input and Contact Debounce
* **Parts:** Breadboard, momentary pushbutton, 2 jumper wires.
* **Wiring:** Button leg A $\rightarrow$ GP15; Button leg B $\rightarrow$ GND.
* **Script:** `experiments/02_button_debounce.py`
* **Concepts:** Floating inputs, high impedance, internal pull-up resistor, mechanical contact bounce.
* **Challenge:** Convert the transition logger into a running counter of valid button presses.

---

## 03 — PWM LED Dimmer & Breathing Light
* **Parts:** 5mm LED, 220–330 $\Omega$ resistor, breadboard, jumpers.
* **Wiring:** GP16 $\rightarrow$ resistor $\rightarrow$ LED Anode; LED Cathode $\rightarrow$ GND.
* **Script:** `experiments/03_pwm_breathe.py`
* **Concepts:** Pulse Width Modulation, duty cycle ($0\text{--}65535$), frequency (1 kHz), persistence of vision.
* **Challenge:** Implement an asymmetric breathing wave (fast inhale 400 ms, slow exhale 1200 ms).

---

## 04 — Potentiometer ADC Voltage Meter
* **Parts:** 10 k$\Omega$ rotary potentiometer, 3 jumpers.
* **Wiring:** Outer pins $\rightarrow$ 3V3(OUT) and GND; Center wiper $\rightarrow$ GP26 (ADC0).
* **Script:** `experiments/04_adc_potentiometer.py`
* **Concepts:** SAR Analog-to-Digital Converter, 16-bit unsigned scaling, input impedance, terminal telemetry.
* **Challenge:** Link the ADC potentiometer reading directly to control the PWM brightness from Lab 03.

---

## 05 — Digital Thermometer: DS18B20
* **Parts:** DS18B20 temperature sensor (probe or TO-92), 4.7 k$\Omega$ resistor, jumpers.
* **Wiring:** VDD $\rightarrow$ 3V3(OUT), GND $\rightarrow$ GND, DQ $\rightarrow$ GP4; place 4.7 k$\Omega$ between DQ and 3V3.
* **Script:** `experiments/05_ds18b20_temperature.py`
* **Concepts:** Dallas 1-Wire open-drain bus, 64-bit unique ROM addressing, thermal conversion latency.
* **Challenge:** Add an audible or visual alarm if temperature exceeds 30 °C (86 °F).

---

## 06 — Ultrasonic Distance Meter (HC-SR04)
* **Parts:** HC-SR04 ultrasonic sensor, two 1 k$\Omega$ resistors (voltage divider), jumpers.
* **Wiring:** VCC $\rightarrow$ VBUS (5V), GND $\rightarrow$ GND, TRIG $\rightarrow$ GP3; ECHO $\rightarrow$ 1 k$\Omega$ $\rightarrow$ GP2 $\rightarrow$ 1 k$\Omega$ $\rightarrow$ GND.
* **Script:** `experiments/06_ultrasonic_distance.py`
* **Concepts:** Acoustic time-of-flight, speed of sound ($343\text{ m/s}$), 5V-to-3.3V logic level shifting.
* **Challenge:** Compute a rolling average of the last 5 distance measurements to reject acoustic noise.

---

## 07 — I2C OLED Sensor Dashboard
* **Parts:** SSD1306 128x64 I2C OLED display, 4 jumpers, `ssd1306.py` library.
* **Wiring:** VCC $\rightarrow$ 3V3(OUT), GND $\rightarrow$ GND, SDA $\rightarrow$ GP0, SCL $\rightarrow$ GP1.
* **Script:** `experiments/07_oled_dashboard.py`
* **Concepts:** I2C synchronous bus, frame buffer memory geometry, graphics rendering.
* **Challenge:** Display live real-time voltage from Lab 04 on the OLED screen.

---

## 08 — Wi-Fi Network Scanner
* **Parts:** Pico W / Pico 2 W and micro-USB cable.
* **Wiring:** None.
* **Script:** `experiments/08_wifi_scan.py`
* **Concepts:** 2.4 GHz RF beacon frames, SSID decoding, RSSI signal attenuation in dBm, channel allocation.
* **Challenge:** Sort detected access points by signal strength (RSSI) from strongest to weakest.

---

## 09 — I2C Bus Explorer & Diagnostic Prober
* **Parts:** Any I2C module (OLED, BME280, MPU6050, etc.), 4 jumpers.
* **Wiring:** VCC $\rightarrow$ 3V3(OUT), GND $\rightarrow$ GND, SDA $\rightarrow$ GP0, SCL $\rightarrow$ GP1.
* **Script:** `experiments/09_i2c_explorer.py`
* **Concepts:** Bus probing, 7-bit addressing, ACK/NACK responses, hardware fault isolation.
* **Challenge:** Connect two distinct I2C devices to the same two wires and identify both addresses.

---

## 10 — Hardware Interrupt Event Counter
* **Parts:** Pushbutton, 2 jumpers.
* **Wiring:** Button leg A $\rightarrow$ GP14, Button leg B $\rightarrow$ GND.
* **Script:** `experiments/10_interrupt_counter.py`
* **Concepts:** Hardware IRQ, falling-edge triggers, ISR latency, ISR rules (no print/malloc in ISR).
* **Challenge:** Measure the exact elapsed time between two consecutive button clicks.

---

## 11 — Addressable NeoPixel / WS2812B RGB LED
* **Parts:** WS2812B / NeoPixel 8-LED strip or ring, 3 jumpers.
* **Wiring:** VCC $\rightarrow$ 3V3(OUT) or VBUS, GND $\rightarrow$ GND, DIN $\rightarrow$ GP18.
* **Script:** `experiments/11_neopixel_rgb.py`
* **Concepts:** 800 kHz single-wire timing, 24-bit GRB color encoding, algorithmic color wheel.
* **Challenge:** Implement a theater-chase animation where lights chase each other around the strip.

---

## 12 — Analog LDR Light Sensor & Nightlight with Hysteresis
* **Parts:** Photoresistor (LDR), 10 k$\Omega$ resistor, LED, 220 $\Omega$ resistor, jumpers.
* **Wiring:** LDR divider to GP27 (ADC1); LED indicator to GP16.
* **Script:** `experiments/12_ldr_nightlight.py`
* **Concepts:** Variable resistance, Schmitt trigger hysteresis, threshold chatter prevention.
* **Challenge:** Dynamically adjust the LED brightness proportional to room darkness using PWM.

---

## 13 — Piezo Buzzer Melody Synthesizer
* **Parts:** Passive piezo buzzer, 100 $\Omega$ resistor, jumpers.
* **Wiring:** Buzzer (+) $\rightarrow$ 100 $\Omega$ $\rightarrow$ GP17; Buzzer (-) $\rightarrow$ GND.
* **Script:** `experiments/13_pwm_buzzer_melody.py`
* **Concepts:** Frequency generation ($f = \frac{1}{T}$), note-to-frequency mapping, musical tempos.
* **Challenge:** Transcribe a custom song melody and play it through the buzzer.

---

## 14 — True Dual-Core Multiprocessing (`_thread`)
* **Parts:** Pushbutton, 2 jumpers.
* **Wiring:** Button between GP15 and GND.
* **Script:** `experiments/14_multicore_threading.py`
* **Concepts:** Dual-core ARM architecture, secondary thread spawning, shared heap, lock-free flags.
* **Challenge:** Pass sensor data from Core 1 to Core 0 safely using a shared list or thread lock.

---

## 15 — MicroPython Wi-Fi Socket Web Server
* **Parts:** Pico W / Pico 2 W, Wi-Fi connection.
* **Wiring:** None.
* **Script:** `experiments/15_wifi_web_server.py`
* **Concepts:** TCP sockets, HTTP GET parsing, dynamic HTML templating, browser IoT control.
* **Challenge:** Add an interactive button to the webpage that triggers a buzzer tone on the Pico.

---

## 16 — Non-Volatile Flash Filesystem Logger
* **Parts:** Pico / Pico 2 W.
* **Wiring:** None (reads internal temperature sensor).
* **Script:** `experiments/16_flash_filesystem_logger.py`
* **Concepts:** LittleFS flash filesystem, JSON serialization, persistent state across power cycles.
* **Challenge:** Add a REST or REPL command to reset the persistent boot counter back to zero.
