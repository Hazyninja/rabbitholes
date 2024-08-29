import os
import shutil

class FileSorter:
    def __init__(self):
        self.file_list = {
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

    def start_sort(self, path_value, user_dirs, progress, empty_error_label, finish_success_label, finish_error_label):
        # Main function to sort files
        count = 0
        os.chdir(path_value)  # Change directory to selected folder
        file_list = os.listdir()  # Stores file names in file_list
        num_files = len(file_list)
        progress['maximum'] = num_files  # Sets progress bar count
        if len(file_list) == 0:
            # Checks if file list is empty and returns error if true
            empty_error_label.config(text='This folder is empty')
            empty_error_label.grid(row=2, column=0, pady=5)
            return

        # Iterate over files in directory
        for file in file_list:
            if os.path.isdir(file):
                count += 1
                continue

            # Default directory
            dir_name = 'Misc'

            for directory, filetypes in self.file_list.items():
                # Generator checks file type
                if any(file.lower().endswith(filetype) for filetype in filetypes):
                    # Sets custom directory if given
                    user_dir = user_dirs[directory].get()
                    dir_name = user_dir if user_dir else directory
                    break

            new_path = os.path.join(path_value, dir_name)
            file_list = os.listdir()
            if dir_name not in file_list:
                os.mkdir(new_path)
            shutil.move(file, new_path)  # Moves file to new location
            count += 1
            progress['value'] = count
            progress.update_idletasks()

        if count == num_files:
            finish_success_label.config(text='Success!')
            finish_success_label.grid(row=9, column=1, pady=5)
        else:
            finish_error_label.config(text='Task Failed')
            finish_error_label.grid(row=9, column=1, pady=5)
