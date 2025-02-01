from enum import Enum

class PageType(Enum):
    MAIN_PAGE = 1
    COUNTDOWN = 2
    QUICK_DRAW = 3
    SESSION_END = 4

class Options():
    image_count = 10
    image_time_seconds = 60
    selected_folders = []