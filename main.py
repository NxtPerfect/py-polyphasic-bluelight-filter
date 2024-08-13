#!/usr/bin/env python3
from os import system
import time
import json
from datetime import datetime
from collections import defaultdict

# DISPLAY=:0.0
# Get sections of time with their color and brightness

BLEND_TIME = 60
JSON_PATH = "./config.json"

def main():
    print("Parsing json")
    sections = parseJson(JSON_PATH)
    print("Getting current time")
    currentTime = getCurrentTime()
    print("Changing temp and brightness")
    changeTempAndBrightness(currentTime, sections)

def parseJson(path: str):
    try:
        f = open(path)
        data = json.load(f)
    except Exception as e:
        print(f'Failed to load json file {path}.')
        return

    # get each section, put into array, each contains time as actual time, color and brightness
    sections = []

    # Check how to read from json when you have more objects, for text config this is pointless
    for key in data:
        sections.append([data[key]['time'], data[key]['color'], data[key]['brightness']])
    f.close()

    return sections

def getCurrentTime():
    timeNow = datetime.now()
    formatedTime = timeNow.strftime("%H:%M")

    return formatedTime

def changeTempAndBrightness(currentTime, sections):
    print(f"Current time {currentTime}")
    beginningOfRange, endOfRange = pickCurrentTimeRange(currentTime, sections)
    # TODO: Calculate change to do, based on settings,
    # how long before the time, assume 5 minutes for testing
    # Then, incrementally change temp and brightness
    # until reached, then sleep until next target time
    temperature = sections[endOfRange][1]
    brightness = sections[endOfRange][2]
    redshift(temperature, brightness)

def pickCurrentTimeRange(currentTime, sections):
    for section in range(len(sections)):
        nextSection = section + 1 if (section + 1) < len(sections) else -1
        if currentTime > sections[section][0]:
            print("Beginning of range in the future")
            continue
        if currentTime > sections[nextSection][0]:
            print("Ending of range in the past or current")
            continue
        print(f'Picked {sections[section][0]} and {sections[nextSection][0]}')
        return section, nextSection
    raise Exception("No matching time range found")

def calculateChangeInTargetTempAndBrightnessToCurrentPerBlendFrame(targetTemp, targetBrightness, currentTemp, currentBrightness):
    tempDifferencePerFrame = round((targetTemp - currentTemp) / BLEND_TIME)
    brightDifferencePerFrame = round((targetBrightness - currentBrightness) / BLEND_TIME, 2)

    return tempDifferencePerFrame, brightDifferencePerFrame

def redshift(temp, brightness):
    print(f"Changing to {temp} {brightness}")
    try:
        system(f'redshift -P -O {temp} -b {brightness}')
    except Exception as e:
        raise e

if __name__ == "__main__":
    main()
