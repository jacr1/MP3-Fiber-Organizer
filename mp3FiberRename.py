import os
from mutagen.mp3 import EasyMP3 as MP3
from mutagen.id3 import ID3, TIT2, TPE1
import sys

from reporter import Reporter

class fileData:

    def __init__(self, artist, title):
        self.title = title;
        self.artist = artist;
    
    def __str__(self):
        return str(self.title) + " - " + str(self.artist)


class MP3FiberOrganizer():

    def __init__(self, reporter):
        self.reporter = reporter

    def run(self, rootPath):
        self.reporter.clear()
        self.rootPath = rootPath
        self.files = []
        totalMP3 = 0
        self.getDirs()
        # No files found
        if len(self.files) > 0:
            for x in range(len(self.files)):
                if self.files[x].endswith('.mp3'):
                    totalMP3 += 1
                    # get out the artist and title from file name
                    newNames = self.splitFilename(self.files[x])
                    # not correct format of download don't rename
                    if newNames != None and newNames != False:
                        if newNames.title != [] and newNames.artist != []:
                            filePath = self.rootPath + "/" + self.files[x]
                            self.changeFilesMetadata(filePath, newNames)
                            newFilePath = self.rootPath + "/" + newNames.title + ".mp3"
                            os.rename(filePath, newFilePath)
                            
                            self.reporter.printLine("Old filepath: ", filePath)
                            self.reporter.printLine("New filepath: ", newFilePath)
                        else:
                            self.reporter.printLine("Failed: Title or artist not split by dash", self.files[x])
                    else:
                        self.reporter.printLine("Failed: Unable to split artist and title", self.files[x])

        if (totalMP3 == 0):
            self.reporter.printLine("Failed: No MP3 files found")

    def getDirs(self):
        for (dirpath, dirnames, filenames) in os.walk(self.rootPath):    
            self.files.extend(filenames)

    def changeFilesMetadata(self, filePath, newNames):
        # Mutagen lib gets out the metadata
        audio = ID3(filePath)
        try:
            print("Artist: ", audio['TPE1'].text[0])
            print("Track: ", audio['TIT2'].text[0])
        except KeyError, e:
            print repr(e)
            audio["TIT2"] = TIT2(encoding=3, text=["Title"])
            audio["TPE1"] = TPE1(encoding=3, text=["Artist"])
        # set the name and title
        audio['TPE1'].text[0] = newNames.artist.decode('utf-8', 'ignore')
        audio['TIT2'].text[0] = newNames.title.decode('utf-8', 'ignore')
        print("New Artist: ", audio['TPE1'].text[0])
        print("New Track: ", audio['TIT2'].text[0])
        audio.save()

    def splitFilename(self, filename):
        filename = list(filename)
        newName = [list(),list()]
        index = 0;
        start = False
        try:
            for i in range(len(filename)):
                # Replace underscore with space or if start nothing
                if filename[i] == "_":
                    if start:
                        newName[index].append("")
                        start = False
                    else:
                        newName[index].append(" ")
                # Start of [www.MP3Fiber.com]
                elif filename[i] == "[":
                    newName[index] = "".join(newName[index])
                    break
                # '-' indicates split of title and artist
                elif filename[i] == "-" and filename[i + 1] == "_":
                    newName[index] = "".join(newName[index])
                    index += 1
                    start = True
                else:
                    newName[index].append(filename[i])
        except IndexError:
    	    return False
        return fileData(newName[0], newName[1])
       
