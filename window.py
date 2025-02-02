# import tkinter
import os
from ttkthemes import ThemedTk

from pages.mainpage import MainPage
from pages.countdown import Countdown
from pages.quickdraw import Quickdraw
from pages.sessionend import SessionEnd
from utils import Options, PageType

# TODO: distribute exe

class Window():
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        self.__root = ThemedTk(theme="equilux")
        width = self.__root.winfo_screenwidth() - 100
        height = self.__root.winfo_screenheight() - 100
        self.__root.iconbitmap(os.path.join(base_dir,"icon.ico"))
        self.__root.title("Quick Poses")
        self.__root.geometry(f"{width}x{height}")
        self.__root.configure(padx=10, pady=10)
        self.__current_page_type = PageType.MAIN_PAGE
        self.__current_page = None
        self.__options = Options()

    def __build_page(self):
        if self.__current_page is not None:
            self.__current_page.destroy()
            
        if self.__current_page_type == PageType.MAIN_PAGE:
            self.__current_page = MainPage(self.__root, self.__options, self.start_countdown)
            self.__current_page.build()
        elif self.__current_page_type == PageType.COUNTDOWN:
            self.__current_page = Countdown(self.__root, self.start_quickdraw)
            self.__current_page.build()
        elif self.__current_page_type == PageType.QUICK_DRAW:
            self.__current_page = Quickdraw(self.__root, self.__options, finish_quickdraw=self.finish_quickdraw)
            self.__current_page.build()
        elif self.__current_page_type == PageType.SESSION_END:
            self.__current_page = SessionEnd(self.__root, self.__viewed_images, self.visit_main_page)
            self.__current_page.build()

    def start_countdown(self):
        self.__current_page_type = PageType.COUNTDOWN
        self.__build_page()

    def start_quickdraw(self):
        self.__current_page_type = PageType.QUICK_DRAW
        self.__build_page()

    def finish_quickdraw(self, images):
        self.__viewed_images = images
        self.__current_page_type = PageType.SESSION_END
        self.__build_page()

    def visit_main_page(self):
        self.__current_page_type = PageType.MAIN_PAGE
        self.__build_page()

    def build(self):
        self.__build_page()
    
    def start(self):
        self.__root.mainloop()