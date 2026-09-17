# Embedded Systems Engineering with MicroPython
### A Practical Laboratory Course for Raspberry Pi Pico & Pico 2 W

---

## Course Overview & Table of Contents

Welcome to the **MicroPython Embedded Systems Course**. This hands-on curriculum takes learners from core digital I/O concepts to hardware communication buses, analog conversion, sensor physics, multithreading, and Internet of Things (IoT) networking.

### Curriculum Structure

| Lab | Title | Domain | Core Hardware / Protocol |
|---|---|---|---|
| **01** | [On-board LED Heartbeat](#lab-01--on-board-led-heartbeat) | Digital Output | Push-pull GPIO, duty cycle |
| **02** | [Button Input & Contact Debounce](#lab-02--button-input--contact-debounce) | Digital Input | Internal pull-up, contact bounce physics |
| **03** | [PWM LED Dimmer & Breathing Light](#lab-03--pwm-led-dimmer--breathing-light) | Analog Simulation | Pulse Width Modulation, frequency vs duty |
| **04** | [Potentiometer ADC Voltage Meter](#lab-04--potentiometer-adc-voltage-meter) | Analog Acquisition | Successive-approximation ADC, quantization |
| **05** | [DS18B20 1-Wire Digital Thermometer](#lab-05--ds18b20-1-wire-digital-thermometer) | Communication Bus | Dallas 1-Wire, open-drain pull-up, ROM addressing |
| **06** | [Ultrasonic Time-of-Flight Distance Meter](#lab-06--ultrasonic-time-of-flight-distance-meter) | Sensor Physics | HC-SR04 sound speed, 5V-to-3.3V voltage divider |
| **07** | [SSD1306 I2C Graphical OLED Dashboard](#lab-07--ssd1306-i2c-graphical-oled-dashboard) | Serial Display | I2C master, frame buffers, telemetry rendering |
| **08** | [2.4 GHz Wi-Fi Access Point Scanner](#lab-08--24-ghz-wi-fi-access-point-scanner) | Wireless & RF | 802.11 b/g/n beacon frames, RSSI, channels |
| **09** | [I2C Bus Explorer & Diagnostic Prober](#lab-09--i2c-bus-explorer--diagnostic-prober) | Bus Diagnostics | I2C ACK/NACK protocol, device discovery |
| **10** | [Hardware Interrupt Event Counter](#lab-10--hardware-interrupt-event-counter) | Asynchronous Events | Edge-triggered IRQ, ISR latency, debouncing |
| **11** | [WS2812B / NeoPixel RGB LED Controller](#lab-11--ws2812b--neopixel-rgb-led-controller) | High-Speed Serial | Single-wire 800 kHz protocol, 24-bit GRB |
| **12** | [LDR Light Sensor & Nightlight with Hysteresis](#lab-12--ldr-light-sensor--nightlight-with-hysteresis) | Analog Interfacing | Photoresistor divider, Schmitt trigger hysteresis |
| **13** | [Piezo Buzzer Melody Synthesizer](#lab-13--piezo-buzzer-melody-synthesizer) | Audio Synthesis | PWM square wave frequencies, acoustic notes |
| **14** | [Dual-Core Multiprocessing with `_thread`](#lab-14--dual-core-multiprocessing-with-_thread) | Concurrency | RP2040/RP2350 dual-core scheduling, race conditions |
| **15** | [MicroPython Socket Wi-Fi Web Server](#lab-15--micropython-socket-wi-fi-web-server) | IoT & Networking | TCP/IP sockets, HTTP protocol, HTML control UI |
| **16** | [Non-Volatile Flash File Logger & JSON State](#lab-16--non-volatile-flash-file-logger--json-state) | Persistent Storage | LittleFS flash filesystem, JSON serialization |

---

## 1. Fundamentals of Embedded Systems

### 1.1 Microcontroller Architecture vs. Microprocessors
A **microcontroller (MCU)** integrates the CPU core, flash program memory, RAM, and peripheral controllers (GPIO, ADC, PWM, I2C, SPI, UART) onto a single silicon chip. Unlike a desktop PC or Raspberry Pi 4 (which boot operating systems like Linux and require virtual memory), the MCU executes bare-metal or real-time firmware directly against physical memory addresses.

* **Raspberry Pi Pico**: Dual-core ARM Cortex-M0+ running at 133 MHz, 264 KB SRAM, 2 MB external QSPI flash.
* **Raspberry Pi Pico 2 / 2 W**: Dual-core ARM Cortex-M33 (or RISC-V Hazard3) running at 150 MHz, 520 KB SRAM, 4 MB flash, with CYW43439 Wi-Fi/Bluetooth.

### 1.2 Voltage and Electrical Safety Rules
> [!CAUTION]
> **3.3V Logic Limit**: All Pico GPIO pins operate strictly at **3.3 V CMOS logic levels**. 
> - Applying **5.0 V directly to any GPIO pin will permanently destroy the pin or the entire microcontroller**.
> - Always use a **resistor voltage divider** or a logic level shifter when reading signals from 5V modules (such as the HC-SR04 Echo pin).
> - Each GPIO pin can source or sink a maximum of **12 mA** safely (default 4 mA). Never connect DC motors, relays, or high-power buzzers directly to GPIO pins without a transistor or MOSFET driver.

### 1.3 Raspberry Pi Pico & Pico 2 Pinout Reference

```
                   +---\___/---+
         GP0 (SDA) | 1      40 | VBUS (5V USB input)
         GP1 (SCL) | 2      39 | VSYS (1.8V - 5.5V)
               GND | 3      38 | GND
         GP2 (Echo)| 4      37 | 3V3_EN
         GP3 (Trig)| 5      36 | 3V3(OUT) (Clean 3.3V supply)
        GP4 (1Wire)| 6      35 | ADC_VREF
               GND | 8      33 | AGND
        GP14 (IRQ) | 19     22 | GP17 (Buzzer PWM)
        GP15 (Btn) | 20     21 | GP16 (LED / PWM)
        GP18 (RGB) | 24     31 | GP26 (ADC0 / Pot)
               GND | 28     32 | GP27 (ADC1 / LDR)
                   +-----------+
```

---

## Lab 01 — On-board LED Heartbeat

### Learning Outcomes
- Understand microcontroller digital output push-pull circuitry.
- Distinguish between physical logic levels: Logic HIGH (`1` / 3.3 V) and Logic LOW (`0` / 0 V).
- Master the `machine.Pin` object lifecycle and blocking delays with `time.sleep()`.

### Circuit & Wiring
* **Pico / Pico 2**: Physical GP25.
* **Pico W / Pico 2 W**: On-board LED is wired to the Infineon CYW43439 wireless chip and addressed symbolically as `"LED"`.
* **External connection**: No external wiring required.

```
+----------------+
|  Pico 2 W      |
|  [ Wireless ]  |----(Internal Line)----> [ On-board Green LED ] ---> GND
|                |
+----------------+
```

### Source Code (`experiments/01_blink_led.py`)
```python
from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)

while True:
    led.on()       # Drives output to 3.3V
    sleep(0.15)    # 150 ms pulse
    led.off()      # Drives output to 0V
    sleep(0.85)    # 850 ms pause
```

### Deep-Dive Analysis
1. `Pin("LED", Pin.OUT)` configures the internal driver pad as a push-pull digital output.
2. In MicroPython, allocating objects consumes heap memory. Instantiating `led` outside the `while True` loop ensures that garbage collection pauses do not jitter the blink timing.

### Student Challenge
Modify the sleep timings to implement an authentic human heartbeat rhythm: two short quick beats (lub-dub) followed by a 1.2-second pause.

---

## Lab 02 — Button Input & Contact Debounce

### Learning Outcomes
- Understand floating inputs and high-impedance state ($Z_{in} > 10\text{ M}\Omega$).
- Configure internal pull-up resistors (`Pin.PULL_UP`).
- Analyze mechanical contact bounce and write software debouncing routines.

### Circuit Schematic & Wiring
* Button Terminal 1 $\rightarrow$ **GP15** (Pin 20)
* Button Terminal 2 $\rightarrow$ **GND** (Pin 18 or Pin 23)

```
       3.3V (Internal)
         |
        [R] (Internal ~50k Pull-Up)
         |
GP15 ----+---------o   o--------- GND
                  Button
             (Normally Open)
```

### Source Code (`experiments/02_button_debounce.py`)
```python
from machine import Pin
from time import sleep_ms

button = Pin(15, Pin.IN, Pin.PULL_UP)
last_state = button.value()

while True:
    state = button.value()
    if state != last_state:
        sleep_ms(25)  # Wait for mechanical bounce to settle
        state = button.value()
        if state != last_state:
            last_state = state
            if state == 0:
                print("Button pressed (Active LOW)")
            else:
                print("Button released (Pulled HIGH)")
    sleep_ms(5)
```

### Theory: Why is Pull-Up Necessary?
When an open switch is connected between a pin and ground without a pull resistor, the pin is connected to nothing. Atmospheric electromagnetic fields will cause the pin voltage to float unpredictably between 0 V and 3.3 V. The internal pull-up resistor gently holds the line at 3.3 V (Logic 1) until the button actively shorts it to 0 V (Logic 0).

---

## Lab 03 — PWM LED Dimmer & Breathing Light

### Learning Outcomes
- Contrast analog voltage variation with Pulse Width Modulation (PWM).
- Calculate duty cycle percentage ($D = \frac{T_{on}}{T_{period}} \times 100\%$) and 16-bit resolution ($0$ to $65535$).
- Understand human eye persistence of vision and perceived brightness.

### Circuit Schematic & Wiring
* **GP16** (Pin 21) $\rightarrow$ 220 $\Omega$ Resistor $\rightarrow$ LED Anode (Long leg)
* LED Cathode (Flat side/short leg) $\rightarrow$ **GND** (Pin 23)

```
GP16 (PWM) ---[ 220 Ohm ]--->|--- (LED) ---> GND
```

### Source Code (`experiments/03_pwm_breathe.py`)
```python
from machine import Pin, PWM
from time import sleep_ms

STEPS = 100
DELAY_MS = 12
pwm = PWM(Pin(16))
pwm.freq(1_000)  # 1 kHz frequency (1 ms period)

while True:
    for step in range(STEPS + 1):
        pwm.duty_u16(step * 65535 // STEPS)
        sleep_ms(DELAY_MS)
    for step in range(STEPS, -1, -1):
        pwm.duty_u16(step * 65535 // STEPS)
        sleep_ms(DELAY_MS)
```

### Technical Note: PWM vs Constant Voltage
PWM does **not** output 1.65 V at 50% duty cycle. It delivers full 3.3 V for 500 $\mu$s, then 0 V for 500 $\mu$s. Because this alternates 1000 times per second, the human eye averages the photon flux, perceiving smooth brightness attenuation.

---

## Lab 04 — Potentiometer ADC Voltage Meter

### Learning Outcomes
- Understand Successive Approximation Register (SAR) Analog-to-Digital Conversion.
- Convert raw 16-bit integer values (`0 - 65535`) to real-world analog voltages ($V = \frac{\text{raw} \times 3.3\text{ V}}{65535}$).
- Render live ASCII terminal telemetry and bargraph indicators.

### Circuit Schematic & Wiring
* Potentiometer Pin 1 $\rightarrow$ **3V3(OUT)** (Pin 36)
* Potentiometer Pin 2 (Center Wiper) $\rightarrow$ **GP26 / ADC0** (Pin 31)
* Potentiometer Pin 3 $\rightarrow$ **GND** (Pin 33 / AGND)

```
3V3(OUT) ---[ Potentiometer Track ]--- GND
                     |
                   (Wiper)
                     |
                 GP26 (ADC0)
```

### Source Code (`experiments/04_adc_potentiometer.py`)
```python
from machine import ADC
from time import sleep_ms

adc = ADC(26)  # GP26 is RP2040/RP2350 ADC Channel 0

while True:
    raw = adc.read_u16()
    volts = raw * 3.3 / 65535
    bar = "#" * (raw * 20 // 65535)
    print("raw={:5d}  voltage={:.2f} V  {:<20}".format(raw, volts, bar))
    sleep_ms(250)
```

---

## Lab 05 — DS18B20 1-Wire Digital Thermometer

### Learning Outcomes
- Learn the Dallas 1-Wire bus architecture: single data wire + ground.
- Master open-drain signaling requiring an external $4.7\text{ k}\Omega$ pull-up resistor.
- Query 64-bit factory ROM identifiers and initiate thermal conversions.

### Circuit Schematic & Wiring
* DS18B20 **VDD** $\rightarrow$ **3V3(OUT)** (Pin 36)
* DS18B20 **GND** $\rightarrow$ **GND** (Pin 38)
* DS18B20 **DQ (Data)** $\rightarrow$ **GP4** (Pin 6)
* **Pull-up Resistor**: Place a $4.7\text{ k}\Omega$ resistor between **DQ** and **3V3**.

```
3V3 --------------------+------------------- (VDD)
                        |
                     [ 4.7k ]
                        |
GP4 --------------------+------------------- (DQ Data)
                                             DS18B20
GND ---------------------------------------- (GND)
```

### Source Code (`experiments/05_ds18b20_temperature.py`)
```python
from machine import Pin
from time import sleep_ms
import ds18x20, onewire

bus = ds18x20.DS18X20(onewire.OneWire(Pin(4)))
devices = bus.scan()

if not devices:
    raise RuntimeError("No DS18B20 found! Check 4.7k pull-up and wiring.")

print("Found {} sensor(s)".format(len(devices)))
while True:
    bus.convert_temp()
    sleep_ms(750)  # 12-bit conversion requires up to 750 ms
    for device in devices:
        c = bus.read_temp(device)
        f = c * 9 / 5 + 32
        print("Device {}: {:.2f} °C / {:.2f} °F".format(device.hex(), c, f))
```

---

## Lab 06 — Ultrasonic Time-of-Flight Distance Meter

### Learning Outcomes
- Measure distance via acoustic time-of-flight: $d = \frac{v \times t}{2}$, where $v_{\text{sound}} \approx 343\text{ m/s}$.
- Generate high-precision $10\ \mu\text{s}$ trigger pulses.
- **Safety Critical**: Build a 2-resistor voltage divider to scale the 5 V Echo pulse down to safe 3.3 V logic.

### Circuit Schematic & Voltage Divider
* HC-SR04 **VCC** $\rightarrow$ **VBUS** (5 V from USB, Pin 40)
* HC-SR04 **GND** $\rightarrow$ **GND** (Pin 38)
* HC-SR04 **TRIG** $\rightarrow$ **GP3** (Pin 5)
* HC-SR04 **ECHO** (5V out) $\rightarrow$ Resistor $R_1\ (1\text{ k}\Omega)$ $\rightarrow$ **GP2** (Pin 4) $\rightarrow$ Resistor $R_2\ (2\text{ k}\Omega\text{ or }1\text{ k}\Omega)$ $\rightarrow$ **GND**.

```
VBUS (5V) ------------------------ (VCC)
GP3 (Trig) ----------------------- (TRIG)
                                  HC-SR04
GP2 (Echo) <----+                 (ECHO) ---> 5V Pulse
                |
             [ 1k R1 ]
                |
                +----------------- (ECHO Pin on Sensor)
                |
             [ 1k or 2k R2 ]
                |
GND ------------+----------------- (GND)
```
$$V_{\text{out}} = 5\text{ V} \times \frac{R_2}{R_1 + R_2} = 5\text{ V} \times \frac{1000}{2000} = 2.5\text{ V (Safe for 3.3V GPIO)}$$

### Source Code (`experiments/06_ultrasonic_distance.py`)
```python
from machine import Pin, time_pulse_us
from time import sleep_ms, sleep_us

trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)
trigger.off()

while True:
    trigger.on()
    sleep_us(10)
    trigger.off()
    
    # Measure pulse duration in microseconds (timeout 30ms)
    duration_us = time_pulse_us(echo, 1, 30_000)
    if duration_us < 0:
        print("Out of range / no echo detected")
    else:
        # Distance = (time * 0.0343 cm/us) / 2
        distance_cm = duration_us * 0.0343 / 2
        print("Distance: {:6.1f} cm".format(distance_cm))
    sleep_ms(500)
```

---

## Lab 07 — SSD1306 I2C Graphical OLED Dashboard

### Learning Outcomes
- Understand I2C (Inter-Integrated Circuit) communication: SDA (Serial Data) & SCL (Serial Clock).
- Initialize frame buffer memory and coordinate geometry $(X: 0\text{--}127,\ Y: 0\text{--}63)$.
- Render dynamic text, telemetry, and graphics to an OLED display.

### Circuit Schematic & Wiring
* OLED **VCC** $\rightarrow$ **3V3(OUT)** (Pin 36)
* OLED **GND** $\rightarrow$ **GND** (Pin 38)
* OLED **SDA** $\rightarrow$ **GP0** (Pin 1)
* OLED **SCL** $\rightarrow$ **GP1** (Pin 2)

```
3V3 ---------------- (VCC)
GND ---------------- (GND)
GP0 (I2C0 SDA) ----- (SDA)  SSD1306 OLED (128x64)
GP1 (I2C0 SCL) ----- (SCL)
```

### Source Code (`experiments/07_oled_dashboard.py`)
*(Requires `ssd1306.py` driver present in the filesystem)*
```python
from machine import I2C, Pin
from time import sleep_ms
import ssd1306

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400_000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

count = 0
while True:
    oled.fill(0)                         # Clear display buffer
    oled.rect(0, 0, 128, 64, 1)          # Draw outer border
    oled.text("EMBEDDED LAB", 16, 8)     # Header
    oled.hline(10, 22, 108, 1)           # Divider line
    oled.text("Uptime: {} s".format(count), 16, 32)
    oled.fill_rect(16, 48, count % 96, 6, 1) # Progress bar
    oled.show()                          # Transfer buffer to screen
    count += 1
    sleep_ms(500)
```

---

## Lab 08 — 2.4 GHz Wi-Fi Access Point Scanner

### Learning Outcomes
- Initialize the embedded wireless subsystem (`network.WLAN`).
- Scan for 802.11 b/g/n beacon frames.
- Decode SSIDs, analyze signal strength (RSSI in dBm), and inspect security protocols.

### Source Code (`experiments/08_wifi_scan.py`)
```python
import network
from time import sleep_ms

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

while True:
    print("Scanning 2.4 GHz airwaves...")
    networks = wlan.scan()
    print("-" * 65)
    print("{:<26} {:<10} {:<8} {}".format("SSID", "RSSI (dBm)", "Channel", "Security"))
    print("-" * 65)
    for ssid, bssid, channel, rssi, security, hidden in networks:
        name = ssid.decode('utf-8', 'ignore') if ssid else "<Hidden>"
        print("{:<26} {:<10d} {:<8d} {}".format(name, rssi, channel, security))
    print("-" * 65)
    print("Found {} network(s)\n".format(len(networks)))
    sleep_ms(10_000)
```

---

## Lab 09 — I2C Bus Explorer & Diagnostic Prober

### Learning Outcomes
- Understand I2C addressing: 7-bit slave addresses (`0x08` to `0x77`).
- Observe ACK/NACK signaling when probing unknown devices.
- Troubleshoot common hardware faults: inverted SDA/SCL, missing common ground, or missing pull-ups.

### Source Code (`experiments/09_i2c_explorer.py`)
```python
from machine import I2C, Pin
from time import sleep_ms

# Hardware I2C0 bus on GP0 (SDA) and GP1 (SCL)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100_000)

while True:
    addresses = i2c.scan()
    if addresses:
        print("Detected I2C Devices:")
        for addr in addresses:
            print("  -> Decimal: {:3d} | Hex: 0x{:02X}".format(addr, addr))
    else:
        print("[!] No I2C devices responded. Verify VCC, GND, SDA, and SCL.")
    sleep_ms(3000)
```

---

## Lab 10 — Hardware Interrupt Event Counter

### Learning Outcomes
- Understand hardware interrupt requests (IRQ) vs CPU busy-wait polling.
- Write robust Interrupt Service Routines (ISRs).
- **Embedded Rule**: *Never allocate memory, call `print()`, or block with `sleep()` inside an ISR!*

### Circuit Schematic & Wiring
* Pushbutton connected between **GP14** (Pin 19) and **GND** (Pin 18).

### Source Code (`experiments/10_interrupt_counter.py`)
```python
from machine import Pin
from time import sleep_ms, ticks_diff, ticks_ms

button = Pin(14, Pin.IN, Pin.PULL_UP)
presses = 0
last_event_ms = 0

def button_isr(pin):
    """Interrupt handler: executes instantly on falling edge."""
    global presses, last_event_ms
    now = ticks_ms()
    if ticks_diff(now, last_event_ms) > 180:  # Debounce filter
        presses += 1
        last_event_ms = now

button.irq(trigger=Pin.IRQ_FALLING, handler=button_isr)

print("Interrupt attached to GP14. Main loop free to do other work!")
while True:
    print("Current Press Count: {}".format(presses))
    sleep_ms(500)
```

---

## Lab 11 — WS2812B / NeoPixel RGB LED Controller

### Learning Outcomes
- Understand high-speed single-wire asynchronous NRZ (Non-Return-to-Zero) timing (800 kHz / 1.25 $\mu$s per bit).
- Encode 24-bit color depth (8-bit Red, 8-bit Green, 8-bit Blue).
- Implement algorithmic rainbow color-wheel transitions without floating-point math.

### Circuit Schematic & Wiring
* NeoPixel **VCC** $\rightarrow$ **VBUS** (5V USB) or **3V3(OUT)**
* NeoPixel **GND** $\rightarrow$ **GND** (Pin 28)
* NeoPixel **DIN** (Data In) $\rightarrow$ **GP18** (Pin 24)

```
3V3/5V ----------------- (VCC)
GND -------------------- (GND)  WS2812B NeoPixel Strip/Ring
GP18 ------------------- (DIN)
```

### Source Code (`experiments/11_neopixel_rgb.py`)
```python
from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

PIN_NUM = 18
NUM_PIXELS = 8
np = NeoPixel(Pin(PIN_NUM, Pin.OUT), NUM_PIXELS)

def wheel(pos):
    pos = pos & 255
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

while True:
    for j in range(256):
        for i in range(NUM_PIXELS):
            pixel_index = (i * 256 // NUM_PIXELS) + j
            np[i] = wheel(pixel_index)
        np.write()
        sleep_ms(15)
```

---

## Lab 12 — LDR Light Sensor & Nightlight with Hysteresis

### Learning Outcomes
- Interface a Photoresistor (LDR) using an analog voltage divider.
- Understand the problem of comparator chatter near decision thresholds.
- Implement **hysteresis** (Schmitt trigger software logic) with separate turn-on and turn-off thresholds.

### Circuit Schematic & Wiring
* 3V3(OUT) $\rightarrow$ $10\text{ k}\Omega$ Fixed Resistor $\rightarrow$ **GP27 (ADC1)** $\rightarrow$ LDR $\rightarrow$ **GND**
* Indicator LED: **GP16** $\rightarrow$ $220\ \Omega$ $\rightarrow$ LED Anode; Cathode $\rightarrow$ **GND**

```
3V3 ---[ 10k Resistor ]---+---[ LDR ]---> GND
                          |
                      GP27 (ADC1)
```

### Source Code (`experiments/12_ldr_nightlight.py`)
```python
from machine import ADC, Pin
from time import sleep_ms

ldr = ADC(27)            # GP27 is ADC1
led = Pin(16, Pin.OUT)   # Indicator LED on GP16

DARK_THRESHOLD = 20000   # Turn ON below this reading
LIGHT_THRESHOLD = 25000  # Turn OFF above this reading
lamp_state = False

while True:
    raw = ldr.read_u16()
    
    if lamp_state and raw > LIGHT_THRESHOLD:
        lamp_state = False
        led.off()
        print("[STATE] Light restored -> Nightlight OFF")
    elif not lamp_state and raw < DARK_THRESHOLD:
        lamp_state = True
        led.on()
        print("[STATE] Dark detected -> Nightlight ON")
        
    sleep_ms(300)
```

---

## Lab 13 — Piezo Buzzer Melody Synthesizer

### Learning Outcomes
- Generate acoustic sound waves using PWM frequency modulation.
- Map musical note letter pitches ($C_4, D_4, E_4 \dots$) to specific frequencies (Hz).
- Implement rhythm, note durations, and staccato articulation pauses.

### Circuit Schematic & Wiring
* Piezo Buzzer (+) $\rightarrow$ $100\ \Omega$ Resistor $\rightarrow$ **GP17** (Pin 22)
* Piezo Buzzer (-) $\rightarrow$ **GND** (Pin 23)

```
GP17 (PWM) ---[ 100 Ohm ]---(+) [ Piezo Buzzer ] (-) ---> GND
```

### Source Code (`experiments/13_pwm_buzzer_melody.py`)
```python
from machine import Pin, PWM
from time import sleep_ms

buzzer = PWM(Pin(17))

NOTES = {
    'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349,
    'G4': 392, 'A4': 440, 'B4': 494, 'C5': 523,
    'E5': 659, 'G5': 784, 'REST': 0
}

def play_tone(freq, duration_ms):
    if freq > 0:
        buzzer.freq(freq)
        buzzer.duty_u16(32768)  # 50% duty cycle square wave
    else:
        buzzer.duty_u16(0)
    sleep_ms(duration_ms)
    buzzer.duty_u16(0)
    sleep_ms(20)  # Brief silence between notes

melody = [('E5', 200), ('E5', 200), ('C5', 200), ('E5', 400), ('G5', 500)]
for note, dur in melody:
    play_tone(NOTES[note], dur)
buzzer.deinit()
```

---

## Lab 14 — Dual-Core Multiprocessing with `_thread`

### Learning Outcomes
- Leverage the dual-core architecture of RP2040 and RP2350 processors.
- Spawn a dedicated hardware thread on Core 1 while keeping Core 0 responsive.
- Understand shared memory, global flags, and thread lifecycle management.

### Architecture
```
+-----------------------------------------------------------+
|                      RP2040 / RP2350                      |
|                                                           |
|    [ Core 0 (Main Execution) ]    [ Core 1 (Secondary) ]  |
|                 |                            |            |
|       Monitors GP15 Button         Runs Heartbeat LED     |
|       Prints User Telemetry        No Main Loop Jitter    |
|                 \                            /            |
|                  +---- Shared Heap RAM -----+             |
+-----------------------------------------------------------+
```

### Source Code (`experiments/14_multicore_threading.py`)
```python
import _thread
from machine import Pin
from time import sleep_ms

thread_running = True

def core1_heartbeat():
    led = Pin("LED", Pin.OUT)
    while thread_running:
        led.on()
        sleep_ms(80)
        led.off()
        sleep_ms(500)

_thread.start_new_thread(core1_heartbeat, ())

button = Pin(15, Pin.IN, Pin.PULL_UP)
while True:
    print("Core 0 running. Button state:", button.value())
    sleep_ms(500)
```

---

## Lab 15 — MicroPython Socket Wi-Fi Web Server

### Learning Outcomes
- Establish Wi-Fi station connectivity on Pico W / Pico 2 W.
- Implement a BSD-style TCP socket server listening on HTTP port 80.
- Parse HTTP GET request headers and serve an interactive mobile-friendly web UI.

### Architecture
```
[ Smartphone / Laptop ]
         |
         | HTTP GET /?led=on
         v
[ Pico 2 W Socket (Port 80) ] ---> Decodes request ---> Sets GP Pin ---> Returns HTML UI
```

### Source Code (`experiments/15_wifi_web_server.py`)
```python
import network, socket
from machine import Pin

led = Pin("LED", Pin.OUT)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("YOUR_WIFI_SSID", "YOUR_WIFI_PASSWORD")

while not wlan.isconnected():
    pass
print("Web Server active at: http://{}/".format(wlan.ifconfig()[0]))

s = socket.socket()
s.bind(('0.0.0.0', 80))
s.listen(2)

while True:
    cl, addr = s.accept()
    req = cl.recv(1024).decode('utf-8', 'ignore')
    if "GET /?led=on" in req:
        led.on()
    elif "GET /?led=off" in req:
        led.off()
    
    html = f"<html><body><h1>Pico Web Server</h1><p>LED is {'ON' if led.value() else 'OFF'}</p><a href='/?led=on'>ON</a> | <a href='/?led=off'>OFF</a></body></html>"
    cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n' + html)
    cl.close()
```

---

## Lab 16 — Non-Volatile Flash File Logger & JSON State

### Learning Outcomes
- Read and write files to the on-board LittleFS SPI flash filesystem.
- Maintain persistent device settings (boot counters, calibration factors) across power resets using JSON.
- Understand flash wear-leveling considerations.

### Source Code (`experiments/16_flash_filesystem_logger.py`)
```python
import json, os
from machine import ADC
from time import sleep_ms, ticks_ms

CONFIG_FILE = "device_config.json"

def get_boot_count():
    try:
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
    except OSError:
        cfg = {"boot_count": 0}
        
    cfg["boot_count"] += 1
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f)
    return cfg["boot_count"]

print("Device successfully powered on. Persistent Boot Cycle #:", get_boot_count())
```

---

## Troubleshooting Guide & Best Practices

| Symptom | Probable Root Cause | Resolution |
|---|---|---|
| `ImportError: no module named 'ssd1306'` | Driver file missing from MCU root | Save `ssd1306.py` to the Pico flash root directory using Thonny or `mpremote fs cp`. |
| `RuntimeError: No DS18B20 found` | Missing pull-up resistor | Connect a $4.7\text{ k}\Omega$ resistor between DQ (Data) and 3V3. Check pin connections. |
| Ultrasonic distance reads negative or erratic | 5V Echo pulse damaging pin or floating | Confirm $1\text{ k}\Omega / 1\text{ k}\Omega$ voltage divider is reducing 5V echo pulse to 2.5V. |
| I2C scan returns empty list `[]` | SDA/SCL lines reversed or lack common ground | Swap GP0 and GP1 jumpers. Ensure sensor GND is tied to Pico GND. |
| Board disconnects when powering a sensor | Current spike exceeded USB limit | Do not power motors or high-power loads directly from 3V3(OUT); use external power supply. |
