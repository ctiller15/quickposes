from tkinter import Frame, Label


class QuickDraw():
    def __init__(self, parent, folders):
        self.__parent = parent
        self.__folders = folders

    def build(self):
        self.__frame = Frame(self.__parent, padx=10, pady=10)
        self.__frame.config(bg="red")
        self.__frame.pack(fill="both", expand=True)

        self.__initialize()
        print("building main page!")

    def __initialize(self):
        self.__image_frame = Frame(self.__frame, bg="purple", padx=10, pady=10)
        Label(self.__image_frame, text="3", font=("Arial", 120)).pack(fill="both", expand=True)
        self.__image_frame.pack(fill="both", expand=True)