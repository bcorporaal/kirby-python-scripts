#   add_image_to_content.py

#   Simple script to add images to corresponding kirby content folder
#   The matching of images and content is done based on the number of the content item
#   Change the settings in settings.json not in this script
#   Note that the script is pretty dumb and has no safety checks

#   Tested on macOS 10.13 with Python 3.6 

#   Copyright Bob Corporaal 2017
#   MIT License

#   TO DO
#   - Change existing link to image if there is already one present. Avoid duplicates

import json
import os
import glob
import re
import shutil
from shutil import copy2

# read settings file
settingsFilename = "settings.json"

with open(settingsFilename) as settingsFile:    
    settings = json.load(settingsFile)

dataFilename = settings["dataFilename"]

print('### START ###')

# get directory contents
imageList = os.listdir(settings["imageDirectory"])
contentList = os.listdir(settings["contentDirectory"])

# loop through image directory
for imageFilename in imageList:
    imageNumber = int(re.findall('\d+',imageFilename)[0]) # IMPORTANT ASSUMPTION: first number in the filename is used

    # match image to content based on the numbers in each
    for contentDir in contentList:
        if contentDir.split('-')[0] == str(imageNumber):

            # build complete directory paths and copy the image
            sourcePath = os.path.join(settings["imageDirectory"], imageFilename)
            destinationPath = os.path.join(settings["contentDirectory"],contentDir, imageFilename)
            dataPath = os.path.join(settings["contentDirectory"],contentDir, dataFilename)

            try:
                copy2(sourcePath, destinationPath)
            except IOError:
                print("IOError") 
            
            # add link to file in data
            dataFile = open(dataPath, 'a')
            dataFile.write('\n----\n')
            dataFile.write(settings["fieldForImage"]+':\n'+imageFilename)
            dataFile.close()

            print("added "+imageFilename+" to "+contentDir)

print('### END ###')
