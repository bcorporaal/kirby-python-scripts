import csv
import datetime
import re
import os

print('### START ###')

linkFile = open('links.csv')
linkReader = csv.reader(linkFile)

refDate     = datetime.datetime(2017, 2, 5, 10, 20, 0)
dateFormat  = '%Y-%m-%d'
timeFormat  = '%H:%M'

baseFolder = 'content'
actualFolder = baseFolder
counter = 0

# increment the counter until the foldername does not exist yet
# pretty clumsy way of doing this, but it works
while os.path.exists(actualFolder) == True:
    counter = counter + 1
    actualFolder = baseFolder + '-' + str(counter)

print('- Make content folder')
os.makedirs(actualFolder)
os.chdir(actualFolder)

print('- Start with rows')

for row in linkReader:
    if linkReader.line_num == 1:
               continue    # skip first row
    link = {}
    link['title']       = row[0]
    link['url']         = row[1]
    link['description'] = row[2]
    link['favorite']    = '1' if row[3].lower() == 'true' else '0'
    link['category']    = row[4].lower()

    tags = filter(None, [str(row[5]),str(row[6]),str(row[7])]) # combine tags and filter empty
    link['tags'] = ', '.join(tags)

    refDate = refDate + datetime.timedelta(seconds=60) # increase the time for each link
    link['date'] = str(refDate.strftime(dateFormat))

    # create folder name with counter and clean title
    link['folder'] = str(linkReader.line_num - 1)+'-'+re.sub('[^\w\-_]', '-', link['title']).lower()

    os.makedirs(link['folder'])
    os.chdir(link['folder'])

    linkFile = open('link.txt', 'w')

    linkFile.write('Title: '+link['title'])
    linkFile.write('\n\n----\n\n')
    linkFile.write('Site-url: '+link['url'])
    linkFile.write('\n\n----\n\n')
    linkFile.write('Description: '+link['description'])
    linkFile.write('\n\n----\n\n')
    linkFile.write('Favorite: '+link['favorite'])
    linkFile.write('\n\n----\n\n')
    linkFile.write('Category: '+link['category'])
    linkFile.write('\n\n----\n\n')
    linkFile.write('Tags: '+link['tags'])
    linkFile.write('\n\n----\n\n')
    linkFile.write('Date: '+refDate.strftime(dateFormat))
    linkFile.write('\n\n----\n\n')
    linkFile.write('Time: '+refDate.strftime(timeFormat))

    # go back up one level to create a new folder
    os.chdir('..')


print('- Done with rows')
