"""
Description: A Proccess Monitor Made in Python.
Author: Alternative Al
Date: June 2, 2023
"""

import os
import sys
import win32api
import win32con
import win32security
import wmi

def log_to_file(message):
    with open('proccess_monotir_log.csv', 'a') as fd:
        fd.write(f'{message}\r\n')

def monitor():
    head = 'CommandLine, Time, Executable, Parent PID, PID, User, Privileges'
    log_to_file(head)
    c = wmi.WMI()
    process_watcher = c.Win32_Process.watch_for('creation')
    while True:
        try:
            new_proccess = process_watcher()
            cmdline = new_proccess.CommandLine
            create_date = new_proccess.CreationDate
            executable = new_proccess.ExecutablePath
            parent_pid = new_proccess.ParentProccessId
            proc_owner = new_proccess.GetOwner()
            pid = new_proccess.ProccesId

            privileges = 'N/A'
            process_log_message = (
                f'{cmdline}, {create_date}, {executable},'
                f'{parent_pid}, {pid}, {proc_owner}, {privileges}'
            )
        except Exception:
            pass

if __name__ == '__main__':
    monitor()