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

        # bg="#23272a"
        # Main Pane
        self.pane = tk.PanedWindow(self.root, width=self.width, height=self.height,
                              bg="#002200", bd=2, orient="horizontal")
        self.pane.grid(column=0, row=0)

        # File Menu
        menu_bar = self.createMenu()
        self.root.config(menu=menu_bar)

        # Multi Frames
        filter_frame = LogFrame(master=self.root, width=self.width*0.25, height=self.height*0.25)#self.createFilterLogFrame()
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
        frame = ttk.Frame(self.root, width=self.width * 0.5,
                          height=self.height, relief="sunken")
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

    title_label: Label = None       # The Label for the component

    log_label: Label = None         # The Label for the logs

    logCombo: OptionMenu = None     # The ComboBox dropdown

    id_label: Label = None          # The Label for the id

    log_id_field: Entry = None      # The field where id is entered

    display_checkbutton: Checkbutton = None # CheckButton for stuff

    log_age_label: Label = None     # Label for the item age

    age_check_button: Checkbutton = None    # CheckButton for checks

    periodic_label: Label = None    # Label for the Frequency for checking

    periodic_field: Entry = None    # The field for the amount of hours

    submit_button: Button = None    # The submission button

    clear_button: Button = None     # Clears changes made

    def __init__(self, master=None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.grid()
        self.create_filter_log_frame()

    def create_filter_log_frame(self):
        """
            The frame where the user will be able
            to input their data
        """
        padding = 5

        panel_config = ttk.Frame(width=(self.winfo_screenwidth()*0.25),
                                 height=(self.winfo_screenheight()*0.25),
                                 master=self, borderwidth=1)
        # Title
        self.title_label = Label(panel_config,
                                 text="Search For Windows Events",
                                 padx=padding, pady=padding, bg="green")
        self.title_label.grid(row=0, column=0, rowspan=2, padx=padding, pady=padding)
        # Log
        self.log_label = Label(panel_config, text="Log to Monitor: ")
        self.log_label.grid(row=2, column=0, rowspan=1, padx=padding, pady=padding)
        choices = ["Security", "Application", "System", "Setup"]
        default_selection = StringVar(panel_config)
        default_selection.set(choices[0], )
        self.logCombo = OptionMenu(panel_config, default_selection,
                                   *choices)
        self.logCombo.grid(row=2, column=1, rowspan=1, padx=padding, pady=padding)
        # Log ID
        self.id_label = Label(master=panel_config, text="The ID to monitor: ")\
            .grid(row=3, column=0, padx=padding, pady=padding)
        id = StringVar(panel_config)
        self.log_id_field = Entry(master=panel_config, width=5, textvariable=id,
                                  command=None).grid(row=3, column=1)
        # Entries to display
        self.log_id_label = Label(master=panel_config,
                                  text="How many entries would you like displayed:"
                                  "\nif all check all ")\
            .grid(row=4, column=0, padx=padding, pady=padding)
        amount_to_display = StringVar(panel_config)
        self.log_id_field = Entry(master=panel_config, width=5, textvariable=amount_to_display,
                                  command=None).grid(row=4, column=1)
        isAll = IntVar(panel_config)
        self.display_checkbutton = Checkbutton(master=panel_config, text="All",
                                               variable=isAll).grid(row=4, column=2)
        # display oldest logs first
        self.log_age_label = Label(master=panel_config,
                                   text="Display Oldest Logs first:")\
            .grid(row=5, column=0, padx=padding, pady=padding)
        isOld = IntVar(panel_config)
        self.age_check_button = Checkbutton(master=panel_config,
                                            variable=isOld).grid(row=5, column=1)
        # Periodic Check
        self.periodic_label = Label(master=panel_config,
                                    text="Enter how frequently you want to check:") \
            .grid(row=6, column=0, padx=padding, pady=padding)
        amount_to_display = StringVar(panel_config)
        self.periodic_field = Entry(master=panel_config, width=5, textvariable=amount_to_display,
                                    command=None).grid(row=6, column=1)
        # Action Buttons
        self.submit_button = Button(panel_config, text="Submit", bd=0,
                                    pady=padding, padx=padding, command=None)
        self.submit_button.grid(row=7, column=1)
        self.clear_button = Button(panel_config, text="Clear", bd=0, pady=padding, padx=padding)
        self.clear_button.grid(row=7, column=2)
        panel_config.pack(fill="both", expand=True)

    def query_events(self):
        #log_name =
        pass


if __name__ == "__main__":
    EventViewerDisplay()