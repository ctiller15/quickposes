from tkinter import filedialog
from typing import List

from tkinter.ttk import Button, Frame, Label
from ttkthemes import ThemedTk

class MainPage():
    def __init__(self, parent: ThemedTk, start_func):
        self.__parent = parent
        self.__start_func = start_func

    def build(self):
        self.__frame = Frame(self.__parent, padding=(10, 10))
        self.__frame.pack(fill="both", expand=True)

        self.__selected_folders = []

        self.__initialize()
    
    def ask_folder(self):
        folder_name = filedialog.askdirectory()
        if len(folder_name) > 0:
            self.__selected_folders.append(folder_name)
            self.__refresh_selected_folders()

    def __refresh_selected_folders(self):
        print(self.__folder_frame_container.winfo_children())
        for folder_frame in self.__folder_frame_container.winfo_children():
            folder_frame.destroy()

        # Recreate the button...

        self.create_directory_button()

        folder_entries: List[Frame] = []
        for i, folder in enumerate(self.__selected_folders):
            folder_entries.append(self.__create_folder_entry(folder, i))

        print(folder_entries)
        for entry in folder_entries:
            entry.pack(fill="x")

    def create_delete_func(self, i):
        def delete_selected_folder():
            nonlocal i
            del self.__selected_folders[i]

            self.__refresh_selected_folders()

        return delete_selected_folder

    def __create_folder_entry(self, folder_name, i) -> Frame:
            new_folder_entry = Frame(self.__folder_frame_container)
            folder_label = Label(new_folder_entry, text=folder_name)
            folder_delete_button = Button(new_folder_entry, text="de-select", command=self.create_delete_func(i))
            folder_label.pack(side="left")
            folder_delete_button.pack(side="right")

            return new_folder_entry

            # self.__folder_frame.pack()

    def __initialize(self):
        self.__start_button_frame = Frame(self.__frame, padding=(0, 5))
        Button(self.__start_button_frame, text="start session", command=self.start_quickdraw_countdown).pack()
        self.__folder_frame_container = Frame(self.__frame)
        self.__start_button_frame.pack(fill="both")
        
        self.create_directory_button()
        
        self.__folder_frame_container.pack(side="top", fill="both", expand=True)
        
    def create_directory_button(self):
        self.__button_frame = Frame(self.__folder_frame_container)
        Button(self.__button_frame, text="Add directory", command=self.ask_folder).pack()
        self.__button_frame.pack(pady=20)
    
    def start_quickdraw_countdown(self):
        self.__start_func(self.__selected_folders)

    def destroy(self):
        # Clear out all frames.
        self.__frame.destroy()
