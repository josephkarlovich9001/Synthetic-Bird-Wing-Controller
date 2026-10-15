"""
Multi-stepper controller for MicroPython (Pico) with a desktop simulation fallback.
 
Bcode file format, one segment per line (trailing comma allowed):
    <motor_id>,<signed_steps>,<steps_per_second>,
e.g.
    1,200,400,
    2,-100,150,
Lines starting with '#' and blank lines are ignored. Each motor runs its own
segments in order, all motors run concurrently at their own speeds.
"""
 
import time
 
# ---------------------------------------------------------------- platform --
try:
    import machine
    HARDWARE = True
except ImportError:          # running on a desktop: simulate the pins
    machine = None
    HARDWARE = False
 
if hasattr(time, "ticks_us"):            # MicroPython
    ticks_us = time.ticks_us
    ticks_diff = time.ticks_diff
    ticks_add = time.ticks_add
else:                                    # CPython
    def ticks_us():
        return time.perf_counter_ns() // 1000
 
    def ticks_diff(a, b):
        return a - b
 
    def ticks_add(a, b):
        return a + b
 
 
class SimPin:
    """Stand-in for machine.Pin when not on hardware."""
 
    def __init__(self, num):
        self.num = num
        self.level = 0
 
    def value(self, level):
        self.level = level
 
 
# ----------------------------------------------------------------- Stepper --
class Stepper:
    # Wave drive, one coil at a time (same pattern as the original code).
    PATTERN = ((1, 0, 0, 0),
               (0, 1, 0, 0),
               (0, 0, 1, 0),
               (0, 0, 0, 1))
    STOP = (0, 0, 0, 0)
 
    def __init__(self, pins):
        self.pos = 0                     # NOT 'step': that would shadow the method
        self.pins = []
        for num in pins:
            if HARDWARE:
                self.pins.append(machine.Pin(num, machine.Pin.OUT))
            else:
                self.pins.append(SimPin(num))
 
    def step(self, distance=0):
        """Take one step toward `distance`; return the steps still remaining."""
        if distance < 0:
            self.pos -= 1
            distance += 1
        elif distance > 0:
            self.pos += 1
            distance -= 1
        else:
            return 0
 
        self.pos %= 4
        for pin, level in zip(self.pins, self.PATTERN[self.pos]):
            pin.value(level)
        return distance
 
    def Stop(self):
        """De-energise all coils."""
        for pin, level in zip(self.pins, self.STOP):
            pin.value(level)
 
 
# -------------------------------------------------------------- Controller --
class Controller:
 
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.numMotors = 0
        self.ID = []
        self.motors = []
        self.stepsPerRev = []
        self.segments = []       # per motor: list of (signed_steps, interval_us)
        self.idx = []            # per motor: current segment index
        self.remaining = []      # per motor: steps left in current segment
        self.interval = []       # per motor: current step interval in us
        self.max_late_us = 0     # worst scheduling lateness seen in the last run
 
    def AddMotor(self, ID="a", pins=(1, 2, 3, 4), stepsPerRev=200):
        self.numMotors += 1
        self.ID.append(str(ID))
        self.motors.append(Stepper(pins))
        self.stepsPerRev.append(stepsPerRev)
        self.segments.append([])
        self.idx.append(0)
        self.remaining.append(0)
        self.interval.append(0)
 
    # ------------------------------------------------------------- parsing --
    def ReadFile(self, file="Bcode.txt"):
        for seg in self.segments:
            del seg[:]
 
        with open(file, "r") as f:
            for lineno, raw in enumerate(f, 1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
 
                fields = [p.strip() for p in line.split(",") if p.strip() != ""]
                if len(fields) < 3:
                    print("Line %d skipped: need id,steps,speed" % lineno)
                    continue
 
                motor_id = fields[0]
                if motor_id not in self.ID:
                    print("Line %d skipped: unknown motor %r" % (lineno, motor_id))
                    continue
 
                try:
                    steps = int(fields[1])
                    speed = int(fields[2])
                except ValueError:
                    print("Line %d skipped: non-integer value" % lineno)
                    continue
 
                if speed <= 0:
                    print("Line %d skipped: speed must be > 0" % lineno)
                    continue
 
                m = self.ID.index(motor_id)
                self.segments[m].append((steps, 1000000 // speed))
 
    # ----------------------------------------------------------- execution --
    def _next_segment(self, m):
        """Load the next segment that has steps for motor m. False if none left."""
        while self.idx[m] < len(self.segments[m]):
            steps, interval = self.segments[m][self.idx[m]]
            if steps != 0:
                self.remaining[m] = steps
                self.interval[m] = interval
                return True
            self.idx[m] += 1
        return False
 
    def Run(self, file="Bcode.txt"):
        self.ReadFile(file)
        self.max_late_us = 0
 
        for m in range(self.numMotors):
            self.idx[m] = 0
        active = [m for m in range(self.numMotors) if self._next_segment(m)]
 
        start = ticks_us()
        next_due = [start] * self.numMotors
 
        try:
            while active:
                for m in tuple(active):
                    now = ticks_us()
                    late = ticks_diff(now, next_due[m])
                    if late < 0:
                        continue                      # not due yet
                    if late > self.max_late_us:
                        self.max_late_us = late
 
                    self.remaining[m] = self.motors[m].step(self.remaining[m])
                    # Advance from the previous deadline, not from 'now',
                    # so timing errors don't accumulate as drift.
                    next_due[m] = ticks_add(next_due[m], self.interval[m])
 
                    if self.remaining[m] == 0:
                        self.idx[m] += 1
                        if not self._next_segment(m):
                            active.remove(m)
                            self.motors[m].Stop()
                            if self.verbose:
                                print("Motor %s finished" % self.ID[m])
        finally:
            for motor in self.motors:                 # always release the coils
                motor.Stop()
 
        print("Done. Worst step lateness: %d us" % self.max_late_us)
 
 
# -------------------------------------------------------------------- main --
if __name__ == "__main__":
    test = Controller(verbose=True)
    test.AddMotor(ID="1", pins=[1, 2, 3, 4])
    test.AddMotor(ID="2", pins=[5, 6, 7, 8])
    test.AddMotor(ID="3", pins=[9, 10, 11, 12])
    test.Run("Bcode.txt")