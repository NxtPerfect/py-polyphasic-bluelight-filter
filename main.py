import os
import time
import json
import datetime

'''Run redshift, and slowly fade it into the next light
Use json for setting up times
One json object contains time - hour:minute, hue - 1100-5000k, brightness - 0.0-1.0'''

# DISPLAY=:0.0

if __name__ == "__main__":
    current_time = time.localtime()
    os.system("redshift -P -O {color} -b {brightness}")


def parseJson(path: str):
    f = open(path)
    data = json.load(f)
    # get each section, put into array, each contains time as actual time, color and brightness
    sections = []
    for key, obj in data:
        sections.append(datetime.datetime.strptime(
            obj['time'], '%H:%M').strftime('%H:%M'))
    f.close()


def calculateChange(time: str, color: int, brightness: float):
    # Add duration of color into the json
    # Increasing the temp should take 10 minutes
    # Decreasing should take 1h
    pass
