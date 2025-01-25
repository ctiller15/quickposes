import tkinter
from tkinter import E, N, S, W, ttk, filedialog

class Window():
    def __init__(self, width, height):
        self.__root = tkinter.Tk()
        # self.__root.wait_visibility(self.__root)
        self.__root.title = "Quick Poses"
        self.__root.geometry("800x600")
        self.__root.columnconfigure(index=0, weight=1)
        self.__root.rowconfigure(index=1, weight=1)


        self.__main_frame = ttk.Frame(self.__root, padding="3 3 12 12")
        self.__main_frame.grid(column=0, row=0, sticky=(N, W, E, S))

        self.__selected_folders = []

        self.__build_main_page()

        self.__root.mainloop()
    
    def __build_main_page(self):
        self.__button_frame = ttk.Frame(self.__main_frame).grid(column=0, row=0)
        ttk.Button(self.__button_frame, text="Add directory", command=self.ask_folder).place(relx=0.5, anchor='n')

    def create_delete_func(self, i):
        def delete_selected_folder():
            nonlocal i
            del self.__selected_folders[i]

            # remove all widgets past a certain row
            for widget in self.__root.grid_slaves():
                if int(widget.grid_info()["row"]) > 1:
                    widget.grid_forget()

            # Then recreate all of the appropriate widgets.
            for ind in range(len(self.__selected_folders)):
                self.__create_folder_entry(self.__selected_folders[ind], ind + 1)

        return delete_selected_folder

    def ask_folder(self):
        folder_name = filedialog.askdirectory()
        if len(folder_name) > 0:
            self.__selected_folders.append(folder_name)
            self.__create_folder_entry(folder_name, len(self.__selected_folders))

    def __create_folder_entry(self, folder_name, i):
            new_entry = ttk.Label(self.__root, width=14, text=folder_name, wraplength=100)
            new_entry.grid(column=0, row=i + 1, sticky="nsew")

            # i - 2 to fix 0-based indexing vs starting at row 2.
            entry_button = ttk.Button(self.__root, width=7, text="de-select", command=self.create_delete_func(i - 1))
            entry_button.grid(column=1, row=i + 1, sticky="WE")
