p = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe', 
                    'Get-EventLog -logname Security -Newest 5'], 
                      stdin=subprocess.PIPE)





import subprocess, sys

def main():
    while True:
        #inputs
        type_of_log = input("What type of log do you want to display (Security, Application, System)? Enter as 'Security' --with single quote marks: ")
        event_ID = input("Which event ID(s) do you want to display? If multiple, enter in format ####, ####, ####: ")
        log_properties = input("What log properties do you want to display (Message, InstanceID, TimeCreated, LevelDisplayName, etc.). If multiple, enter in format TimeCreated, InstanceId, Message: ")
        newest = input("Do you want to display the newest logs or oldest logs first? Enter either newest or oldest: ")
        number_of_logs = input("How many logs do you want to display. Enter a number or all: ")

        #main
        if newest == "newest":
            if number_of_logs == "all":
                event_log = subprocess.Popen(['powershell.exe', 'Get-WinEvent -FilterHashTable @{LogName = ', type_of_log,';ID =', event_ID, '} | Select-Object -Property', log_properties],
                    stdout = sys.stdout)
                event_log.communicate()
            else:
                event_log = subprocess.Popen(['powershell.exe', 'Get-WinEvent -FilterHashTable @{LogName = ', type_of_log, ';ID =', event_ID, '} -MaxEvents', number_of_logs, '| Select-Object -Property', log_properties],
                    stdout=sys.stdout)
                event_log.communicate()
        elif newest == "oldest":
            if number_of_logs == "all":
                event_log = subprocess.Popen(['powershell.exe', 'Get-WinEvent -FilterHashTable @{LogName = ', type_of_log,';ID =', event_ID, '} -Oldest | Select-Object -Property', log_properties],
                    stdout = sys.stdout)
                event_log.communicate()
            else:
                event_log = subprocess.Popen(['powershell.exe', 'Get-WinEvent -FilterHashTable @{LogName = ', type_of_log, ';ID =', event_ID,'} -MaxEvents', number_of_logs, ' -Oldest | Select-Object -Property', log_properties],
                    stdout=sys.stdout)
                event_log.communicate()

main()
---------------------------------------------------------------------------------------------------------------------------------------------------
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
                                    -FilterHashtable @{{LogName= ''{log_name}'' ; id={log_id}}} -Credential Administrator | format-list"])

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
