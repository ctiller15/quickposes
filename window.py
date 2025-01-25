from enum import Enum
import tkinter
from tkinter import E, N, S, W, ttk, filedialog

from pages.mainpage import MainPage
from pages.quickdraw import QuickDraw

class PageType(Enum):
    MAIN_PAGE = 1
    QUICK_DRAW = 2

class Window():
    def __init__(self, width, height):
        self.__root = tkinter.Tk()
        self.__root.title = "Quick Poses"
        self.__root.geometry("800x600")
        self.__root.configure(bg="lightblue", padx=10, pady=10)
        self.__current_page_type = PageType.MAIN_PAGE
        self.__current_page = None

        self.__build_page()

        self.__root.mainloop()

    def __build_page(self):
        if self.__current_page is not None:
            self.__current_page.destroy()
            
        if self.__current_page_type == PageType.MAIN_PAGE:
            self.__current_page = MainPage(self.__root, self.start_quickdraw)
            self.__current_page.build()
        elif self.__current_page_type == PageType.QUICK_DRAW:
            self.__current_page = QuickDraw(self.__root, self.__selected_folders)
            self.__current_page.build()

    def start_quickdraw(self, folders):
        print(f"starting quickdraw! with folders: {folders}")
        self.__selected_folders = folders
        self.__current_page_type = PageType.QUICK_DRAW
        self.__build_page()
        # create quickdraw page
