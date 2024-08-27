from tkinter import *
from tkinter import filedialog
import os
import shutil

# Added dictionary and generator for file extension sorting
"""This is a sorting script with a GUI that handles sorting via file
 extension. After selecting the folder needed to be sorted, click the start
 button to begin the sort. The files are sorted into three folders 
 that are created if needed inside the parent folder."""

# FIXME: Adjust grid on buttons


class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.user_dirs = None
        self.file_list = None
        self.new_path = None
        self.empty_error = None
        self.dir_name = None
        self.button_Frame = None
        self.start_Button = None
        self.browse_Button = None
        self.path = None
        self.geometry('600x600')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.browse_button()
        self.usr_defined_dir()

    def browse_button(self):
        # Sets browse button in window
        self.button_Frame = Frame(self)
        self.button_Frame.grid(
            row=5, column=0,
            padx=5, pady=5,
            sticky='n'
        )
        self.browse_Button = Button(
            self.button_Frame, text='Browse',
            command=self.get_path,
            width=20,
            height=2,
            activebackground='Blue',
            background='#1DAF28',
            activeforeground='Red'
        )
        self.browse_Button.grid(row=5, column=3, padx=20, pady=5)

    def get_path(self):
        self.path = filedialog.askdirectory()  # Opens directory dialog
        # Creates start button if one does not exist
        if self.path:
            if not self.start_Button:
                self.start_button(self.path)

    def usr_defined_dir(self):
        # User inputs for custom directory names
        self.user_dirs = {}
        file_types = [
            'ImgFiles', 'TextFiles',
            'Executables', 'CompressedFiles'
        ]
        # Retrieve the index and value for proper grid placement
        for i, file_type in enumerate(file_types):
            print(f"Creating input for {file_type} at row {i}")  # Debugging print

            label = Label(
                self,
                text=f'{file_type} Directory Name: '
            )
            label.grid(row=i+1, column=0, padx=50, pady=5, sticky='w')
            entry = Entry(self)
            entry.grid(row=i+1, column=1, padx=50, pady=5, sticky='w')
            self.user_dirs[file_type] = entry

    def start_button(self, path_value):
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
        self.start_Button.grid(row=5, column=4, pady=5, padx=20)

    def _start(self, path_value):
        # Main function to sort files
        count = 0
        os.chdir(path_value)  # Change directory to selected folder
        self.file_list = os.listdir()  # Stores file names in file_list
        num_files = len(self.file_list)
        if len(self.file_list) == 0:
            self.empty_error = Label(text='This folder is empty')
            self.empty_error.grid(row=2, column=0, pady=5)
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
                    # Sets custom directory if given
                    user_dir = self.user_dirs[directory].get()
                    self.dir_name = user_dir if user_dir else directory
                    break

            self.new_path = os.path.join(path_value, self.dir_name)
            self.file_list = os.listdir()
            if self.dir_name not in self.file_list:
                os.mkdir(self.new_path)
            shutil.move(file, self.new_path)  # Moves file to new location
            count += 1

        if count == num_files:
            self.finish_success = Label(text='Success!')
            self.finish_success.grid(row=5, column=1, pady=5)
        else:
            self.finish_error = Label(text='Task Failed')
            self.finish_error.grid(row=5, column=1, pady=5)


if __name__ == '__main__':
    app = GUI()
    app.mainloop()
