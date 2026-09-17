"""Lab 13: Piezo Buzzer Melody Player using PWM frequency modulation on GP17.

Demonstrates how microcontroller PWM generates acoustic sound frequencies,
converting note pitches (Hz) into sound waves with variable tempo and duration.
"""
from machine import Pin, PWM
from time import sleep_ms

# Pin GP17 connected to Piezo buzzer (+) through 100-330 ohm resistor; (-) to GND
buzzer = PWM(Pin(17))

# Note frequency dictionary (Hz)
NOTES = {
    'REST': 0,
    'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349,
    'G4': 392, 'A4': 440, 'B4': 494, 'C5': 523,
    'D5': 587, 'E5': 659, 'F5': 698, 'G5': 784
}

# Musical score: tuples of (Note Name, Duration in 16th notes)
MELODY = [
    ('E5', 2), ('E5', 2), ('REST', 2), ('E5', 2),
    ('REST', 2), ('C5', 2), ('E5', 4),
    ('G5', 4), ('REST', 4), ('G4', 4), ('REST', 4),
    ('C5', 3), ('REST', 1), ('G4', 3), ('REST', 1),
    ('E4', 3), ('REST', 1), ('A4', 2), ('B4', 2),
    ('REST', 4)
]

TEMPO_MS = 100  # Base duration of a single 16th beat in milliseconds

def play_tone(frequency, duration_ms):
    """Play a specific frequency for duration_ms, then pause briefly."""
    if frequency > 0:
        buzzer.freq(frequency)
        buzzer.duty_u16(32768)  # 50% duty cycle square wave
    else:
        buzzer.duty_u16(0)      # Silence / rest

    sleep_ms(duration_ms)
    buzzer.duty_u16(0)          # Staccato gap between notes
    sleep_ms(20)

print("Lab 13: Playing melody on piezo buzzer (GP17)...")
try:
    for note, beats in MELODY:
        freq = NOTES.get(note, 0)
        dur = beats * TEMPO_MS
        play_tone(freq, dur)
    print("Melody finished successfully.")
finally:
    buzzer.duty_u16(0)
    buzzer.deinit()
