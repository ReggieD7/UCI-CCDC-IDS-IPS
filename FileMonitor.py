import hashlib
import os, time
import tkinter 
from tkinter import filedialog
from datetime import datetime, timezone


def make_checksum(file_path):
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    
    the_hash = hashlib.sha256()
    
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            the_hash.update(data)
            
    return the_hash

def check_checksum(original_hash, updated_hash):
    return original_hash.digest() == updated_hash.digest()

def get_meta_data(file_path):
    after_file_size = os.path.getsize(file_path)
    
    utc_m_time = int(os.path.getmtime(file_path))
    utc_m_time = datetime.fromtimestamp(utc_m_time, timezone.utc)
    local_m_time = utc_m_time.astimezone()
    m_time = local_m_time.strftime("%Y/%m/%d %I:%M:%S %p")
    
    
    return after_file_size, m_time

def main():
    root = tkinter.Tk()
    root.withdraw() # use to hide tkinter window

    while True:
        chosen_file_to_monitor = filedialog.askopenfilename()
        if len(chosen_file_to_monitor) > 0:
            time_check = float(input("Enter how long in hours you would like to check the desired file: "))
            print(f"You chose {chosen_file_to_monitor}")
            
            original_hash = make_checksum(chosen_file_to_monitor)
            
            time.sleep(time_check*3600)
            
            updated_hash = make_checksum(chosen_file_to_monitor)
            
            check_if_hashs_are_equal = check_checksum(original_hash, updated_hash)
            
            if check_if_hashs_are_equal:
                print('File has not been altered')
            else:
                print(get_meta_data(chosen_file_to_monitor))
        else:
            pressed_cancel = input('Would you like to exit? [Yes/No] ')
            if pressed_cancel == 'Yes':
                break
            
if __name__ == "__main__":
    main()
    

