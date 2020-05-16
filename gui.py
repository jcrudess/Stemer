import tkinter as tk
from tkinter import filedialog
import os
import time
import threading

INIT_STATUS = "Spreman!"
TITLE = "Stemer v.0.1.1"


class Application(tk.Frame):
    folderPath = os.path.abspath(os.getcwd())
    filePath = os.path.abspath(os.path.join(os.getcwd(), "test.mp3"))
    optionDict = {
        "2 stems - vokal + instrumenti": "spleeter:2stems",
        "4 stems - vokal + bubanj + bas + ostalo": "spleeter:4stems",
        "5 stems - vokal + bubanj + bas + klavir + ostalo": "spleeter:5stems",
    }
    optionList = list(optionDict.keys())
    option = "spleeter:2stems"

    def __init__(self):
        # windows
        self.window = tk.Tk()
        self.window.iconbitmap("./resource/hammer.ico")
        self.window.title(TITLE)
        self.window.size
        self.window.resizable(False, False)
        self.choiceVar = tk.StringVar(self.window)
        # label file
        self.fileLabelFrame = tk.Frame(self.window, height=10, width=100)
        self.fileLabelFrame.grid(row=1, column=1, pady=2)
        self.fileOpis = tk.Label(self.fileLabelFrame, text="File:", width=8, anchor="e")
        self.fileOpis.grid(column=0, row=0)
        self.fileLabel = tk.Label(self.fileLabelFrame, text=self.filePath, width=58)
        self.fileLabel.grid(column=1, row=0)
        self.fileButton = tk.Button(
            self.fileLabelFrame, text="Odaberi file...", command=self.loadFile, width=14
        )
        self.fileButton.grid(column=2, row=0)
        # label folder
        self.folderLabelFrame = tk.Frame(self.window, height=10, width=100)
        self.folderLabelFrame.grid(row=2, column=1, pady=2)
        self.folderOpis = tk.Label(
            self.folderLabelFrame, text="Spremi u:", width=8, anchor="e"
        )
        self.folderOpis.grid(column=0, row=0)
        self.folderLabel = tk.Label(
            self.folderLabelFrame, text=self.folderPath, width=58
        )
        self.folderLabel.grid(column=1, row=0)
        self.folderButton = tk.Button(
            self.folderLabelFrame,
            text="Odaberi folder...",
            command=self.loadFolder,
            width=14,
        )
        self.folderButton.grid(column=2, row=0)
        # opcije i konvert
        self.optionFrame = tk.Frame(self.window, height=10, width=100)
        self.optionFrame.grid(row=3, column=1, pady=2)
        self.choiceVar.set("2 stems - vokal + instrumenti")
        self.options = tk.OptionMenu(
            self.optionFrame,
            self.choiceVar,
            *self.optionList,
            command=self.optionChange
        )
        self.options.config(width=71)
        self.options.grid(column=0, row=0)
        self.convButton = tk.Button(
            self.optionFrame, text="Razdvoji!", command=self.separate, width=14
        )
        self.convButton.grid(column=1, row=0)
        # status traka
        self.statusLabelFrame = tk.Frame(self.window, height=10, width=100)
        self.statusLabelFrame.grid(row=4, column=1, pady=2)
        self.statusLabel = tk.Label(self.statusLabelFrame, text=INIT_STATUS, width=66)
        self.statusLabel.grid(column=0, row=0)
        self.window.mainloop()

    def loadFile(self):
        fileDialog = filedialog.askopenfilename(
            filetypes=(("mp3 files", "*.mp3"),), title="Select file"
        )
        self.filePath = fileDialog
        self.fileLabel.config(text=fileDialog)

    def loadFolder(self):
        folderDialog = filedialog.askdirectory()
        self.folderPath = folderDialog
        self.folderLabel.config(text=folderDialog)

    def separate(self):
        t = threading.Thread(
            target=self.callSpleeter, args=(self.filePath, self.folderPath, self.option)
        )
        t.start()

    def setStatus(self, text):
        self.statusLabel.config(text=text)

    def optionChange(self, arg):
        self.option = self.optionDict[arg]

    def callSpleeter(self, file, folder, mode):
        self.setStatus("Radim...")
        self.convButton.config(state="disabled")
        try:
            from spleeter.separator import Separator

            separator = Separator(mode)
            separator.separate_to_file(file, folder)
        except Exception as e:
            print(e)
        self.setStatus("Gotov!")
        self.convButton.config(state="normal")
        self.setStatus(INIT_STATUS)
