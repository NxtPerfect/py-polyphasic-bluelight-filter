#!/usr/bin/env python3
from os import system
from sys import argv
import time
from datetime import datetime

# DISPLAY=:0.0
# Get sections of time with their color and brightness

BLEND_TIME = 120
SECOND = 1000

def main():
    args = argv
    if len(args) < 6:
        print("Input all 5 arguments, current temp and brightness, as well as target time, temp and brightness.")
        return
    currentTemp, currentBrightness = int(args[1]), float(args[2])
    targetTime, targetTemp, targetBrightness = args[3], int(args[4]), float(args[5])

    if not all([currentTemp, currentBrightness, targetTemp, targetBrightness]):
        print("Input all 5 arguments, current temp and brightness, as well as target time, temp and brightness.")
        return

    print("Calculating how many changes needed to hit target...")
    changesAmount = calculateChangesRequired(targetTime)
    tempChangePerIter = (int(targetTemp) - int(currentTemp)) / (changesAmount)
    brightnessChangePerIter = (float(targetBrightness) - float(currentBrightness)) / (changesAmount)
    print("Changing temp and brightness...")
    try:
        changeTempAndBrightness(
            changesAmount,
            currentTemp,
            currentBrightness,
            tempChangePerIter,
            brightnessChangePerIter
        )
    except Exception as e:
        print(e)
    finally:
        # Do one final change to target value
        # because we're too inaccurate in calcs
        # and will miss it
        redshift(targetTemp, targetBrightness)

def calculateChangesRequired(targetTime: str):
    currentTime = getCurrentTime()
    if len(targetTime.split(":")) < 3:
        targetTime += ":0"
    parsedTargetTime = datetime.strptime(targetTime, "%H:%M:%S")

    return round(((parsedTargetTime - currentTime)).total_seconds() * BLEND_TIME)

def getCurrentTime():
    timeNow = datetime.now()
    formatedTime = timeNow.strftime("%H:%M:%S")

    return datetime.strptime(formatedTime, "%H:%M:%S")

def changeTempAndBrightness(changesAmount, currentTemp, currentBrightness, tempChange, brightnessChange):
    for _ in range(changesAmount):
        currentTemp += tempChange
        currentBrightness += brightnessChange
        if _ % BLEND_TIME == 0:
            print(f"Changing to {currentTemp} {currentBrightness}")
        redshift(currentTemp, currentBrightness)
        # fps to ms per frame to seconds
        time.sleep((BLEND_TIME/SECOND)/SECOND)

def redshift(temp, brightness):
    if temp < 1000 or temp > 25000:
        raise Exception(f'Temperature not in range 1000, 25000 got: {temp}')
    if brightness < 0 or brightness > 1.0:
        raise Exception(f'Brightness not in range 0 1, got: {brightness}')
    try:
        system(f'redshift -P -O {temp} -b {brightness}')
    except Exception as e:
        raise e

if __name__ == "__main__":
    main()
