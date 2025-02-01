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

# If these aren't sufficient, we can add a custom option.
time_choices = {
    "30s": 30,
    "45s": 45,
    "1m": 60,
    "1m30s": 90,
    "2m": 120,
    "3m": 180,
    "5m": 300,
    "10m": 600,
    "20m": 1200,
    "30m": 1800,
}