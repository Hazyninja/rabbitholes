from tkinter import *
from tkinter import filedialog
import os
import shutil

# Added dictionary and generator for file extension sorting
"""This is a sorting script with a GUI that handles sorting via file
 extension. After selecting the folder needed to be sorted, click the start
 button to begin the sort. The files are sorted into three folders 
 that are created if needed inside the parent folder."""

# FIXME: Add browsing support within app instead of on launch
# FIXME: Add the ability to select multiple folders
# FIXME: Add customizable output directories


class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.file_list = None
        self.new_path = None
        self.empty_error = None
        self.dir_name = None
        self.button_Frame = None
        self.start_Button = None
        self.geometry('600x600')

    def get_path(self):
        self.path = filedialog.askdirectory()  # Opens directory dialog
        return self.path

    def start_button(self, path_value):
        self.button_Frame = Frame(self)
        self.button_Frame.pack(expand=True)
        # Calls _start on click to begin sorting
        self.start_Button = Button(
            self.button_Frame, text='Start',
            command=lambda: self._start(path_value),
            width=20,
            height=2,
            activebackground='Blue',
            background='#1DAF28',
            activeforeground='Red'
        )
        self.start_Button.pack(anchor='center')

    def _start(self, path_value):
        # FIXME: Redesign _start to use for loops supported by dictionary
        count = 0
        os.chdir(path_value)  # Change directory to selected folder
        self.file_list = os.listdir()  # Stores file names in file_list
        num_files = len(self.file_list)
        if len(self.file_list) == 0:
            self.empty_error = Label(text='This folder is empty')
            self.empty_error.pack()
            exit()

        # Dictionary associating file extensions and directory names
        file_list = {
            'ImgFiles': ('.png', '.jpg'),
            'TextFiles': ('.txt', '.docx', '.pdf', '.rtf'),
            'Executables': '.exe',
            'CompressedFiles': ('.rar', '.zip', '.7zip'),
        }
        # Iterate over files in directory
        for file in self.file_list:
            if os.path.isdir(file):
                count += 1
                continue

            # Default directory
            self.dir_name = 'Misc'

            for directory, filetypes in file_list.items():
                # Generator checks file type
                if any(file.endswith(filetype) for filetype in filetypes):
                    self.dir_name = directory
                    break

            self.new_path = os.path.join(path_value, self.dir_name)
            self.file_list = os.listdir()
            if self.dir_name not in self.file_list:
                os.mkdir(self.new_path)
            shutil.move(file, self.new_path)  # Moves file to new location
            count += 1

        if count == num_files:
            self.finish_success = Label(text='Success!')
            self.finish_success.pack()
        else:
            self.finish_error = Label(text='Task Failed')
            self.finish_error.pack()


if __name__ == '__main__':
    app = GUI()
    path = app.get_path()
    app.start_button(path)
    app.mainloop()
