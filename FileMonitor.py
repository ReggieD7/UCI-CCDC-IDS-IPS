import hashlib
import os, time
import tkinter
from tkinter import filedialog
from datetime import datetime, timezone


def make_checksum(file_path):
    #computes hash using sha256
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
    #checks if original hash is the same as updated one (if file has been altered, it will be different)
    return original_hash.digest() == updated_hash.digest()


def get_meta_data(file_path):
    #gets file size after modification
    after_file_size = os.path.getsize(file_path)

    #gets time of modification in unix time then converts it to local time
    utc_m_time = int(os.path.getmtime(file_path))
    utc_m_time = datetime.fromtimestamp(utc_m_time, timezone.utc)
    local_m_time = utc_m_time.astimezone()
    m_time = local_m_time.strftime("%Y/%m/%d %I:%M:%S %p")

    return after_file_size, m_time


def main():
    root = tkinter.Tk()
    root.withdraw()  # use to hide tkinter window
    chosen_file_to_monitor = filedialog.askopenfilename()

    while True:
        if len(chosen_file_to_monitor) > 0:
            time_check = float(input("Enter how long in hours you would like to check the desired file: "))
            print(f"You chose {chosen_file_to_monitor}")

            #computes first hash and gets original file size
            original_hash = make_checksum(chosen_file_to_monitor)

            file_size_before = os.path.getsize(chosen_file_to_monitor)

            time.sleep(time_check * 3600)

            #computes second hash and checks if it's equal to the first
            updated_hash = make_checksum(chosen_file_to_monitor)

            check_if_hashs_are_equal = check_checksum(original_hash, updated_hash)

            if check_if_hashs_are_equal:
                print('File has not been altered')
            else:
                #prints meta data of altered file
                meta_data = get_meta_data(chosen_file_to_monitor)
                print(f'File: {chosen_file_to_monitor}')
                print(f'File size before: {file_size_before} bytes')
                print(f'File size after: {meta_data[0]} bytes')
                print(f'Date and Time Altered: {meta_data[1]}')

        else:
            pressed_cancel = input('Would you like to exit? [Yes/No] ')
            if pressed_cancel == 'Yes':
                break


if __name__ == "__main__":
    main()

