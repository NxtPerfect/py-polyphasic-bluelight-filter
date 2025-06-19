#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3
from os import system
from sys import argv
import time
from datetime import datetime

BLEND_TIME = 30

type number = int | float


def main():
    args = argv
    if len(args) < 6:
        print(
            "Input all 5 arguments, current temp and brightness, as well as target time, temp and brightness."
        )
        return
    currentTemp, currentBrightness = int(args[1]), float(args[2])
    targetTime, targetTemp, targetBrightness = args[3], int(args[4]), float(args[5])

    if not all([currentTemp, currentBrightness, targetTemp, targetBrightness]):
        print(
            "Input all 5 arguments, current temp and brightness, as well as target time, temp and brightness."
        )
        return

    print("Calculating how many changes needed to hit target...")
    changesAmount = calculateChangesRequired(targetTime)
    tempChangePerIter = (int(targetTemp) - int(currentTemp)) / (changesAmount)
    brightnessChangePerIter = (float(targetBrightness) - float(currentBrightness)) / (
        changesAmount
    )
    print("Changing temp and brightness...")
    try:
        changeTempAndBrightness(
            changesAmount,
            currentTemp,
            currentBrightness,
            tempChangePerIter,
            brightnessChangePerIter,
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
        targetTime += ":00"
    parsedTargetTime = datetime.strptime(targetTime, "%H:%M:%S")
    timeDiff = ((parsedTargetTime - currentTime)).total_seconds()

    return round(timeDiff * BLEND_TIME)


def getCurrentTime():
    timeNow = datetime.now()
    formatedTime = timeNow.strftime("%H:%M:%S")

    return datetime.strptime(formatedTime, "%H:%M:%S")


def changeTempAndBrightness(
    changesAmount: int,
    currentTemp: number,
    currentBrightness: number,
    tempChange: number,
    brightnessChange: number,
):
    for i in range(changesAmount):
        currentTemp += tempChange
        currentBrightness += brightnessChange
        if i % BLEND_TIME == 0:
            print(f"Changing to {currentTemp} {currentBrightness}")
        redshift(currentTemp, currentBrightness)
        time.sleep(1 / BLEND_TIME)


def redshift(temp: number, brightness: number):
    if round(temp) not in range(1000, 25000):
        raise Exception(f"Temperature not in range 1000, 25000 got: {temp}")
    if round(brightness * 100) not in range(0, 100):
        raise Exception(
            f"Brightness not in range 0 1, got: {brightness} {round(brightness*100)}"
        )
    try:
        _ = system(f"redshift -P -O {temp} -b {brightness} > /dev/null 2>&1")
    except Exception as e:
        raise e


if __name__ == "__main__":
    main()
