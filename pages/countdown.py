from tkinter.ttk import Frame, Label

class Countdown():
    def __init__(self, parent, start_quickdraw):
        self.__parent = parent
        self.__start_quickdraw = start_quickdraw

    def build(self):
        self.__frame = Frame(self.__parent, padding=(10, 10))
        self.__frame.pack(fill="both", expand=True)

        self.__initialize()

    def __initialize(self):
        countdown_label = Label(self.__frame, font=("Arial", 200), name="countdown", anchor="center")
        countdown_label.pack(anchor="center", fill="both", expand=True)
        label = self.__frame.nametowidget('countdown')
        self.__frame.after(0, lambda: self.countdown(3, label))

    def countdown(self, i, label: Label):

        label['text'] = i

        if i > 0:
            i -= 1
            self.__frame.after(1000, lambda: self.countdown(i, label))
        else:
            print("starting!")
            self.__start_quickdraw()

    def destroy(self):
        self.__frame.destroy()