import subprocess
import time

def builtin_administrator():
    builtin_admin_attributes = ((subprocess.check_output(['Powershell.exe', 'net user Administrator'])).decode('UTF-8'))
    return "Account active               Yes" in builtin_admin_attributes
        

def query_event_viewer(log_name, log_id, number_of_events, oldest):
    if oldest == 'Y':
        if number_of_events.isdigit():
            return subprocess.check_output(['Powershell.exe', 
                                    f"Get-WinEvent \
                                    -FilterHashtable @{{LogName= '{log_name}' ; id=@({log_id})}} -MaxEvents {number_of_events} -oldest -Credential Administrator | format-list"])
        elif number_of_events == 'all':
            return subprocess.check_output(['Powershell.exe', 
                                    f"Get-WinEvent \
                                    -FilterHashtable @{{LogName= '{log_name}' ; id=@({log_id})}} -oldest -Credential Administrator | format-list"])
        else:
            pass
                                    
    else:
        if number_of_events.isdigit():
            return subprocess.check_output(['Powershell.exe', 
                                    f"Get-WinEvent \
                                    -FilterHashtable @{{LogName= '{log_name}' ; id=@({log_id})}} -MaxEvents {number_of_events} -Credential Administrator | format-list"])
        elif number_of_events == 'all':
            return subprocess.check_output(['Powershell.exe', 
                                    f"Get-WinEvent \
                                    -FilterHashtable @{{LogName= '{log_name}' ; id=@({log_id})}} -Credential Administrator | format-list"])
        else:
            pass
            

def get_inputs():
    log_name = input('What type of log would you like to monitor? ')
    log_id = input('Which id(s) would you like to monitor? Enter in format: #### #### #### ')
    log_id = ','.join([f"'{i}'" for i in (log_id).split()])
    oldest = input('Would you like to display the oldest logs first? [Y/N] ')
    number_of_events = input('How many entries would you like displayed? If you would like all, please enter "all" ') 
    return log_name, log_id, number_of_events, oldest
    
def gen(info):    
    for i in (info.decode('UTF-8')).split('\n'):
        if 'TimeCreated' in i:
            yield i.strip('\r')
        elif 'Id' in i:
            yield i.strip('\r')
        elif 'Message' in i:
            yield i.strip('\r')
        elif ('Account Name' in i) and (len(i) > 41) and ('Network' not in i):
            yield i.replace('\r', '')
        elif ('Account Domain' in i) and (len(i) > 41) and ('Network' not in i):
            yield i
        else:
            pass
      
    
def main():
    if builtin_administrator():
        duration = eval(input('Enter how periodically you would like to check for certain ids: '))
        user_inputs = get_inputs()
        info = query_event_viewer(user_inputs[0], user_inputs[1], user_inputs[2], user_inputs[3])
        while True:
            time.sleep(duration)
            parsed_info = gen(info)
            for i in parsed_info:
                print(i)
        
    else:
        print('You will need to enable the built-in Administrator')

    
if __name__ == "__main__":
    main()
