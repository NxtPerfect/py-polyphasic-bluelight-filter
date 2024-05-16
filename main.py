#!/usr/bin/env python3
from math import floor
import os
import time
import json
import datetime

'''Run redshift, and slowly fade it into the next light
Use json for setting up times
One json object contains time - hour:minute, hue - 1100-5000k, brightness - 0.0-1.0
Current issue is how can we read actual time from .json, to match either a string, or datetime structure
Also read all the times and manage that'''

# DISPLAY=:0.0
# Get sections of time with their color and brightness

BLEND_TIME = 60

def parseJson(path: str):
    f = open(path)
    data = json.load(f)
    # get each section, put into array, each contains time as actual time, color and brightness
    sections = []

    # Check how to read from json when you have more objects, for text config this is pointless
    for key in data:
        sections.append(
            tuple([data[key]['time'], data[key]['color'], data[key]['brightness']]))
    f.close()

    return sections


def calculateChange(color: int, brightness: float, currentColor: int, currentBrightness: float):
    # Add duration of color into the json
    # Increasing the temp should take 10 minutes

    # Time during which we want to blend from one color and brightness to another

    colorDiffPerFrame: int = int((color - currentColor)/BLEND_TIME)
    brightnessDiffPerFrame: float = round((
        brightness - currentBrightness)/BLEND_TIME, 2)

    print(f'Calculated color diff: {colorDiffPerFrame} and brightness diff: {brightnessDiffPerFrame}')

    return [colorDiffPerFrame, brightnessDiffPerFrame]


def changeColorBrightness(color: int, brightness: float):
    print(f'Current brightness before change: {brightness}')
    try:
        os.system(f'redshift -P -O {color} -b {brightness}')
    except Exception as e:
        print(e)


if __name__ == "__main__":
    color: int = 5500
    brightness: float = 1.0

    section = parseJson("./config.json")
    [_targetTime, _targetColor, _targetBrightness] = [], [], []
    for item in section:
        _targetTime.append(item[0])
        _targetColor.append(item[1])
        _targetBrightness.append(item[2])

    print(f'Target time: {_targetTime}')

    [targetTime, targetColor, targetBrightness] = "00:00", 5500, 1.0
    # Pick correct time
    for x in range(len(_targetTime)-1):
        curTime = datetime.datetime.now().strftime("%H:%M:%S")
        if _targetTime[x+1] < curTime:
            continue
        # If current time is more than time[x] but less than next time
        # set it's value to previous time, and target next one
        if _targetTime[x] <= curTime and curTime < _targetTime[x+1]:
            changeColorBrightness(section[x][1], section[x][2])
            [targetTime, targetColor, targetBrightness] = section[x+1][0], section[x+1][1], section[x+1][2]
            print(f'Target time: {targetTime} color: {targetColor}')

    # # For debug purposes
    # color = 3500
    # brightness = 0.55

    [colorDiff, brightnessDiff] = calculateChange(
        targetColor, targetBrightness, color, brightness)

    # Currently when timezone is picked, it never gets changed
    # so once we successfully change the time once
    # we don't get new section
    while True:
        # timeToChange = (datetime.datetime.strptime(targetTime, '%H:%M') -
        #                 datetime.timedelta(minutes=BLEND_TIME)).time()
        # If we reach that change time, how do we know?
        timeToChange = (datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(targetTime, '%H:%M').time()) -
                        datetime.timedelta(minutes=15))
        currentTime = datetime.datetime.now().strftime("%H:%M")
        print(f'Time to change at: {timeToChange.time()} current time: {currentTime}')
        if (timeToChange.time() != time.time()):
            # time.sleep(60) # sleep until target time
            curTime = datetime.datetime.now()
            timeDiff = (timeToChange - curTime).total_seconds()
            print(f'Not the right time. Sleeping for: {floor(timeDiff)}s {timeDiff/60:.2f}m {timeDiff/3600:.2f}h')
            time.sleep(floor((timeToChange.timestamp() - curTime.timestamp()) * 60))
            continue

        for x in range(BLEND_TIME):
            print(
                    f'Correct time. Changing color {color}K to {targetColor}K and brightness {brightness:.2f} to {targetBrightness:.2f}...')
            color += colorDiff
            brightness += round(brightnessDiff, 2)
            brightness = round(brightness, 2)

            changeColorBrightness(color, brightness)
            print(f'Changes left {BLEND_TIME-x}. Sleeping...')
            time.sleep((15*60)/BLEND_TIME)
