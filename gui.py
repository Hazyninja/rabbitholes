from tkinter import *
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import threading
from file_sorter import FileSorter


class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.file_sorter = FileSorter()
        self.user_dirs = None
        self.file_list = None
        self.new_path = None
        self.empty_error = Label(self, text='')
        self.finish_success = Label(self, text='')
        self.finish_error = Label(self, text='')
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
        self.original_image = Image.open('Images/blue_texture.png')
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
            focuscolor='Black'
        )

        style.configure(
            'TLabel',
            foreground='Red',
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
        self.browse_Button.grid(row=5, column=0, sticky='w')

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
                target=self.file_sorter.start_sort, args=(
                    path_value, self.user_dirs, self.progress,
                    self.empty_error, self.finish_success, self.finish_error
                )
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
