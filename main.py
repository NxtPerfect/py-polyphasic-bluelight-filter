import os
import time
import json

'''Run redshift, and slowly fade it into the next light
Use json for setting up times
One json object contains time - hour:minute, hue - 1100-5000k, brightness - 0.0-1.0'''

# DISPLAY=:0.0
# Get sections of time with their color and brightness


def parseJson(path: str):
    f = open(path)
    data = json.load(f)
    # get each section, put into array, each contains time as actual time, color and brightness
    sections = []

    # Check how to read from json when you have more objects, for text config this is pointless
    for key in data:
        value = data[key]

    sections.append(
        tuple([data['time'], data['color'], data['brightness']]))
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
    currentTime = time.time()
    currentColor: int = 5500
    currentBrightness: float = 1.0

    [targetTime, targetColor, targetBrightness] = parseJson("./config.json")

    [colorDiff, brightnessDiff] = calculateChange(
        targetColor, targetBrightness, currentColor, currentBrightness)

    nextColor = currentColor
    nextBrightness = currentBrightness

    while True:
        if ((targetTime+3600) != time.time):
            time.sleep(30)
            continue

        nextColor += colorDiff
        nextBrightness += brightnessDiff

        changeColorBrightness(nextColor, nextBrightness)
        time.sleep(20)
