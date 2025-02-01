from tkinter import Event, StringVar, filedialog
from typing import List

from tkinter.ttk import Button, Frame, Label, Style, Spinbox, Combobox
from ttkthemes import ThemedTk

from utils import Options, time_choices

class MainPage():
    def __init__(self, parent: ThemedTk, opts: Options, start_func):
        self.__parent = parent
        self.__opts = opts
        self.__start_func = start_func

    def build(self):
        self.__frame = Frame(self.__parent, padding=(10, 10))
        self.__frame.pack(fill="both", expand=True)

        self.__frame.update()
        self.__initialize()

    def __initialize(self):
        self.__folder_frame_container = Frame(self.__frame)
        self.create_start_button()
        self.create_options()
        self.__refresh_selected_folders()
        
        self.__folder_frame_container.pack(side="top", fill="both", expand=True)
    
    def ask_folder(self):
        folder_name = filedialog.askdirectory()
        if len(folder_name) > 0:
            self.__opts.selected_folders.append(folder_name)
            self.__refresh_selected_folders()

    def __refresh_selected_folders(self):
        for folder_frame in self.__folder_frame_container.winfo_children():
            folder_frame.destroy()

        # Recreate the button...
        self.create_directory_button()

        folder_entries: List[Frame] = []
        for i, folder in enumerate(self.__opts.selected_folders):
            folder_entries.append(self.__create_folder_entry(folder, i))

        for entry in folder_entries:
            entry.pack(fill="x")

    def create_delete_func(self, i):
        def delete_selected_folder():
            nonlocal i
            del self.__opts.selected_folders[i]

            self.__refresh_selected_folders()

        return delete_selected_folder

    def __create_folder_entry(self, folder_name, i) -> Frame:
            new_folder_entry = Frame(self.__folder_frame_container)
            folder_label = Label(new_folder_entry, text=folder_name)
            folder_delete_button = Button(new_folder_entry, text="de-select", command=self.create_delete_func(i))
            folder_label.pack(side="left")
            folder_delete_button.pack(side="right")

            return new_folder_entry

    def create_start_button(self):
        # TODO: disable button if length of folders is zero.
        s = Style()
        s.configure("my.TButton", font=("Arial", 20))

        self.__start_button_frame = Frame(self.__frame, padding=(0, 5))
        Button(self.__start_button_frame, text="Start Session", command=self.start_quickdraw_countdown, style="my.TButton").pack()
        self.__start_button_frame.pack(fill="both")

    def create_options(self):
        self.__options_frame = Frame(self.__frame, padding=(int(self.__frame.winfo_width() / 4) - 10, 5))
        num_images_frame = self.generate_num_images_option()
        pose_time_frame = self.generate_time_choices_option()
 
        num_images_frame.pack(fill="x")
        pose_time_frame.pack(fill="x")
        self.__options_frame.pack(fill="both")

    def generate_time_choices_option(self):
        image_time_frame = Frame(self.__options_frame)
        image_time_label = Label(image_time_frame, text="Time Per Image:", font=("Arial", 20))

        selected_index = list(time_choices.values()).index(self.__opts.image_time_seconds)
        selected_time = StringVar(self.__frame, list(time_choices.keys())[selected_index])
        time_selection_box = Combobox(
            image_time_frame,
            textvariable=selected_time,
            values=list(time_choices.keys())
        )
        time_selection_box.bind("<<ComboboxSelected>>", lambda event, v=selected_time: self.update_opts_pose_time(event, selected_time))
        image_time_label.pack(side="left")
        time_selection_box.pack(side="right")

        return image_time_frame
    
    def generate_num_images_option(self):
        num_images_frame = Frame(self.__options_frame)
        num_images_label = Label(num_images_frame, text="Number of Images:", font=("Arial", 20))

        count_text = StringVar(self.__frame, self.__opts.image_count)
        image_count = Spinbox(
            num_images_frame, 
            textvariable=count_text, 
            from_=2, 
            to=1000, 
            command=lambda v=count_text: self.update_opts_image_count(count_text),
            validate="key",
            validatecommand=(self.__frame.register(self._validate_numeric), "%P"))
        image_count.bind("<Key>", lambda event, v=count_text: self.handle_key_img_count(event, count_text))
        num_images_label.pack(side="left")
        image_count.pack(side="right")

        return num_images_frame

    def create_directory_button(self):
        s = Style()
        s.configure("my.TButton", font=("Arial", 20))
        self.__button_frame = Frame(self.__folder_frame_container)
        Button(self.__button_frame, text="Add Directory", command=self.ask_folder, style="my.TButton").pack()
        self.__button_frame.pack(pady=20)
    
    def start_quickdraw_countdown(self):
        self.__start_func()

    def update_opts_image_count(self, image_count: StringVar):
        self.__opts.image_count = int(image_count.get())

    def update_opts_pose_time(self, event, time_var: StringVar):
        self.__opts.image_time_seconds = time_choices[time_var.get()]
        print(self.__opts.image_time_seconds)

    def handle_key_img_count(self, event: Event, image_count: StringVar):
        if event.char.isnumeric():
            self.__opts.image_count = int(image_count.get() + event.char)
        elif event.keysym=="BackSpace":
            if len(image_count.get()) > 1:
                self.__opts.image_count = int(image_count.get()[:-1])
            else:
                self.__opts.image_count = 1

        # at the very least, ceil it to 1000 if it doesn't handle that natively in tkinter.
        if self.__opts.image_count > 1000:
            image_count.set("1000")
            self.__opts.image_count = 1000

    def _validate_numeric(self, P):
        return P.isdigit()

    def destroy(self):
        self.__frame.destroy()
