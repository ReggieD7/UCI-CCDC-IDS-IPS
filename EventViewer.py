import subprocess
import time

def query_event_viewer(log_name, log_id, number_of_events, oldest):
    if oldest == 'Y':
        if number_of_events.isdigit():
            return subprocess.check_output(['Powershell.exe', 
                                    f"Get-WinEvent \
                                    -FilterHashtable @{{LogName= '{log_name}' ; id={log_id}}} -MaxEvents {number_of_events} -oldest -Credential Administrator | format-list"])
                                    
    else:
        if number_of_events == 'all':
            return subprocess.check_output(['Powershell.exe', 
                                    f"Get-WinEvent \
                                    -FilterHashtable @{{LogName= '{log_name}' ; id={log_id}}} -Credential Administrator | format-list"])

def get_inputs():
    log_name = input('What type of log would you like to monitor? ')
    log_id = input('Which id(s) would you like to monitor? ')
    number_of_events = input('How many entries would you like displayed? If you would like all, please enter "all" ')
    oldest = input('Would you like to display the oldest logs first? [Y/N] ') 
    return log_name, log_id, number_of_events, oldest
    
    
def main():
    duration = int(input('Enter how periodically you would like to check for certain ids'))
    user_inputs = get_inputs()
    info = query_event_viewer(user_inputs[0], user_inputs[1], user_inputs[2], user_inputs[3])
    while True:
        time.sleep(duration)
        print(info.decode('UTF-8'))

if __name__ == "__main__":
    main()
