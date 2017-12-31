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

    def runDirFileNames(self, rootPath):
        self.reporter.clear()
        self.rootPath = rootPath
        # gets all files in the current directory that ends in .mp3
        self.files = [x for x in next(os.walk(rootPath))[2] if x.endswith('.mp3')]
        # No files found
        if len(self.files) > 0:
            for x in range(len(self.files)):
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
                        self.reporter.printLine("Failed: ", self.files[x])
                else:
                    self.reporter.printLine("Failed: ", self.files[x])
        else:
            self.reporter.printLine("Failed: No MP3 files found")

    def changeFilesMetadata(self, filePath, newNames):
        # Mutagen lib gets out the metadata
        audio = ID3(filePath)
        # Doesn't have track fields, so needs to be created. 
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

    def createArtistFolders(self, rootPath):
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
                        directory = rootPath + "/" + artist.encode('utf-8').strip()
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        os.rename(rootPath + "/" + fileName, directory + "/" + fileName)
                        self.reporter.printLine("SUCCESS: " + fileName)
                except KeyError, e:
                    self.reporter.printLine("FAILURE: " + fileName)
        else:
            self.reporter.printLine("Failed: No MP3 files found")


if __name__ == '__main__':
    rootPath = "/media/jaco1a/326025077B693289/music"

    organizer = MP3FiberOrganizer(normalReporter())
    organizer.runDirFileNames(rootPath)
    organizer.createArtistFolders(rootPath)      
