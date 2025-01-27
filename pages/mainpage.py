from tkinter import Tk, filedialog, Frame, Label, Button


class MainPage():
    def __init__(self, parent: Tk, start_func):
        self.__parent = parent
        self.__start_func = start_func

    def build(self):
        self.__frame = Frame(self.__parent, padx=10, pady=10)
        self.__frame.config(bg="red")
        self.__frame.pack(fill="both", expand=True)

        self.__selected_folders = []

        self.__initialize()
        print("building main page!")
    
    def ask_folder(self):
        folder_name = filedialog.askdirectory()
        if len(folder_name) > 0:
            self.__selected_folders.append(folder_name)
            self.__refresh_selected_folders()

    def __refresh_selected_folders(self):
        for folder_frame in self.__folder_frame_container.winfo_children():
            folder_frame.destroy()

        for i, folder in enumerate(self.__selected_folders):
            self.__create_folder_entry(folder, i)

    def create_delete_func(self, i):
        def delete_selected_folder():
            nonlocal i
            del self.__selected_folders[i]

            self.__refresh_selected_folders()

        return delete_selected_folder

    def __create_folder_entry(self, folder_name, i):
            self.__folder_frame = Frame(self.__folder_frame_container, bg="yellow")
            folder_label = Label(self.__folder_frame, text=folder_name, wraplength=100)
            folder_delete_button = Button(self.__folder_frame, text="de-select", command=self.create_delete_func(i))
            folder_label.pack(side="left")
            folder_delete_button.pack(side="right")

            self.__folder_frame.pack(side="top", fill="both", expand=True)

    def __initialize(self):
        self.__start_button_frame = Frame(self.__frame, bg="green")
        Button(self.__start_button_frame, text="start session", command=self.start_quickdraw_countdown).pack()
        self.__button_frame = Frame(self.__frame, bg="blue")
        Button(self.__button_frame, text="Add directory", command=self.ask_folder).pack()
        self.__folder_frame_container = Frame(self.__frame, bg="orange")
        
        self.__start_button_frame.pack(fill="both", expand=True)
        self.__button_frame.pack(fill="both", expand=True)
        self.__folder_frame_container.pack(side="top", fill="both", expand=True)
        
    def start_quickdraw_countdown(self):
        self.__start_func(self.__selected_folders)

    def destroy(self):
        # Clear out all frames.
        self.__frame.destroy()
