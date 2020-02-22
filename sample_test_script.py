'''
Created on Sep 12, 2017

@author: nandal-pc
'''
#!/usr/bin/env python3

import sys, os
from pathlib import Path
from pydroid import pydroid
from datetime import datetime
import sys

deviceId = "5c3d963935f0"
if len(sys.argv) > 2:
    deviceId = sys.argv[1].strip()


# Set Test Config Params in SingleTon File
# Set Android Device Id - which we get using $ adb devices
deviceId =deviceId

# Set adb executable full path
adbExe = 'adb'

# set dir which contains temp data during the test run
tempDataDir = "{}/temp".format(Path.home())
# set dir for dumps, screenshots n other results during test run
resultDir = "{}/result_dir".format(Path.home())
# set file path for results logs
resultFilePath = resultDir+"/result_"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+".txt"

        
print("Running Tests for : ", deviceId, adbExe, resultFilePath)
        
# Create an instance of Android Device
device = pydroid.Element(deviceId=deviceId, adbExe=adbExe, tempDataDir=tempDataDir,resultDir=resultDir,resultFilePath=resultFilePath)

# go to home
device.home()

# Swipe Left
device.swipe("LEFT")

# go to home
device.home()


