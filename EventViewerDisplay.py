import tkinter as tk

from tkinter import ttk
from tkinter import Menu

class EventViewerDisplay:
    '''
        Acts as the window display for Events
    '''

    def __init__(self):
        ''' Creates The Window and runs main loop'''
        # Configuring Root Window
        self.root = tk.Tk()
        self.root.title("Cyber@UCI IDPS Display Manager")
        self.height = self.root.winfo_screenheight()
        self.width = self.root.winfo_screenwidth()

        # bg="#23272a"
        # Main Pane
        self.pane = tk.PanedWindow(self.root, width=self.width, height=self.height,
                              bg="#002200", bd=2, orient="horizontal")
        self.pane.pack(fill="both", expand=True)

        # File Menu
        menu_bar = self.createMenu()
        self.root.config(menu=menu_bar)

        # Multi Frames
        filter_frame = self.createFilterLogFrame()
        table_frame = self.createTableLogFrame()
        notification_frame = self.createNotificationFrame()

        self.pane.add(child=filter_frame)
        self.pane.add(child=table_frame)
        self.pane.add(child=notification_frame)
        self.root.mainloop()

    def createMenu(self):
        """
        Creates a menu to be added to the root element
        :return: The menu bar for the display
        """
        menu_bar = Menu(self.root)
        # Creating the file menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit")
        file_menu.add_command(label="New")
        file_menu.add_separator()
        menu_bar.add_cascade(label="File", menu=file_menu)
        return menu_bar


    def createTableLogFrame(self):
        # bg="#23272a"
        frame = ttk.Frame(self.root, width=self.width * 0.5, height=self.height, relief="sunken")
        return frame

    # Create the Table


    def createFilterLogFrame(self):
        frame = ttk.Frame(self.root, width=self.width * 0.25, height=self.height, relief="sunken")
        return frame

    def createNotificationFrame(self):
        ttk.Frame(self.root, width=self.width * 0.25, height=self.height, relief="sunken")
        frame = ttk.Frame(self.root, width=self.width * 0.25, height=self.height, relief="sunken")
        return frame


if __name__ == "__main__":
    EventViewerDisplay();