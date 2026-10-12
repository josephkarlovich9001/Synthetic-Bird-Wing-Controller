import time
import StepperController

time1 = 1
stop1 = 1

time2= 2
stop2=1

#= = = = = = = = = =
#== == == == == == ==

#speed is one tick per second, ex: 500 is 500 ticks per second
#issue: current movement is just back and fourth
speed = 1
speed2 = 3



from machine import Pin
import time

# --- Motor 1 Pins (ULN2003 Driver 1) ---
m1_pins = [Pin(2, Pin.OUT), Pin(3, Pin.OUT), Pin(4, Pin.OUT), Pin(5, Pin.OUT)]

# --- Motor 2 Pins (ULN2003 Driver 2) ---
m2_pins = [Pin(6, Pin.OUT), Pin(7, Pin.OUT), Pin(8, Pin.OUT), Pin(9, Pin.OUT)]

# Full-step sequence for 4-pin unipolar motors
step_sequence = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

def apply_step(pins, step_index):
    for i in range(4):
        pins[i].value(step_sequence[step_index][i])

# Motor state dictionaries
motor1 = {
    "pins": m1_pins,
    "step_idx": 0,
    "direction": 1,          # 1 for forward, -1 for backward
    "delay_ms": 3,           # Speed control (smaller = faster)
    "last_step_time": time.ticks_ms()
}

motor2 = {
    "pins": m2_pins,
    "step_idx": 0,
    "direction": -1,         # Opposite direction
    "delay_ms": 5,           # Different speed
    "last_step_time": time.ticks_ms()
}

def update_motor(m):
    now = time.ticks_ms()
    if time.ticks_diff(now, m["last_step_time"]) >= m["delay_ms"]:
        m["last_step_time"] = now
        m["step_idx"] = (m["step_idx"] + m["direction"]) % len(step_sequence)
        apply_step(m["pins"], m["step_idx"])

# --- Main Loop ---
while True:
    update_motor(motor1)
    update_motor(motor2)
    # Yield slightly or do other tasks here
    time.sleep_ms(1)
