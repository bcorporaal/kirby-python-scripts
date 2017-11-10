import csv
import datetime
import re
import os

print('### START ###')

# TO DO
# - option to change variables from the command line
# - use date from csv file or set date automatically

# variables
contentFile  = open('test_content.csv')
refDate     = datetime.datetime(2017, 11, 13, 15, 00, 0)
counter     = 0
baseFolder  = 'content'
contentFilename = 'data'
entryNameField = 0

# Array of interval between posts in days
# [1] = one post a day
# [2] = every other day
# [1,4,2] = one post, a post the next day, one 4 days later, a post two days later, a post the next day, 4 days later, etc.
postInterval = [3,4]

dateFormat  = '%Y-%m-%d'
timeFormat  = '%H:%M'

contentReader = csv.reader(contentFile)

# create the content folder
# increment the counter until the foldername does not exist yet
# pretty clumsy way of doing this, but it works
actualFolder = baseFolder
while os.path.exists(actualFolder) == True:
    counter = counter + 1
    actualFolder = baseFolder + '-' + str(counter)

print('- Make content folder')
os.makedirs(actualFolder)
os.chdir(actualFolder)

print('- Get header row fields')
fields = next(contentReader)

print('- Start with rows')
for row in contentReader:

    # set the name for this entry
    folderName = str(contentReader.line_num - 1)+'-'+re.sub('[^\w\-_]', '-', row[entryNameField]).lower()

    # make the folder and go there
    os.makedirs(folderName)
    os.chdir(folderName)

    # create a text file
    contentFile = open(contentFilename+'.txt', 'w')

    # write the content
    i = 0
    for contentSection in row:
        
        # rewrite booleans to 0 and 1
        if contentSection == 'TRUE':
            contentSection = '1'
        elif contentSection == 'FALSE':
            contentSection = '0'

        # write content
        contentFile.write(fields[i]+':\n'+contentSection)
        contentFile.write('\n\n----\n\n')

        i += 1

    # add date and time
    contentFile.write('Date: '+refDate.strftime(dateFormat))
    contentFile.write('\n\n----\n\n')
    contentFile.write('Time: '+refDate.strftime(timeFormat))

    # go back up one level to create a new folder
    os.chdir('..')

    # increase the date
    nrDays = postInterval.pop(0)
    postInterval.append(nrDays)
    refDate += datetime.timedelta(days=nrDays)

print('- Done with the rows')
print('### FINISHED ###')
