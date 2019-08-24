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
