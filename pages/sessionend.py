from tkinter import Canvas
from PIL import ImageTk, Image
from tkinter.ttk import Button, Frame, Label, Scrollbar, Style
import tkinter as tk


class SessionEnd():
    def __init__(self, parent, images_seen, visit_main_page):
        self.__parent = parent
        self.images_seen = images_seen
        self.images_list = []
        self.visit_main_page = visit_main_page

    def build(self):
        # Move out of here. Child should not be modding parent state.
        self.__parent.columnconfigure(0, weight=1)
        self.__parent.rowconfigure(0, weight=1)
        self.__frame = Frame(self.__parent, padding=(10, 10))

        self.__frame
        self.__frame.pack(expand=True, fill="both")
        # Force an update to have winfo width and height display correctly.
        self.__frame.update()

        self.__show_images()

    def __show_images(self):
        s = Style()
        s.configure("my.TButton", font=("Arial", 30))
        header = Frame(self.__frame)

        frame_label = Label(header, text="Session Complete!", font=("Arial", 30))
        frame_label.pack(side="left")

        restart_button = Button(header, text="New Session", style="my.TButton", command=self.new_session)
        restart_button.pack(side="right")

        header.grid(row=0, column=0, sticky="nsew")

        sub_header = Label(self.__frame, text="Images Seen:", font=("Arial", 20))
        sub_header.grid(row=1, column=0, sticky="nsew")

        full_frame = Frame(self.__frame)
        full_frame.grid(row=2, column=0, sticky="nw")
        frame_width = self.__frame.winfo_width() - 20
        frame_height = self.__frame.winfo_height() - 80
        full_frame.configure(width=frame_width, height=frame_height)
        full_frame.grid_rowconfigure(0, weight=1)
        full_frame.grid_columnconfigure(0, weight=1)
        full_frame.grid_propagate(False)

        canvas = Canvas(full_frame)
        canvas.grid(row=0, column=0, sticky="nsew")

        vsb = Scrollbar(full_frame, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=vsb.set)

        frame_images = Frame(canvas)
        canvas.create_window((0, 0), window=frame_images, anchor="nw")

        row = 2
        col = 0

        img_container_width = int(frame_width / 5) - 8
        img_container_height = int(frame_height / 3) - 10

        for i in range(len(self.images_seen)):
            img = Image.open(self.images_seen[i])
            full_img = ImageTk.PhotoImage(img)
            img_aspect_ratio = float(full_img.width()) / float(full_img.height())

            width, height = self.crop_dims(img_container_width, img_container_height, img_aspect_ratio)
            # reassign. Refactor this after it's working.
            full_img = ImageTk.PhotoImage(img.resize((width, height)))

            img_label = tk.Label(frame_images, image=full_img, width=img_container_width, height=img_container_height)
            img_label.image = full_img
            img_label.grid(column=col, row=row, sticky="news")

            if col == 4:
                col = 0
                row += 1
            else:
                col += 1

        frame_images.update_idletasks()

        canvas.config(scrollregion=canvas.bbox("all"))

    def crop_dims(self, width, height, ratio):
        if width > height * ratio:
            width = int(height * ratio + .5)
        else:
            height = int(width/ratio + .5)
        return (width, height)
    
    def new_session(self):
        self.visit_main_page()

    def destroy(self):
        self.__frame.destroy()