import os
import glob

contentDirectory = '/Users/bob/Projects/add_thumb_to_data/content/2-links'
dataFilename     = 'link.txt'

print('### START ###')

# loop through contentDirectory
for folderName, subfolders, filenames in os.walk(contentDirectory):
    for name in subfolders:

        currentFolder = os.path.join(folderName, name)
        dataPath      = os.path.join(currentFolder, dataFilename)
        searchPath    = os.path.join(currentFolder, '*.jpg')

        # check if the data file exists here
        if os.path.exists(dataPath) == True:

            # check for thumb and pick the first one
            thumbs = glob.glob(searchPath)
            if thumbs:
                thumbFilename = os.path.basename(thumbs[0])
                #print(thumbFilename)

                dataFile = open(dataPath, 'a')
                dataFile.write('\n----\n')
                dataFile.write('Link-image: '+thumbFilename)
                dataFile.close()


print('### END ###')
