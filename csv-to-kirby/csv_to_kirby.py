#   csv_to_kirby.py

#   Script to use a create kirby content directories based on a CSV file
#   Use only on a copy of the content as this script has no safety checks
#   Change the settings in settings.json not in this script

#   Tested on macOS 10.13 with Python 3.6 and CSV export from Google Sheets

#   Copyright Bob Corporaal 2017
#   MIT License

import re
import os
import json
import csv
import datetime

print("### START ###")

# base
dateFormat  = "%Y-%m-%d"
timeFormat  = "%H:%M"
maxFolderNameLength = 20

# read settings file
settingsFilename = "settings.json"

with open(settingsFilename) as settingsFile:    
    settings = json.load(settingsFile)

postDate = datetime.datetime.strptime(settings["startDate"], dateFormat+" "+timeFormat)
startID = settings["startID"]

print("- Open the input file")
inputFile  = open(settings["inputFilename"])
inputReader = csv.reader(inputFile)

print("- Set content folder")

contentDirectory = settings["baseFolder"]

if os.path.exists(contentDirectory) == False:
    os.makedirs(contentDirectory)
    startID = int(settings["startID"])
else:
    dirContents = os.listdir(contentDirectory)

    # get max number from content entries
    maxID = max([int(dirName.split("-")[0]) for dirName in dirContents]) + 1

    # use the highest of maxID and the provided startID
    startID = max(maxID,int(settings["startID"]))

os.chdir(contentDirectory)

print("- Get header row fields")
headerFields = next(inputReader)

print("- Start processing rows")
for row in inputReader:

    # set the name for this entry
    baseFolderName = row[settings["fieldForURL"]][0:maxFolderNameLength]
    folderName = str(inputReader.line_num + startID - 2)+"-"+re.sub("[^\w\-_]", "-", baseFolderName).lower()

    # make the folder and go there
    os.makedirs(folderName)
    os.chdir(folderName)

    # create the output file
    outputFile = open(settings["outputFilename"], "w")

    # write the content
    i = 0
    for fieldContent in row:
        
        # rewrite booleans to 0 and 1 because that is what Kirby does standard
        if fieldContent == "TRUE":
            fieldContent = "1"
        elif fieldContent == "FALSE":
            fieldContent = "0"

        # write content
        outputFile.write(headerFields[i]+":\n"+fieldContent)
        outputFile.write("\n\n----\n\n")

        i += 1

    # add date and time
    outputFile.write("Date: "+postDate.strftime(dateFormat))
    outputFile.write("\n\n----\n\n")
    outputFile.write("Time: "+postDate.strftime(timeFormat))

    # go back up one level to create a new folder
    os.chdir("..")

    # increase the date while looping through the intervals
    nrDays = settings["postInterval"].pop(0)
    settings["postInterval"].append(nrDays)
    postDate += datetime.timedelta(days=nrDays)

print("- Done with rows")
print("### FINISHED ###")
