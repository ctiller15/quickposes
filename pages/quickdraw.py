import os
import random
from tkinter import Button, Event, Frame, Label
from PIL import ImageTk, Image


VALID_IMAGE_EXTENSIONS = ["png", "jpeg", "jpg"]

class Quickdraw():
    image_label: Frame

    def __init__(self, parent, folders: list[str], image_count=10, finish_quickdraw=None):
        self.__parent = parent
        self.__folders = folders
        self.__seen_images = []
        self.__all_images = []
        self.image_count = image_count
        self.images_remaining = image_count
        self.finish_quickdraw = finish_quickdraw

        self.__gather_available_images()

    def build(self):
        self.__frame = Frame(self.__parent, padx=10, pady=10)
        self.__frame.config(bg="white")
        self.__frame.pack(fill="both", expand=True)

        self.__manage_draw_images()
        print("quickdrawing baby!")

    # Would make more sense to do this during the countdown phase.
    def __gather_available_images(self):
        for folder in self.__folders:
            for file in os.listdir(folder):
                ext = file.split(".")[len(file.split(".")) -1]
                if (ext in VALID_IMAGE_EXTENSIONS):
                    self.__all_images.append(os.path.join(folder,file))

    def __manage_draw_images(self):
        # should be a loop that goes for a set amount of time
        # After a timeout has passed, display new image on screen.
        # For convenience, just show a single random image right now.
        self.__frame.after(0, lambda: self.cycle_images())

    def cycle_images(self):
        if self.images_remaining > 0:
            self.images_remaining -= 1
            self.__set_next_image()
            # self.__frame.after(10000, lambda: self.cycle_images(images_remaining))
        else:
            print("quickdraw complete!")
            self.finish_quickdraw(self.__seen_images)

    def __set_next_image(self):
        # running into weirdness when resizing:
        # check https://stackoverflow.com/questions/58056320/why-does-this-code-make-the-tkinter-window-continuously-resize-grow-automaticall
        try:
            if self.image_label is not None:
                self.image_label.destroy()
        except AttributeError:
            pass

        next_image = self.chooseRandomImage()
        self.__seen_images.append(next_image)
        self.img = Image.open(next_image)
        self.img_copy = self.img.copy()
        self.img_aspect_ratio = float(self.img.width) / float(self.img.height)
        self.display_img = ImageTk.PhotoImage(self.img)

        self.image_label = Label(self.__frame, image=self.display_img, name="img_container")
        self.image_label.pack(fill="both", expand=True)
        self.image_label.bind('<Configure>', self._resize_image)

        self.info = Frame(self.image_label, width=self.img.width, height=(int(self.img.height * .1)), borderwidth=1, relief="solid")
        time_remaining = Label(self.info)
        self.info.place(relx=1.0, rely=1.0, x=-2, y=-2,anchor="se")
        self.__frame.after(0, lambda: self.countdown(10, time_remaining))
        time_remaining.pack(side="right")
        nav_buttons = Frame(self.info, width=400)
        prev_button = Button(nav_buttons, text="previous image")
        next_button = Button(nav_buttons, text="next image")
        prev_button.pack(side="left")
        next_button.pack(side="right")
        nav_buttons.pack(side="left", padx=(int(self.img.width / 20), int(self.img.width / 4)))
        # Move info into function that can rerun given a width and height.
    def countdown(self, i, label: Label):
        label['text'] = i

        if i > 0:
            i -= 1
            # Pauses when resizing. It's a convenient side-effect.
            self.__frame.after(1000, lambda: self.countdown(i, label))
        else:
            print("showing next image!")
            self.cycle_images()

    def _resize_image(self, event: Event):
        print(event.width, event.height)
        new_width, new_height = self.crop_dims(event.width, event.height, self.img_aspect_ratio)
        self.img = self.img_copy.resize((new_width, new_height))
        self.display_img = ImageTk.PhotoImage(self.img)
        self.image_label.configure(image=self.display_img)

    def chooseRandomImage(self):
        choice = random.randint(0, len(self.__all_images) - 1)
        chosen_image = self.__all_images[choice]
        # Remove random image from array.
        return chosen_image

    def crop_dims(self, width, height, ratio):
        if width > height * ratio:
            width = int(height * ratio + .5)
        else:
            height = int(width/ratio + .5)
        return (width, height)

    def destroy(self):
        self.__frame.destroy()
