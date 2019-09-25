import tkinter as tk

from tkinter import ttk
from tkinter import Frame
from tkinter import Menu
from tkinter import Label
from tkinter import OptionMenu
from tkinter import StringVar
from tkinter import Entry
from tkinter.font import Font
from tkinter import Checkbutton
from tkinter import IntVar
from tkinter import Button
from tkinter import PanedWindow

from threading import *
from EventViewer import *
from EventViewerEntity import EventEntity
from EventViewerEntity import EventEntityManager


class EventViewerDisplay:
    """
        Acts as the window display for Events
    """

    def __init__(self):
        """
            Creates The Window and runs main loop
        """
        # Configuring Root Window
        self.root = tk.Tk()
        self.root.title("Cyber@UCI IDPS Display Manager")
        self.height = self.root.winfo_screenheight()
        self.width = self.root.winfo_screenwidth()
        # self.handleInputs = EventViewer()

        # Default Log Filter Values
        self.logType = "Security"
        self.IDNum = ""
        self.numOfEntries = "all"
        self.newestLogsFirst = True
        self.logFrequency = 300

        self.log_output = StringVar()
        self.log_output.set("")
        self.continueBackGroundProcess = True

        # Main Pane
        self.pane = PanedWindow(self.root, width=self.width, height=self.height,
                                bd=2, orient="horizontal")
        self.pane.grid(column=0, row=0)

        # File Menu
        menu_bar = self.createMenu()
        self.root.config(menu=menu_bar)

        # Multi Frames
        self.filter_frame = LogFrame(master=self.root,
                                     width=self.width*0.25,
                                     height=self.height*0.25)
        table_frame = self.createTableLogFrame()
        notification_frame = self.createNotificationFrame()

        self.pane.add(child=self.filter_frame)
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

    # Create the Table

    def createTableLogFrame(self):
        # bg="#23272a"
        padding = 5
        frame = ttk.Frame(self.root, width=self.width * 0.5, height=self.height, relief="sunken")
        treeview = ttk.Treeview(frame)
        title = Label(frame,
                      text="<-----------------------------------------------------------------------Log Information------------------------------------------------------------------------>"
                      , padx=padding, pady=padding, bg="orange", font=("Helvetica", 10, "bold"))
        title.grid(row=0, columnspan=2, padx=padding, pady=padding)

        stopButton = Button(frame, text="Stop", command=self.filter_frame.stopFunction)
        stopButton.grid(row=1, column=0)

        resumeButton = Button(frame, text="Continue", command=self.filter_frame.resumeFunction)
        resumeButton.grid(row=1, column=1)

        consoleOutput = Label(frame, textvariable=self.filter_frame.get_log_text(), anchor="w")
        consoleOutput.grid(row=2, columnspan=2)

        return frame

    def createNotificationFrame(self):
        frame = ttk.Frame(self.root, width=self.width * 0.25, height=self.height, relief="sunken")
        return frame

class LogFrame(Frame):
    """
        Class is reponsible for taking user inputs and producing
        the correct output
    """

    title_label: Label = None               # The Label for the title of the panel

    log_label: Label = None                 # The Label for the logs

    logCombo: OptionMenu = None             # The OptionMenu dropdown

    default_selection: StringVar = None     # Option Menu Selection is stored

    id_label: Label = None                  # The Label for the id

    id: StringVar = None                    # The value of the id

    number_of_events_field: Entry = None    # The field for the amount of events to load in

    isAll: IntVar = None                    # The variable for loading all events

    log_id_label: Label = None              # The Log ID label

    log_id_field: Entry = None              # The field where id is entered

    amount_to_display: StringVar = None     # The variable to store amount of entities

    display_checkbutton: Checkbutton = None # CheckButton for stuff

    log_age_label: Label = None             # Label for the item age

    isOld: IntVar = None                    # Stores whether user wants to see old logs

    age_check_button: Checkbutton = None    # CheckButton for checks

    periodic_label: Label = None            # Label for the Frequency for checking

    freq: StringVar = None                  # The frequency of occurence

    periodic_field: Entry = None            # The field for the amount of hours

    submit_button: Button = None            # The submission button

    clear_button: Button = None             # Clears changes made

    continueBackGroundProcess: bool = True  # Boolean indicator if the thread is running

    def __init__(self, master=None, **kwargs):
        """
            Initializes the LogFrame
            :param master: The root frame
            :param kwargs:
        """
        Frame.__init__(self, master, **kwargs)
        self.grid()
        self.log_output: StringVar = StringVar(self)  # The output to the console
        self.log_output.set('')
        self.create_filter_log_frame()

    def create_filter_log_frame(self):
        """
            The frame where the user will be able
            to input their data
        """
        padding = 5
        font_field = Font(family="Helvetica", size=10, weight="bold")

        panel_config = Frame(width=(self.winfo_screenwidth() * 0.25),
                             height=(self.winfo_screenheight() * 0.25),
                             master=self, borderwidth=2)
        self.title_label = Label(panel_config,
                                 text="<---------------------------Filter Options--------------------------->",
                                 padx=padding, pady=padding, bg="orange", font=font_field)
        self.title_label.grid(row=0, columnspan=3, padx=padding, pady=padding)

        # Log Type
        self.log_label = Label(panel_config, text="Log Type", anchor="w")
        self.log_label.grid(row=2, column=0, rowspan=1, padx=padding, pady=padding)
        choices = ["Security", "Application", "System", "Setup"]
        self.default_selection = StringVar(panel_config)  #Todo Add to var list
        self.default_selection.set(choices[0], )
        self.logCombo = OptionMenu(panel_config, self.default_selection,
                              *choices, command=None)
        self.logCombo.grid(row=2, column=1, columnspan=2, padx=padding, pady=padding)

        # Log ID
        self.id_label = Label(master=panel_config, text="ID Number", anchor="w") \
            .grid(row=3, column=0, padx=padding, pady=padding)
        self.id = StringVar(panel_config)
        self.log_id_field = Entry(master=panel_config, width=5, textvariable=id,
                                  command=None)
        self.log_id_field.grid(row=3, column=1)

        # Entries to display
        self.log_id_label = Label(master=panel_config,
                                  text="Number of Entries", anchor="w") \
            .grid(row=4, column=0, padx=padding, pady=padding)
        self.amount_to_display = StringVar(panel_config)
        self.number_of_events_field = Entry(master=panel_config, width=5,  # Todo Add this to my list
                                            textvariable=self.amount_to_display,
                                            command=None)
        self.number_of_events_field.grid(row=4, column=1)
        self.isAll = IntVar(panel_config)
        self.display_checkbutton = Checkbutton(master=panel_config, text="All",
                                               variable=self.isAll).grid(row=4, column=2)

        # Display oldest logs first
        self.log_age_label = Label(master=panel_config,
                                   text="Oldest Logs First?") \
            .grid(row=5, column=0, padx=padding, pady=padding)
        self.isOld = IntVar(panel_config)
        self.age_check_button = Checkbutton(master=panel_config,
                                            variable=self.isOld)
        self.age_check_button.grid(row=5, column=1)

        # Periodic Check
        self.periodic_label = Label(master=panel_config,
                                    text="Log Frequency") \
            .grid(row=6, column=0, padx=padding, pady=padding)
        self.freq = StringVar(panel_config)
        self.periodic_field = Entry(master=panel_config, width=5,
                                    textvariable=self.freq,
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

    def submitForm(self):
        """
            Gets the inputs the user writes and runs a seperate
            thread to get continuous log data
            :return: None
        """
        log_type = self.default_selection.get()
        IDNum = self.log_id_field.get()
        numOfEntries = self.number_of_events_field.get()
        newestLogsFirst = self.isOld.get()
        logFrequency = self.periodic_field.get()

        liveConsoleOutput = Thread(target=self.handleInputs,
                                   args=(log_type, IDNum, numOfEntries, newestLogsFirst, logFrequency))
        liveConsoleOutput.daemon = True
        liveConsoleOutput.start()

    def clearEntries(self):
        """
            Resets the inputs that the user can place in
            :return: None
        """
        self.log_id_field.delete(0, 'end')
        self.number_of_events_field.delete(0, 'end')
        self.periodic_field.delete(0, 'end')
        self.isOld.set(0)
        self.default_selection.set("Security")

    def handleInputs(self, log_type: str, id_num: int, num_of_entries: int, newest_logs_first: str, log_frequency: int):
        """
            Handles Submissions the user does for Monitoring Events
            :param log_type: The EventViewer Log to look at
            :param id_num: The id of the event type ex 4624
            :param num_of_entries: The amount of entries to display
            :param newest_logs_first: whether to show old logs or new logs
            :param log_frequency: the time to have this run in seconds
            :return: None
        """
        duration = int(log_frequency)
        info = query_event_viewer(log_type, id_num, num_of_entries, newest_logs_first)
        logText = ""
        while self.continueBackGroundProcess:  # Runs the code in the background
            time.sleep(duration)
            ev_entity = EventEntity(info)
            logText += '\n' + str(ev_entity)
            self.log_output.set(logText)
            # print(logText)

    def resumeFunction(self):
        """
            Resumes the thread for running
            :return: None
        """
        self.continueBackGroundProcess = True

    def stopFunction(self):
        """
            Stops the thread from running
            :return: None
        """
        self.continueBackGroundProcess = False

    def get_log_text(self):
        """
            Returns output for the event log_output
            :return: log_output
        """
        return self.log_output


if __name__ == "__main__":
    EventViewerDisplay()