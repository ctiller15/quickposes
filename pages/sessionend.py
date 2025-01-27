from tkinter import Frame, Label
from PIL import ImageTk, Image


class SessionEnd():
    def __init__(self, parent, images_seen):
        self.__parent = parent
        self.images_seen = images_seen
        self.images_list = []

    def build(self):
        self.__frame = Frame(self.__parent, padx=10, pady=10)
        self.__frame.config(bg="purple")
        self.__frame.pack(fill="both", expand=True)

        self.__show_images()

    def __show_images(self):
        for i in range(len(self.images_seen)):
            img = Image.open(self.images_seen[i])
            img_copy = img.copy()
            self.images_list.append(ImageTk.PhotoImage(img))
            img_aspect_ratio = float(self.images_list[-1].width()) / float(self.images_list[-1].height())
            width, height = self.crop_dims(100, 100, img_aspect_ratio)
            # reassign. Refactor this after it's working.
            self.images_list[-1] = ImageTk.PhotoImage(img.resize((width, height)))

            img_label = Label(self.__frame, image=self.images_list[-1], width=60, height=80, padx=10, pady=10)
            img_label.config(bg="green")
            img_label.grid()

    def crop_dims(self, width, height, ratio):
        if width > height * ratio:
            width = int(height * ratio + .5)
        else:
            height = int(width/ratio + .5)
        return (width, height)

    def destroy(self):
        self.__frame.destroy()