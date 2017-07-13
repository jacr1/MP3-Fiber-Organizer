from mp3FiberRename import MP3FiberOrganizer
from reporter import normalReporter

rootPath = "./../"

organizer = MP3FiberOrganizer(normalReporter())
organizer.run(rootPath)
