from Tkinter import *
import tkFileDialog
import os

from mp3FiberRename import MP3FiberOrganizer
from reporter import Reporter

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

def main():
    root = Tk()
    root.minsize(600, 80)
    root.title("MP3Fiber Rename Tool")
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)
    # Frames for the buttons and reporting
    frameTop=Frame(root)
    frameTop.grid(row=1, column=0, sticky=N+E+W, padx=10, pady=5)
    frameBottom=Frame(root)
    frameBottom.grid(row=0, column=0, sticky=N+E+W+S, padx=10, pady=5)
    # Reporting Box
    scrollbar = Scrollbar(frameBottom) 
    textArea = Text(frameBottom, 
                   width=10, height=10, 
                   wrap="word",
                   yscrollcommand=scrollbar.set,
                   borderwidth=0, highlightthickness=0, 
                   state=DISABLED,
                   background="#c4c4c4", highlightbackground="#898989")
    scrollbar.config(command=textArea.yview)

    Grid.rowconfigure(frameBottom, 0, weight=1)
    Grid.columnconfigure(frameBottom, 0, weight=1)
    textArea.grid(row=0, column=0, sticky=N+S+E+W)
    scrollbar.grid(row=0, column=1, sticky=E+N+S)

    org = MP3FiberOrganizer(GuiReporter(textArea))

    # Add entry for file Path
    Grid.rowconfigure(frameTop, 0, weight=1)
    Grid.columnconfigure(frameTop, 0, weight=1)
    filepathEntry = Entry(frameTop, width=50)
    filepathEntry.insert(0, os.getcwd())
    filepathEntry.focus_set()
    filepathEntry.grid(row=0, column=0, sticky=N+E+W+S)
    # Gets the files path from the dir
    def getFilePath():
        # get directory
        currdir = os.getcwd()
        tempdir = tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        if len(tempdir) > 0:
            filepathEntry.delete(0,END)
            filepathEntry.insert(0, tempdir)

    # Add get file Path button
    Grid.rowconfigure(frameTop, 0, weight=1)
    Grid.columnconfigure(frameTop, 1, weight=1)
    btn = Button(frameTop, text="File Directory", background="#0099cc", command=getFilePath)
    btn.grid(row=0, column=1, sticky=N+E+W+S)

    # Runs the filepathEntry
    def printRootPath():
        org.run(filepathEntry.get())

    # Add track rename
    Grid.rowconfigure(frameTop, 0, weight=1)
    Grid.columnconfigure(frameTop, 2, weight=1)
    btn = Button(frameTop, text="Run", background="#00cc66", command=printRootPath)
    btn.grid(row=0, column=2, sticky=N+E+W+S)

    mainloop()

main()