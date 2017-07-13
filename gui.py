from Tkinter import *
import tkFileDialog
import os

from dj_python import mp3FiberRename

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
        mp3FiberRename(filepathEntry.get())

    # Add track rename
    Grid.rowconfigure(frameTop, 0, weight=1)
    Grid.columnconfigure(frameTop, 2, weight=1)
    btn = Button(frameTop, text="Run", background="#00cc66", command=printRootPath)
    btn.grid(row=0, column=2, sticky=N+E+W+S)

    scrollbar = Scrollbar(frameBottom) 
    editArea = Text(frameBottom, 
                   width=10, height=10, 
                   wrap="word",
                   yscrollcommand=scrollbar.set,
                   borderwidth=0, highlightthickness=0, 
                   state=DISABLED,
                   background="#c4c4c4", highlightbackground="#898989")
    scrollbar.config(command=editArea.yview)

    Grid.rowconfigure(frameBottom, 0, weight=1)
    Grid.columnconfigure(frameBottom, 0, weight=1)
    editArea.grid(row=0, column=0, sticky=N+S+E+W)
    scrollbar.grid(row=0, column=1, sticky=E+N+S)

    mainloop()

main()