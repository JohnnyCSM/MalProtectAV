'''
A signature based detection tool that identifies malicious code.
Helps in determining desired functionality of predefined executable files and code.
'''

import PySimpleGUI as psg
import os
from malicious_codes_list import malicious_codes
import shutil
from fatrat_binaries import fatrat

# List of most commonly used for malicious code injection.
target_files_ext = ('.py', '.exe', '.doc', '.docx', '.docm', '.xlsm', '.hta', '.html',
                '.htm', '.js', '.jar', '.vbs', '.vb', 'pdf')

#Create the window
layout = [[psg.Text('MalProtectAV', size=(10,2), key = "process_update")],
          [psg.Text("Choose folder to scan: "), psg.FolderBrowse(key = "dir_to_scan")],
          [psg.Button('Scan'), psg.Button('Results'), psg.Button('Quarantine'), psg.Button('Exit')]]

window = psg.Window('MalProtect Antivirus', layout, margins=(150, 150))
process_text = window['process_update']

def scan_complete():
    process_text.update('Scan complete... Check results.')

def q_complete():
    process_text.update('Quarantine complete.')

# function call
def scan_target():
    process_text.update('Scanning... please wait.')
    scan_target_dir = values["dir_to_scan"]
    with open('scan_results.txt', 'a+') as scan_results, open('to_be_quarantined.txt', 'a+') as quarantine_results:
        for root, dirs, files in os.walk(scan_target_dir):
            for filename in files:
                if any(filename.endswith(extension) for extension in target_files_ext):
                    targeted_file = os.path.join(root,filename)
                    with open(targeted_file, errors = 'ignore') as read_file:
                        signature_detection = read_file.read()
                        for snippet in malicious_codes:
                            if snippet in signature_detection:
                                scan_results.write('[WARNING] ' + targeted_file + ' [May be malicious] ' + '\n\n')
                                quarantine_results.write(targeted_file + "\n")
                        if filename.endswith('.exe'):
                            with open(filename, 'r+b') as exe_binaries:
                                signature_detection_hex = exe_binaries.read()
                                for snippet in fatrat:
                                    if snippet in signature_detection_hex:
                                        scan_results.write(
                                            '[WARNING] ' + targeted_file + '[May be a TheFatRat file and must be quarantined.]' + '\n\n')
                                        quarantine_results.write(targeted_file + "\n")
                                    
    scan_complete()

def quarantine_from_results():
    user_desktop = os.path.expanduser("~/Desktop")
    q_directory = os.path.join(user_desktop, r'Quarantine')
    if not os.path.exists(q_directory):
        os.makedirs(q_directory)
    with open('to_be_quarantined.txt', 'r') as files_to_be_quarantined:
        for line in files_to_be_quarantined:
            try:
                shutil.move(line.strip("\n"), q_directory)
            except FileExistsError:
                continue
    
    q_complete()

# Run GUI in a loop
while True:
    event, values = window.read()
    if event == psg.WIN_CLOSED or event == 'Exit':
        break
    if event == "Scan":
        scan_target()
    elif event == 'Results':
        process_text.update('Opening Results...')
        os.system("notepad.exe scan_results.txt")
    elif event == 'Quarantine':
        process_text.update('Quarantine results...')
        quarantine_from_results()
