import tkinter as tk

from tkinter import ttk

class EventViewerDisplay:
    '''
        Acts as the window display for Events
    '''

    def __init__(self):
        ''' Creates The Window and runs main loop'''
        # Configuring Root Window
        self.root = tk.Tk()
        self.root.title("Cyber@UCI IDPS Display Manager")
        self.height = 500
        self.width = 500
        canvas_bg = tk.Canvas(self.root, height=self.height, width=self.width, bg="#2c2f33")
        canvas_bg.pack()

        # Main Frame
        self.root_frame = ttk.Frame(self.root)
        self.root_frame.pack(expand=True)
        self.root.mainloop()

    def createWindowLogFrame(self):
        window_log_frame = ttk.Frame(self.root_frame, bg="#23272a")
        window_log_frame.pack(side="left", fill="Y")

    def createEventLogFrame(self):
        pass

    def createNotificationFrame(self):
        pass


if __name__ == "__main__":
    EventViewerDisplay();