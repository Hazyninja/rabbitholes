from tkinter import *
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import threading
import os
import shutil

# Added dictionary and generator for file extension sorting
"""This is a sorting script with a GUI that handles sorting by file
 extension. After selecting the folder needed to be sorted, click the start
 button to begin the sort. The files are sorted into three folders 
 that are created if needed inside the parent folder."""

# Added dynamic background
# Added styling to labels


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
        self.geometry('400x360')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.title('Rabbithole Sorter')

        # Canvas widget for background
        self.canvas = Canvas(self, width=400, height=360)
        self.canvas.grid(row=0, column=0, rowspan=11, columnspan=2, sticky='nsew')

        # Load image for background
        self.original_image = Image.open('Images/background.png')
        self.bg_image = ImageTk.PhotoImage(self.original_image.resize((400, 360)))

        # Attach image to canvas
        self.bg_image_obj = self.canvas.create_image(
            0, 0,
            anchor='nw',
            image=self.bg_image,
        )

        self.bind('<Configure>', self.resize_image)

        self.create_browse_button()
        self.define_dir()
        # Initialize progress bar
        self.progress = ttk.Progressbar(
            self, orient='horizontal',
            length=300, mode='determinate'
        )
        self.progress.grid(row=10, column=0, columnspan=2, pady=10)
        # Button styling
        style = ttk.Style()
        style.configure(
            'TButton',
            background='#1DAF28',
            foreground='Red',
            font=('High Tower Text', 12),
            relief='groove',
            highlightthickness=10,
            focuscolor='Black'
        )

        style.configure(
            'TLabel',
            foreground='RoyalBlue4',
            font=('High Tower Text', 12),

        )

    def create_browse_button(self):
        # Sets browse button in window
        self.button_Frame = Frame(self)
        self.button_Frame.grid(
            row=9, column=0,
            padx=5, pady=5,
            sticky='n'
        )
        self.browse_Button = ttk.Button(
            self.button_Frame, text='Browse',
            command=self.get_path,
            width=10,
        )
        self.browse_Button.grid(row=5, column=0, padx=5, pady=5, sticky='w')

    def get_path(self):
        self.path = filedialog.askdirectory()  # Opens directory dialog
        # Creates start button if one does not exist
        if self.path:
            if not self.start_Button:
                self.create_start_button(self.path)

    def define_dir(self):
        # User inputs for custom directory names
        self.user_dirs = {}
        file_types = [
            'ImgFiles', 'TextFiles',
            'Executables', 'CompressedFiles',
            'Audio', 'Video', 'Documents',
            'CodeFiles'
        ]
        # Retrieve the index and value for proper grid placement
        for i, file_type in enumerate(file_types):
            label = ttk.Label(
                self,
                text=f'{file_type} Directory Name: '
            )
            label.grid(row=i+1, column=0, padx=10, pady=1, sticky='e')
            entry = Entry(self)
            entry.grid(row=i+1, column=1, padx=10, pady=1, sticky='w')
            self.user_dirs[file_type] = entry

    def create_start_button(self, path_value):
        # Calls start_sort on click to begin sorting
        self.start_Button = ttk.Button(
            self.button_Frame, text='Start',
            command=lambda: threading.Thread(
                target=self.start_sort, args=(path_value,)
            ).start(),
            width=10,
        )
        self.start_Button.grid(row=5, column=5, pady=5, sticky='e')

    def resize_image(self, event):
        # Resizes the background dynamically
        self.canvas.config(width=event.width, height=event.height)

        # Resize background based on window size
        resized_image = self.original_image.resize((event.width, event.height))
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # update canvas with adjusted image
        self.canvas.itemconfig(self.bg_image_obj, image=self.bg_image)




    def start_sort(self, path_value):
        # Main function to sort files
        count = 0
        os.chdir(path_value)  # Change directory to selected folder
        self.file_list = os.listdir()  # Stores file names in file_list
        num_files = len(self.file_list)
        self.progress['maximum'] = num_files  # Sets progress bar count
        if len(self.file_list) == 0:
            # Checks if file list is empty and returns error if true
            self.empty_error = Label(text='This folder is empty')
            self.empty_error.grid(row=2, column=0, pady=5)
            exit()

        # Dictionary associating file extensions and directory names
        file_list = {
            'ImgFiles': (
                '.png', '.jpg', '.jpeg', '.gif',
                '.bmp', '.tiff', '.svg'
            ),
            'TextFiles': (
                '.txt', '.docx', '.pdf', '.rtf',
                '.md', '.odt', '.csv'
            ),
            'Executables': (
                '.exe', '.bat', '.sh', '.msi'
            ),
            'CompressedFiles': (
                '.rar', '.zip', '.7zip', '.tar',
                '.gz', '.bz2', '.xz'
            ),
            'Audio': (
                '.mp3', '.wav', '.aac', '.flac', '.ogg'
            ),
            'Video': (
                '.mp4', '.avi', '.mkv', '.mov', '.wmv'
            ),
            'Documents': (
                '.xlsx', '.pptx', '.ods'
            ),
            'CodeFiles': (
                '.py', '.java', '.cpp', '.js', '.html', '.css'
            )
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
            self.progress['value'] = count
            self.update_idletasks()

        if count == num_files:
            self.finish_success = Label(text='Success!')
            self.finish_success.grid(row=9, column=1, pady=5)
        else:
            self.finish_error = Label(text='Task Failed')
            self.finish_error.grid(row=9, column=1, pady=5)


if __name__ == '__main__':
    app = GUI()
    app.mainloop()
