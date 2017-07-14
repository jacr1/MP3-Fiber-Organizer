from mp3FiberRename import MP3FiberOrganizer
from reporter import normalReporter
from artistFolders import createArtistFolders

rootPath = "./../"

organizer = MP3FiberOrganizer(normalReporter())
organizer.run(rootPath)

createArtistFolders(rootPath)
