# Raspberry Pi Pico / Pico 2 W MicroPython Lab Pack

This pack contains **sixteen self-contained embedded systems experiments** designed for students and engineers learning embedded development with MicroPython on the Raspberry Pi Pico / Pico 2 / Pico 2 W.

For the comprehensive textbook tutorial, circuit diagrams, and deep dives, read [TUTORIAL.md](../TUTORIAL.md).

---

## Curriculum Table

| Lab | Topic | Primary Concept |
|---|---|---|
| **01** | On-board LED | Digital push-pull output logic levels. |
| **02** | Button Debounce | High impedance inputs, internal pull-ups, and contact settling. |
| **03** | PWM Fade | Pulse Width Modulation, duty cycles, and average power. |
| **04** | Potentiometer | Successive approximation ADC, 16-bit unsigned scaling. |
| **05** | DS18B20 Temp | Dallas 1-Wire open-drain bus with pull-up. |
| **06** | Ultrasonic Range | Acoustic time-of-flight and 5V-to-3.3V voltage division. |
| **07** | OLED Dashboard | I2C synchronous bus and frame buffer graphics. |
| **08** | Wi-Fi AP Scan | 802.11 b/g/n RF beacon scanning, RSSI, channels. |
| **09** | I2C Explorer | ACK/NACK bus probing and hardware fault isolation. |
| **10** | Interrupt Counter | Hardware IRQ triggers, ISR latency, debouncing. |
| **11** | NeoPixel RGB | High-speed single-wire timing (800 kHz) and 24-bit GRB. |
| **12** | LDR Nightlight | Analog photoresistor divider with Schmitt trigger hysteresis. |
| **13** | PWM Buzzer Melody | Audio tone generation and acoustic note frequencies. |
| **14** | Multicore Threading | Dual-core processing on RP2040/RP2350 using `_thread`. |
| **15** | Wi-Fi Web Server | Embedded TCP socket server with mobile-friendly HTML UI. |
| **16** | Flash FS Logger | Persistent non-volatile JSON state on LittleFS flash. |

---

## Hardware Pinout Reference

| Signal / Peripheral | Pico Pin Used | Description / Warning |
|---|---|---|
| On-board LED | `"LED"` (Pico W) / GP25 (Pico) | Push-pull digital output |
| Button Input | GP15 | Connect other terminal to GND |
| External LED (PWM) | GP16 | Use 220–330 $\Omega$ series resistor |
| Buzzer Tone (PWM) | GP17 | Passive piezo buzzer via 100 $\Omega$ resistor |
| NeoPixel WS2812B | GP18 | 800 kHz single-wire data stream |
| Interrupt Button | GP14 | Hardware falling-edge IRQ |
| Potentiometer Wiper | GP26 (ADC0) | Max 3.3V input voltage |
| LDR Divider | GP27 (ADC1) | $10\text{ k}\Omega$ pull-up to 3.3V |
| DS18B20 1-Wire | GP4 | Requires $4.7\text{ k}\Omega$ pull-up to 3.3V |
| HC-SR04 Trigger | GP3 | 3.3V digital output trigger |
| HC-SR04 Echo | GP2 | **Must use voltage divider** (5V $\rightarrow$ 2.5V) |
| I2C0 SDA / SCL | GP0 / GP1 | 400 kHz bus lines |

---

## Driver Dependencies

* Labs 01–06, 08–10, 12–14, 16 use only built-in MicroPython standard libraries.
* Lab 07 (OLED) requires `ssd1306.py`, which is included in `outputs/experiments/ssd1306.py`.
* Lab 11 (NeoPixel) uses the built-in `neopixel` driver included in all official Pico MicroPython builds.
