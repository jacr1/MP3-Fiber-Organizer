import os
from mutagen.mp3 import EasyMP3 as MP3
from mutagen.id3 import ID3, TIT2, TPE1
import sys


def createArtistFolders(rootPath):
    currentDir = next(os.walk(rootPath))
    filesNames = [x for x in next(os.walk(rootPath))[2] if x.endswith('.mp3')]

    # For all files, look at artist or ignore if none exists
    # see if dir exsits named the same thing
    # if so, move file into that folder
    # if not, create and move file into folder
    if len(filesNames) != 0:
        for fileName in filesNames:
            audio = ID3(rootPath + "/" + fileName)
            try:
                artist = audio['TPE1'].text[0]
                if (artist != None and artist != ""):
                    directory = rootPath + "/" + str(artist)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    #print(rootPath + "/" + fileName, directory + "/" + fileName)
                    os.rename(rootPath + "/" + fileName, directory + "/" + fileName)
                    print("SUCCESS: " + fileName)
            except KeyError, e:
                print("FAILURE: " + fileName)
    else:
        print("Failed: No MP3 files found")
