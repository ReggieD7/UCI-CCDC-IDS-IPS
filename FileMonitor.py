# Monitors Changes in Files

# Ask For the Directory/Files To monitor

# Read in Files to monitor and compute their Hashes

# Monitor For changes to the file and return data on changes

# Types of changes to monitor
# name changes, deletion, creation, and modification

# Must know who modified and when it occurred also the file size change

# Time to check should be periodic and user should decide


from enum import Enum
from sched import *
from fileMonitorEntity import *
from collections import defaultdict
from uuid import *


class Monitor(Enum):
    CREATION = 1
    DELETION = 2
    CHANGES = 3
    MODIFICATIONS = 4


class Priority(Enum):
    CRITICAL = 2
    NONCRITICAL = 1


class FileMonitor:


    def initialize(self):
        pass

    def __init__(self):
        self.monitored_files = defaultdict(list)
        self.observed_directory = {}
        self.schedule = scheduler();

    def startMonitoring(self, file="", time_period=5,):
        """
        Monitor file specified by the specified amount of time
        :param file: Can be a directory or a specific file
        :param time_period:
        :return:
        """
        # Check if its a directory or a file
        monitor_id = uuid4();
        file_to_monitor = Path(file)
        self.observed_directory[monitor_id] = file_to_monitor
        if file_to_monitor.exists():
            if file_to_monitor.is_file():
                fme = FileMonitorEntity(file_to_monitor)
                self.monitored_files[monitor_id].append(fme)
            elif file_to_monitor.is_dir(): # Recurse through directory and add to map
                for file_item in self.recurse_dir(file_to_monitor):
                    fme = FileMonitorEntity(file_item)
                    self.monitored_files[monitor_id].append(fme)
        # UUID with the event

    def monitor(self, uuid):
        """Will run and identify any changes made to a file"""
        # Check Files under UUID
        #for observed_directory in original_monitored_directory[uuid]:




       # for mfe in monitored_files[uuid]:





    def stopMonitoring(self, file):
        pass

    def recurse_dir(self, file):
        #TODO Big fix does not work
        cache_list = []
        if file.is_file():
            return cache_list.append(file)
        elif file.is_dir():
            for file_item in file.iterdir():
                cache_list += self.recurse_dir(file_item)
        return cache_list


if __name__ == "__main__":
    fm = FileMonitor()
    fm.startMonitoring("D:\Desktop\Test\FuckYou.txt")
