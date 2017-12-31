from Tkinter import *
import tkFileDialog
import os

from mp3FiberOrganizer import MP3FiberOrganizer
from reporter import Reporter
from AutocompleteEntry import AutocompleteEntry

class GuiReporter(Reporter):
        
    def __init__(self, textArea):
        self.textArea = textArea

    def printLine(self, *args):
        self.textArea['state'] = 'normal'
        if (len(args) == 1):
            print(args[0])
            self.textArea.insert(INSERT, "(" + str(args[0]) + ")\n")
        elif (len(args) == 2):
            print(args[0], args[1])
            self.textArea.insert(INSERT, "(" + str(args[0]) + ", " + str(args[1]) + ")\n")
        self.textArea['state'] = 'disabled'

    def clear(self):
        self.textArea['state'] = 'normal'
        self.textArea.delete(1.0, END)
        self.textArea['state'] = 'disabled'


class mainGUI(object):
    
    def __init__(self):
        root = Tk()
        root.minsize(600, 80)
        root.title("MP3Fiber Rename Tool")
        self.root = root

        Grid.rowconfigure(root, 0, weight=1)
        Grid.columnconfigure(root, 0, weight=1)
        # Frames for top, middle and bottom
        frameTop=Frame(root)
        frameTop.grid(row=0, column=0, sticky=N+E+W+S, padx=10, pady=5)
        frameMiddle=Frame(root)
        frameMiddle.grid(row=1, column=0, sticky=N+E+W, padx=10, pady=5)
        frameBottom = Frame(root)
        frameBottom.grid(row=2, column=0, sticky=N+E+W+S, padx=10, pady=5)
        
        textArea = self.createReportingBox(frameTop)
        # Create fiber organizer 
        self.org = MP3FiberOrganizer(GuiReporter(textArea))
        self.filepathEntry = self.createFilePathEntry(frameMiddle)

        self.addFilePathButton(frameMiddle)
        self.addTrackRenameButton(frameMiddle)
        self.artistTick = self.addTickbox(frameBottom)

        mainloop()

    def createReportingBox(self, frame):
        # Reporting Box
        scrollbar = Scrollbar(frame) 
        textArea = Text(frame, 
                       width=10, height=10, 
                       wrap="word",
                       yscrollcommand=scrollbar.set,
                       borderwidth=0, highlightthickness=0, 
                       state=DISABLED,
                       background="#c4c4c4", highlightbackground="#898989")
        scrollbar.config(command=textArea.yview)
        # add to grid
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        textArea.grid(row=0, column=0, sticky=N+S+E+W)
        scrollbar.grid(row=0, column=1, sticky=E+N+S)

        return textArea

    def triggerEntryPostion(self, event):
        self.filepathEntry.windowMovement()

    def createFilePathEntry(self, frame):
        lista = ["/home/jaco1a/Music/", "/home/jaco1a/Music/MP3-Fiber-Organizer/something"]
        filepathEntry = AutocompleteEntry(lista, frame, width=50)
        self.root.bind("<Configure>", self.triggerEntryPostion)
        
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        filepathEntry.insert(0, os.getcwd())
        filepathEntry.focus_set()
        filepathEntry.grid(row=0, column=0, sticky=N+E+W+S)

        return filepathEntry

    def getFilePath(self):
        # get directory
        currdir = os.getcwd()
        tempdir = tkFileDialog.askdirectory(parent=self.root, 
            initialdir=currdir, 
            title='Please select a directory')

        if len(tempdir) > 0:
            self.filepathEntry.delete(0,END)
            self.filepathEntry.insert(0, tempdir)
    
    def addFilePathButton(self, frame):
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 1, weight=1)
        btn = Button(frame, text="File Directory", background="#0099cc", command=self.getFilePath)
        btn.grid(row=0, column=1, sticky=N+E+W+S)

    def runFilesRename(self):
        self.org.runDirFileNames(self.filepathEntry.get())
        if (self.artistTick.get() == 1):
            self.org.createArtistFolders(self.filepathEntry.get())


    def addTrackRenameButton(self, frame):
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 2, weight=1)
        btn = Button(frame, text="Run", background="#00cc66", command=self.runFilesRename)
        btn.grid(row=0, column=2, sticky=N+E+W+S)

    def addTickbox(self, frame):
        artistTick = IntVar()
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        check = Checkbutton(frame, text="Create Artist Folders", variable=artistTick)
        check.grid(row=0, column=0, sticky=E)
        return artistTick

mainGUI()