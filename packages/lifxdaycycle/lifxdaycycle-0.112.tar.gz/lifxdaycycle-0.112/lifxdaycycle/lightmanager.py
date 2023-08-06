from datetime import datetime
import time
import sys
from lifxlan import LifxLAN, Light
# light = Light("d0:73:d5:5b:86:3e", "192.168.0.23") # get with this: for d in LifxLAN(1).get_lights(): print(d)
DURATION = 2000 # transition duration
# PRODUCTION = True

# hour e.g. 13.5 for 13:30 h | brightness 0 - 1 | kelvin 0 - 1
schedule = [
    [0,      0.1,   0],
    [7,      0.1,   0],
    [8,      1,     1],
    [17,     0.6,   0.5],
    [18,     0.5,   0.25],
    [20,     0.01,  0],
    [24,     0.01,  0]
]

def change(light, b, k):
    color = [0, 0, round(b * 65535), round(6500 - 1500) * k + 1500]
    light.set_color(color, DURATION)

def calc_diff(schedule, time_h):
    # cleaning
    time_h = round(time_h, 2)
    if time_h >= 24:
        time_h = 23.99

    # find start end end slot int times
    for i, slot in enumerate(schedule):
        if time_h < slot[0]:
            start = schedule[i - 1]
            end = schedule[i]
            break

    ratio = round((time_h - start[0]) / (end[0] - start[0]), 2)

    # calc brightness and kevlin from the diff
    b = round(start[1] + (end[1] - start[1]) * ratio, 2)
    k = round(start[2] + (end[2] - start[2]) * ratio, 2)
    return b, k


# Simulate full day
def run_simulation(lights):
    for it in [x * 1 for x in range(0, 25)]:
        result = calc_diff(schedule, it)
        print(f"{it}: {result}")
        time.sleep(0.5)

        for light in lights:
            change(light, result[0], result[1])


def main():
    lights = LifxLAN().get_lights()

    if len(sys.argv) == 2:
        if 'on' == sys.argv[1]:
            for light in lights:
                light.set_power(1)
        elif 'off' == sys.argv[1]:
            for light in lights:
                light.set_power(0)
        elif 'test' == sys.argv[1]:
            run_simulation(lights)
        else:
            print("options: on|off|test")
    else:
        while True:
            t = datetime.now()
            current_time = round(t.hour + t.minute / 60, 2)
            values = calc_diff(schedule, current_time)

            for light in lights:
                change(light, values[0], values[1])

            time.sleep(60*10)


