#   shuffle_content.py

#   Simple script to shuffle content pages
#   Set the content directory in settings.json

#   Tested on macOS 10.13 with Python 3.6 and Kirby 3

#   Copyright Bob Corporaal 2019
#   MIT License

import json
import os
import glob
import re
import shutil
from shutil import copy2
from random import shuffle

# read settings file
settingsFilename = "settings.json"

with open(settingsFilename) as settingsFile:    
    settings = json.load(settingsFile)

contentDirectory = settings["contentDirectory"]

print('### START ###')

# get directory contents
contentList = os.listdir(settings["contentDirectory"])

print('Old directory')
print(contentList)
shuffle(contentList)

c = 1
newContentList = []

# loop through the directory
for contentName in contentList:
    newContentName = str(c) + '_' + contentName.split('_')[1]
    c = c + 1
    newContentList.append(newContentName)

for newContentName, contentName in zip(newContentList, contentList):
    os.rename(os.path.join(contentDirectory, contentName), os.path.join(contentDirectory, newContentName))

print('New directory')
print(os.listdir(settings["contentDirectory"]))

print('### END ###')
