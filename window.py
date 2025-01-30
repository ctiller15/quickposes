from enum import Enum
# import tkinter
from ttkthemes import ThemedTk

from pages.mainpage import MainPage
from pages.countdown import Countdown
from pages.quickdraw import Quickdraw
from pages.sessionend import SessionEnd

class PageType(Enum):
    MAIN_PAGE = 1
    COUNTDOWN = 2
    QUICK_DRAW = 3
    SESSION_END = 4

class Window():
    def __init__(self, width, height):
        self.__root = ThemedTk(theme="equilux")
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
            self.__current_page = MainPage(self.__root, self.start_countdown)
            self.__current_page.build()
        elif self.__current_page_type == PageType.COUNTDOWN:
            self.__current_page = Countdown(self.__root, self.start_quickdraw)
            self.__current_page.build()
        elif self.__current_page_type == PageType.QUICK_DRAW:
            self.__current_page = Quickdraw(self.__root, self.__selected_folders, image_count=5, finish_quickdraw=self.finish_quickdraw)
            self.__current_page.build()
        elif self.__current_page_type == PageType.SESSION_END:
            print("session end...")
            self.__current_page = SessionEnd(self.__root, self.__viewed_images)
            self.__current_page.build()

    def start_countdown(self, folders):
        print(f"starting quickdraw! with folders: {folders}")
        self.__selected_folders = folders
        self.__current_page_type = PageType.COUNTDOWN
        self.__build_page()
        # create quickdraw page

    def start_quickdraw(self):
        print("countdown finished! Starting quickdraw!")
        self.__current_page_type = PageType.QUICK_DRAW
        self.__build_page()

    def finish_quickdraw(self, images):
        print(f"finished quickdraw. Images seen: {images}")
        self.__viewed_images = images
        self.__current_page_type = PageType.SESSION_END
        self.__build_page()
