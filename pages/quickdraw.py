import os
import random
from tkinter import Event, Frame, Label
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
        self.__frame.after(0, lambda: self.cycle_images(self.image_count))

    def cycle_images(self, images_remaining):
        if images_remaining > 0:
            images_remaining -= 1
            self.__set_next_image()
            self.__frame.after(10000, lambda: self.cycle_images(images_remaining))
        else:
            print("quickdraw complete!")
            self.finish_quickdraw(self.__seen_images)
            # Start completion page.
            # Pass in all completed quickdraw image links
            # Show all completed images

    def __set_next_image(self):
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
        print(self.img_aspect_ratio)
        self.display_img = ImageTk.PhotoImage(self.img)

        # img = ImageTk.PhotoImage(file=next_image)
        self.image_label = Label(self.__frame, image=self.display_img, name="img_container")
        # image_label.image = img
        self.image_label.pack(fill="both", expand=True)
        self.image_label.bind('<Configure>', self._resize_image)

    def _resize_image(self, event: Event):
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
