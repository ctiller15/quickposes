# import tkinter
from ttkthemes import ThemedTk

from pages.mainpage import MainPage
from pages.countdown import Countdown
from pages.quickdraw import Quickdraw
from pages.sessionend import SessionEnd
from utils import Options, PageType

class Window():
    def __init__(self, width, height):
        self.__root = ThemedTk(theme="equilux")
        self.__root.title("Quick Poses")
        self.__root.geometry("800x600")
        self.__root.configure(padx=10, pady=10)
        self.__current_page_type = PageType.MAIN_PAGE
        self.__current_page = None
        self.__options = Options()

        self.__build_page()

        self.__root.mainloop()

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