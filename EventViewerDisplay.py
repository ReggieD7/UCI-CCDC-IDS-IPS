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
from tkinter import Scrollbar
from tkinter import Listbox
from tkinter import filedialog

from EventViewer import query_event_viewer
from EventViewer import gen

from FileMonitor import make_checksum
from FileMonitor import get_meta_data
from FileMonitor import check_checksum

from threading import *
import time
from time import strftime, gmtime
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
        
        #Default Log Monitor Filter Values
        self.logType="Security"
        self.IDNum=""
        self.numOfEntries="all"
        self.newestLogsFirst=True
        self.logFrequency=300

        self.log_output= StringVar()
        self.log_output.set("")
        self.continueBackGroundProcess_logMonitor= True
        
        #Default File Monitor Filter Values
        self.fileName_input= StringVar()
        self.fileName_input.set("<File>")
        self.continueBackGroundProcess_fileMonitor= True
        self.fileName=""
        self.checkFrequency=1
        self.checkResults= StringVar()
        self.checkResults.set("")
        
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
                                 master=self.root, borderwidth=2, relief='sunken')
        title_label = Label(panel_config,
                            text="<---------------------------Filter Options--------------------------->",
                            padx=padding, pady=padding, bg="orange", font=("Helvetica", 10, "bold"))
        title_label.grid(row=0, columnspan=3, padx=padding, pady=10)
        
        logMonitor_options= Label(panel_config, text= "<---------Log Monitor Options--------->", padx=padding, pady= padding, bg="dodger blue", font=("Helvetica", 8, "bold"))
        logMonitor_options.grid(row=1, columnspan=3)
        
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
        log_age_label = Label(master=panel_config, text="Oldest Logs First?")
        log_age_label.grid(row=5, column=0, padx=padding, pady=padding)
        self.isOld = IntVar(panel_config)
        self.age_check_button = Checkbutton(master=panel_config,
                                       variable=self.isOld)
        self.age_check_button.grid(row=5, column=1)
        
        # Periodic Check
        periodic_label = Label(master=panel_config, text="Log Frequency")
        periodic_label.grid(row=6, column=0, padx=padding, pady=padding)
        amount_to_display_logMonitor = StringVar()
        self.periodic_field = Entry(master=panel_config, width=5, textvariable=amount_to_display_logMonitor,
                               command=None)
        self.periodic_field.grid(row=6, column=1)
        
        # Action Buttons
        self.submit_button_logMonitor = Button(panel_config, text="Submit", bd=2,
                               pady=padding, padx=padding, command=self.submitForm_logMonitor)
        self.submit_button_logMonitor.grid(row=7, column=1)
        self.clear_button_logMonitor = Button(panel_config, text="Clear", bd=2, 
                              pady=padding, padx=padding, command=self.clearEntries_logMonitor)
        self.clear_button_logMonitor.grid(row=7, column=2, padx= padding, pady= padding)
        panel_config.pack(fill="both", expand=True)
        
        logMonitor_options= Label(panel_config, text= "<------File Activity Monitor Options------>", padx=padding, pady= padding, bg="dodger blue", font=("Helvetica", 8, "bold"))
        logMonitor_options.grid(row=8, columnspan=3, pady= 10)
        
        filePath_label= Label(panel_config, text="File Path", padx= padding, pady= padding)
        filePath_label.grid(row=9, column=0, padx= padding, pady= padding)
        
        
        self.filePath_button= Button(panel_config, textvariable=self.fileName_input, padx= padding, pady= padding, command=self.handleFileName_Button)
        self.filePath_button.grid(row=9, column=1, padx= padding, pady= padding)
        
        timeCheck_label= Label(panel_config, text="Frequency of Checks", padx= padding, pady= padding)
        timeCheck_label.grid(row=10, column=0, padx= padding, pady= padding)
        
        amount_to_display_fileMonitor= StringVar()
        self.timeCheck_entry= Entry(panel_config, width=5, textvariable= amount_to_display_fileMonitor)
        self.timeCheck_entry.grid(row=10, column= 1)
        
        self.submit_button_fileMonitor = Button(panel_config, text="Submit", bd=2,
                               pady=padding, padx=padding, command=self.submitForm_fileMonitor)
        self.submit_button_fileMonitor.grid(row=11, column=1)
        self.clear_button_fileMonitor = Button(panel_config, text="Clear", bd=2, 
                              pady=padding, padx=padding, command=self.clearEntries_fileMonitor)
        self.clear_button_fileMonitor.grid(row=11, column=2, padx= padding, pady= padding)
        panel_config.pack(fill="both", expand=True)

        return panel_config

    # Create the Table

    def createTableLogFrame(self):
        # bg="#23272a"
        padding=5
        frame = ttk.Frame(self.root, width=self.width * 0.5, height=self.height, relief="sunken")
        treeview = ttk.Treeview(frame)
        title=Label(frame, text="<--------------------------------------------------------------------------Log Information--------------------------------------------------------------------------->"
                    ,padx=padding, pady=padding, bg="orange", font=("Helvetica", 10, "bold"))
        title.grid(row=0, columnspan=2, padx=padding, pady=padding)
        
        pauseButton= Button(frame, text="Pause", command=self.stopFunction_logMonitor)
        pauseButton.grid(row=1, column=0)
        
        resumeButton= Button(frame, text="Continue", command=self.resumeFunction_logMonitor)
        resumeButton.grid(row=1, column=1)
        
        scrollBar = Scrollbar(frame)
        scrollBar.grid(rowspan=2, column=1,sticky="nse")
        
        self.consoleOutput_logMonitor = Listbox(frame, yscrollcommand=scrollBar.set, height= 55, width= 114, 
                                     relief="sunken", borderwidth=5)
        self.consoleOutput_logMonitor.grid(row=2, columnspan=2, padx=5, pady=5)

        scrollBar.config(command=self.consoleOutput_logMonitor.yview)
        
        return frame

    def createNotificationFrame(self):
        padding=5
        frame = ttk.Frame(self.root, width=self.width * 0.25, height=self.height, relief="sunken")
        title=Label(frame, text="<---------------------------------------------------------------------------------File Activity Monitor---------------------------------------------------------------------------------->"
                    ,padx=padding, pady=padding, bg="orange", font=("Helvetica", 10, "bold"))
        title.grid(row=0, columnspan=2, padx=padding, pady=padding)
        
        pauseButton= Button(frame, text="Pause", command=self.stopFunction_fileMonitor)
        pauseButton.grid(row=1, column=0)
        
        resumeButton= Button(frame, text="Continue", command=self.resumeFunction_fileMonitor)
        resumeButton.grid(row=1, column=1)
        
        scrollBar = Scrollbar(frame)
        scrollBar.grid(rowspan=2, column=1,sticky="nse")
        
        self.fileStatus_box = Listbox(frame, yscrollcommand=scrollBar.set, height= 55, width= 114, 
                                     relief="sunken", borderwidth=5)
        self.fileStatus_box.grid(row=2, columnspan=2, padx=5, pady=5)

        scrollBar.config(command=self.fileStatus_box.yview)
        
        return frame
        

    def getLogTypeValue(self, value):
        self.logType= value
    
    def clearEntries_logMonitor(self):
        self.log_id_field.delete(0, 'end')
        self.numOfEntries_field.delete(0, 'end')
        self.periodic_field.delete(0, 'end')
        self.isOld.set(0)                
        self.default_selection.set("Security")
            
    
    def submitForm_logMonitor(self):
        
        self.IDNum= self.log_id_field.get()
        self.numOfEntries= self.numOfEntries_field.get()
        self.newestLogsFirst= self.isOld.get()
        self.logFrequency=self.periodic_field.get()
        
        liveConsoleOutput_logMonitor = Thread(target=self.handleInputs_logMonitor)
        liveConsoleOutput_logMonitor.daemon=True
        liveConsoleOutput_logMonitor.start()
        
    def clearEntries_fileMonitor(self):
        
        self.fileName_input.set("<File>")
        self.timeCheck_entry.delete(0,'end')
        
        
    def submitForm_fileMonitor(self):
        
        self.checkFrequency= self.timeCheck_entry.get()
        
        liveConsoleOutput_fileMonitor = Thread(target=self.handleInputs_fileMonitor)
        liveConsoleOutput_fileMonitor.daemon=True
        liveConsoleOutput_fileMonitor.start()
        
    def handleFileName_Button(self):
    
        root = tk.Tk()
        root.withdraw() # use to hide tkinter window
        self.fileName = filedialog.askopenfilename()
        if self.fileName== "":
            self.fileName_input.set("<File>")
        else:
            self.fileName_input.set(self.fileName)
        
    def handleInputs_logMonitor(self):
        user_inputs= [self.logType, self.IDNum, self.numOfEntries, self.newestLogsFirst]
        duration= int(self.logFrequency)
        info = query_event_viewer(user_inputs[0], user_inputs[1], user_inputs[2], user_inputs[3])
        num=1
        while self.continueBackGroundProcess_logMonitor:
            time.sleep(duration)
            parsed_info = gen(info)
            parsed_info_arr= []
            for i in parsed_info:
                parsed_info_arr.append(i)
            parsed_info_arr.append("<-------------------------------->")
            for i in range(len(parsed_info_arr)):
                if i==0:
                    self.consoleOutput_logMonitor.insert(i, ("%d). %s" % (num, parsed_info_arr[i])))
                else:
                    self.consoleOutput_logMonitor.insert(i, "     " + parsed_info_arr[i])
            num+=1
            
    def handleInputs_fileMonitor(self):
        while self.continueBackGroundProcess_fileMonitor:
            if len(self.fileName) > 0:
                original_hash = make_checksum(self.fileName)
            
                time.sleep(float(self.checkFrequency)*3600)
            
                updated_hash = make_checksum(self.fileName)
            
                check_if_hashs_are_equal = check_checksum(original_hash, updated_hash)
                
                time_current = strftime("%H:%M:%S", gmtime())
            
                if check_if_hashs_are_equal:
                    self.fileStatus_box.insert(0, f'{time_current} | File has not been altered')
                    self.fileStatus_box.insert(1, '<-------------------------------->')
                else:
                    meta_data = get_meta_data(self.fileName)
                    self.fileStatus_box.insert(0, f'{time_current} | File: {self.fileName}')
                    self.fileStatus_box.insert(1, f'{time_current} | File size before: {file_size_before} bytes')
                    self.fileStatus_box.insert(2, f'{time_current} | File size after: {meta_data[0]} bytes')
                    self.fileStatus_box.insert(3, f'{time_current} | Date and Time ALtered: {meta_data[1]}')
                    self.fileStatus_box.insert(4, '<-------------------------------->')

            
    def resumeFunction_logMonitor(self):
        self.continueBackGroundProcess_logMonitor=True
    
    def stopFunction_logMonitor(self):
        self.continueBackGroundProcess_logMonitor=False   
        
    def resumeFunction_fileMonitor(self):
        self.continueBackGroundProcess_fileMonitor=True
    
    def stopFunction_fileMonitor(self):
        self.continueBackGroundProcess_fileMonitor=False
        
        
                    

if __name__ == "__main__":
    EventViewerDisplay()