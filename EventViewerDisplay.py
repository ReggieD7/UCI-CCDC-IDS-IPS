import tkinter as tk
from tkinter import ttk
from tkinter import Frame
from tkinter import Menu
from tkinter import Label
from tkinter import OptionMenu
from tkinter import StringVar
from tkinter import Entry
from tkinter import font
from tkinter import Checkbutton
from tkinter import IntVar
from tkinter import Button

from EventViewer import query_event_viewer
from EventViewer import gen

from threading import *
import time

class ColorScheme:
    pass


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
        #self.handleInputs = EventViewer()
        
        #Default Log Filter Values
        self.logType="Security"
        self.IDNum=""
        self.numOfEntries="all"
        self.newestLogsFirst=True
        self.logFrequency=300

        self.log_output= StringVar()
        self.log_output.set("")
        self.continueBackGroundProcess= True
        
        # bg="#23272a"
        # Main Pane
        self.pane = tk.PanedWindow(self.root, width=self.width, height=self.height, bd=3, orient="horizontal")
        self.pane.pack(fill="both", expand=False)

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

    def createFilterLogFrame(self):
        """
            The frame where the user will be able
            to input their data
        """ 
        padding = 5
        panel_config = Frame(width=(self.root.winfo_screenwidth() * 0.25),
                                 height=(self.root.winfo_screenheight() * 0.25),
                                 master=self.root, borderwidth=2)
        title_label = Label(panel_config,
                            text="<---------------------------Filter Options--------------------------->",
                            padx=padding, pady=padding, bg="orange", font=("Helvetica", 10, "bold"))
        title_label.grid(row=0, columnspan=3, padx=padding, pady=padding)
        
        # Log Type
        log_label = Label(panel_config, text="Log Type", anchor="w")
        log_label.grid(row=2, column=0, rowspan=1, padx=padding, pady=padding)
        choices = ["Security", "Application", "System", "Setup"]
        self.default_selection = StringVar(panel_config)
        self.default_selection.set(choices[0], )
        logCombo = OptionMenu(panel_config, self.default_selection,
                              *choices, command=self.getLogTypeValue)
        logCombo.grid(row=2, column=1, columnspan=2, padx=padding, pady=padding)
        
        # Log ID
        log_id_label = Label(master=panel_config, text="ID Number", anchor="w") \
            .grid(row=3, column=0, padx=padding, pady=padding)
        id = StringVar(panel_config)
        self.log_id_field = Entry(master=panel_config, width=5, textvariable=id,
                             command=None)
        self.log_id_field.grid(row=3, column=1)
        
        # Entries to display
        log_id_label = Label(master=panel_config,
                             text="Number of Entries", anchor="w") \
            .grid(row=4, column=0, padx=padding, pady=padding)
        amount_to_display = StringVar(panel_config)
        self.numOfEntries_field = Entry(master=panel_config, width=5, textvariable=amount_to_display,
                             command=None)
        self.numOfEntries_field.grid(row=4, column=1)
        isAll = IntVar(panel_config)
        display = Checkbutton(master=panel_config, text="All",
                              variable=isAll).grid(row=4, column=2)
        
        # Display oldest logs first
        log_age_label = Label(master=panel_config,
                              text="Oldest Logs First?") \
            .grid(row=5, column=0, padx=padding, pady=padding)
        self.isOld = IntVar(panel_config)
        self.age_check_button = Checkbutton(master=panel_config,
                                       variable=self.isOld)
        self.age_check_button.grid(row=5, column=1)
        
        # Periodic Check
        periodic_label = Label(master=panel_config,
                               text="Log Frequency") \
                        .grid(row=6, column=0, padx=padding, pady=padding)
        amount_to_display = StringVar(panel_config)
        self.periodic_field = Entry(master=panel_config, width=5, textvariable=amount_to_display,
                               command=None)
        self.periodic_field.grid(row=6, column=1)
        
        # Action Buttons
        self.submit_button = Button(panel_config, text="Submit", bd=2,
                               pady=padding, padx=padding, command=self.submitForm)
        self.submit_button.grid(row=7, column=1)
        self.clear_button = Button(panel_config, text="Clear", bd=2, 
                              pady=padding, padx=padding, command=self.clearEntries)
        self.clear_button.grid(row=7, column=2)
        panel_config.pack(fill="both", expand=True)

        return panel_config

    # Create the Table

    def createTableLogFrame(self):
        # bg="#23272a"
        padding=5
        frame = ttk.Frame(self.root, width=self.width * 0.5, height=self.height, relief="sunken")
        treeview = ttk.Treeview(frame)
        title=Label(frame, text="<-----------------------------------------------------------------------Log Information------------------------------------------------------------------------>"
                    ,padx=padding, pady=padding, bg="orange", font=("Helvetica", 10, "bold"))
        title.grid(row=0, columnspan=2, padx=padding, pady=padding)
        
        stopButton= Button(frame, text="Stop", command=self.stopFunction)
        stopButton.grid(row=1, column=0)
        
        resumeButton= Button(frame, text="Continue", command=self.resumeFunction)
        resumeButton.grid(row=1, column=1)
        
        consoleOutput = Label(frame, textvariable=self.log_output, anchor="w")
        consoleOutput.grid(row=2,columnspan=2)
        
        return frame

    def createNotificationFrame(self):
        frame = ttk.Frame(self.root, width=self.width * 0.25, height=self.height, relief="sunken")
        return frame
        

    def getLogTypeValue(self, value):
        self.logType= value
    
    def clearEntries(self):
        self.log_id_field.delete(0, 'end')
        self.numOfEntries_field.delete(0, 'end')
        self.periodic_field.delete(0, 'end')
        self.isOld.set(0)                
        self.default_selection.set("Security")
            
    
    def submitForm(self):
        
        self.IDNum= self.log_id_field.get()
        self.numOfEntries= self.numOfEntries_field.get()
        self.newestLogsFirst= self.isOld.get()
        self.logFrequency=self.periodic_field.get()
        
        liveConsoleOutput = Thread(target=self.handleInputs)
        liveConsoleOutput.daemon=True
        liveConsoleOutput.start()
        
    def handleInputs(self):
        user_inputs= [self.logType, self.IDNum, self.numOfEntries, self.newestLogsFirst]
        duration= int(self.logFrequency)
        info = query_event_viewer(user_inputs[0], user_inputs[1], user_inputs[2], user_inputs[3])
        logText= ""
        while self.continueBackGroundProcess:
            time.sleep(duration)
            parsed_info = gen(info)
            for i in parsed_info:
                logText = i + "\n" + logText
                self.log_output.set(logText)
                print(logText)
            
    def resumeFunction(self):
        self.continueBackGroundProcess=True
    
    def stopFunction(self):
        self.continueBackGroundProcess=False
        
                    

if __name__ == "__main__":
    EventViewerDisplay()