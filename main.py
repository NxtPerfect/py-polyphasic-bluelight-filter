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
    blendTime = 10 * 60

    colorDiffPerFrame: int = int((color - currentColor)/blendTime)
    brightnessDiffPerFrame: float = (
        brightness - currentBrightness)/blendTime

    return [colorDiffPerFrame, brightnessDiffPerFrame]


def changeColorBrightness(color: int, brightness: float):
    try:
        os.system(f'redshift -P -O {color} -b {brightness}')
    except Exception as e:
        print(e)


if __name__ == "__main__":
    color: int = 5500
    brightness: float = 1.0

    section = parseJson("./config.json")
    [_targetTime, _targetColor, _targetBrightness] = [], [], []
    for item, key in section:
        _targetTime.append(item["time"])
        _targetColor.append(item["color"])
        _targetBrightness.append(item["brightness"])

    print(_targetTime)

    [targetTime, targetColor, targetBrightness] = section[4][0], section[4][1], section[4][2]

    # For debug purposes
    color = 3500
    brightness = 0.55

    [colorDiff, brightnessDiff] = calculateChange(
        targetColor, targetBrightness, color, brightness)

    while True:
        timeToChange = (datetime.datetime.strptime(targetTime, '%H:%M') +
                        datetime.timedelta(minutes=2)).time()
        currentTime = datetime.datetime.now().strftime("%H:%M:%S")
        print(f'{timeToChange}, {currentTime}')
        if (timeToChange != time.time()):
            print("Not the right time. Sleeping 60s...")
            time.sleep(30)
            continue

        for x in range(10):
            print(
                f'Correct time. Changing color {color} and brightness {brightness}...')
            color += colorDiff
            brightness += brightnessDiff

            changeColorBrightness(color, brightness)
            print(f'Changes left {10-x}. Sleeping...')
            time.sleep(60)
