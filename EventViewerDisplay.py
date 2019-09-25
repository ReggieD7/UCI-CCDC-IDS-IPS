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

import _thread
import time
import threading

import EventViewer as ev
from EventViewerEntity import EventEntity
from EventViewerEntity import EventEntityManager

class StyleTheme:
    '''
        Responsible for managing the style of everything
    '''
    background = "#323232"

    text_color = "#e9f1f7"


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

        # Main Pane
        self.pane = PanedWindow(self.root, width=self.width, height=self.height,
                                bd=2, orient="horizontal")
        self.pane.grid(column=0, row=0)

        # File Menu
        menu_bar = self.createMenu()
        self.root.config(menu=menu_bar)

        # Multi Frames
        filter_frame = LogFrame(master=self.root,
                                width=self.width*0.25,
                                height=self.height*0.25)
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
        frame = Frame(self.root, width=self.width * 0.5,
                      height=self.height, relief="sunken", bg=StyleTheme.background)
        treeview = ttk.Treeview(frame)
        return frame

    # Create the Table

    def createNotificationFrame(self):
        ttk.Frame(self.root, width=self.width * 0.25, height=self.height, relief="sunken")
        frame = ttk.Frame(self.root, width=self.width * 0.25, height=self.height, relief="sunken")
        return frame


class LogFrame(Frame):
    """
        Class is reponsible for taking user inputs and producing
        the correct output
    """

    title_label: Label = None               # The Label for the component

    log_label: Label = None                 # The Label for the logs

    logCombo: OptionMenu = None             # The ComboBox dropdown

    default_selection: StringVar = None     # Option Menu Selection

    id_label: Label = None                  # The Label for the id

    id: StringVar = None                    # The value of the id

    log_id_field: Entry = None              # The field where id is entered

    isAll: IntVar = None                    # The variable for loading all events

    log_id_label: Label = None              # The Log ID label

    amount_to_display: StringVar = None     # The variable to store amount of entities

    display_checkbutton: Checkbutton = None # CheckButton for stuff

    log_age_label: Label = None             # Label for the item age

    isOld: IntVar = None                    #

    age_check_button: Checkbutton = None    # CheckButton for checks

    periodic_label: Label = None            # Label for the Frequency for checking

    freq: StringVar = None                  # The frequency of occurence

    periodic_field: Entry = None            # The field for the amount of hours

    submit_button: Button = None            # The submission button

    clear_button: Button = None             # Clears changes made

    def __init__(self, master=None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.grid()
        self.create_filter_log_frame()

    def create_filter_log_frame(self):
        """
            The frame where the user will be able
            to input their data
        """
        # Styling
        padding = 5
        font_m = Font(family="Helvetica", size=16)
        font_s = Font(family="Helvetica", size=12)

        panel_config = Frame(width=(self.winfo_screenwidth()*0.25),
                             height=(self.winfo_screenheight()*0.25),
                             master=self, borderwidth=1, bg=StyleTheme.background)
        # Title
        self.title_label = Label(panel_config,
                                 text="Search For Windows Events",
                                 padx=padding, pady=padding)
        self.title_label.config(font=font_m,
                                bg=StyleTheme.background,
                                fg=StyleTheme.text_color)
        self.title_label.grid(row=0, column=0, rowspan=2, padx=padding, pady=padding)
        # Log
        self.log_label = Label(panel_config, text="Log to Monitor: ")
        self.log_label.config(font=font_s,
                              bg=StyleTheme.background,
                              fg=StyleTheme.text_color)
        self.log_label.grid(row=2, column=0, rowspan=1, padx=padding, pady=padding)
        choices = ["Security", "Application", "System", "Setup"]
        self.default_selection = StringVar(panel_config)
        self.default_selection.set(choices[0])
        self.logCombo = OptionMenu(panel_config, self.default_selection,
                                   *choices)
        self.logCombo.grid(row=2, column=1, rowspan=1, padx=padding, pady=padding)
        # Log ID
        self.id_label = Label(master=panel_config, text="The ID to monitor: ")
        self.id_label.grid(row=3, column=0, padx=padding, pady=padding)
        self.id_label.config(font=font_s,
                             bg=StyleTheme.background,
                             fg=StyleTheme.text_color)
        self.id = StringVar(panel_config)
        self.log_id_field = Entry(master=panel_config, width=5, textvariable=self.id,
                                  command=None).grid(row=3, column=1)
        # Entries to display
        self.log_id_label = Label(master=panel_config,
                                  text="How many entries would you like displayed:"
                                  "\nif all check all ")
        self.log_id_label.config(font=font_s,
                                 bg=StyleTheme.background,
                                 fg=StyleTheme.text_color)
        self.log_id_label.grid(row=4, column=0, padx=padding, pady=padding)

        self.amount_to_display = StringVar(panel_config)
        self.log_id_field = Entry(master=panel_config, width=5, textvariable=self.amount_to_display,
                                  command=None).grid(row=4, column=1)
        self.isAll = IntVar(panel_config)
        self.display_checkbutton = Checkbutton(master=panel_config, text="All",
                                               variable=self.isAll).grid(row=4, column=2)
        # display oldest logs first
        self.log_age_label = Label(master=panel_config,
                                   text="Display Oldest Logs first:")
        self.log_age_label.grid(row=5, column=0, padx=padding, pady=padding)
        self.log_age_label.config(font=font_s,
                                  bg=StyleTheme.background,
                                  fg=StyleTheme.text_color)
        # self.amount_to_display = StringVar(panel_config)
        self.isOld = IntVar(panel_config)
        self.age_check_button = Checkbutton(master=panel_config,
                                            variable=self.isOld).grid(row=5, column=1)
        # Periodic Check
        self.periodic_label = Label(master=panel_config,
                                    text="Enter how frequently you want to check:")
        self.periodic_label.grid(row=6, column=0, padx=padding, pady=padding)
        self.periodic_label.config(font=font_s,
                                   bg=StyleTheme.background,
                                   fg=StyleTheme.text_color)
        self.freq = StringVar(panel_config)
        self.periodic_field = Entry(master=panel_config, width=5, textvariable=self.freq,
                                    command=None).grid(row=6, column=1)
        # Action Buttons
        self.submit_button = Button(panel_config, text="Submit", bd=0,
                                    pady=padding, padx=padding, command=self.start)
        self.submit_button.grid(row=7, column=1)
        self.submit_button.config(width=10, height=1, background="#000")
        self.clear_button = Button(panel_config, text="Clear", bd=0, pady=padding, padx=padding)
        self.clear_button.grid(row=7, column=2)
        panel_config.pack(fill="both", expand=True)

    def query_events(self):
        """
            Queries the events
            :return: None
        """
        log_name = self.default_selection.get()
        log_id = self.id.get()
        number_of_events = self.amount_to_display.get()
        oldest = 'Y'
        duration = int(self.freq.get())  # In hours
        if self.isAll.get() == 1:
            number_of_events = "all"
        if self.isOld.get() == 0:
            oldest = 'N'
        if log_id != "" and log_name is not None and number_of_events != "" and duration != "":
            delay = int(self.freq.get()) * 6
            ev_entity = None
            ticker =  threading.Event()
            event_entities = EventEntityManager.get_event_entities()
            while not ticker.wait(delay):
                # This thread will repeat itself
                # TODO Admin keeps popping up
                ev_entity = self.test(log_name, log_id, number_of_events, oldest)
                # TODO Create function that will add in new items
                event_entities[ev_entity.id].append([ticker, [ev_entity]])
                print("yo")

    def test(self, log_name, log_id, number_of_events, oldest):
        query_object = ev.query_event_viewer(log_name, log_id, number_of_events, oldest)
        if query_object is not None:
            ev_entity = EventEntity(query_object)
            print(ev_entity)
            return ev_entity


    def start(self):
        # Generates a thread when submitted
        _thread.start_new_thread(self.query_events, ())


if __name__ == "__main__":
    EventViewerDisplay()