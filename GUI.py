'''
A signature detection tool that identifies malicious code.
Helps in determining desired functionality of predefined executable files and code.
At scale this application would not identify malicious code using strings, but by way of weights within a trained neural network.
'''

import PySimpleGUI as psg
import os
from malicious_codes_list import malicious_codes
from threading import Thread

# List of most commonly used for malicious code injection.
target_files_ext = ('.py', '.exe', '.doc', '.docx', '.docm', '.xlsm', '.hta', '.html',
                '.htm', '.js', '.jar', '.vbs', '.vb', 'pdf')

#Create the window
layout = [[psg.Text('MalProtectAV', size=(10,2), key = "process_update")],
           [psg.Button('Scan'), psg.Button('Results'), psg.Button('Quarantine'), psg.Button('Custom Scan'), psg.FileBrowse(), psg.Button('Exit')]]

window = psg.Window('MalProtect Antivirus', layout, margins=(150, 150))
process_text = window['process_update']

# function call
def scan_target():
    with open('scan_results.txt', 'a+') as scan_results:
        for root, dirs, files in os.walk('/'):
            for filename in files:
                if any(filename.endswith(extension) for extension in target_files_ext):
                    targeted_file = os.path.join(root,filename)
                    with open(targeted_file, errors = 'ignore') as read_file:
                        signature_detection = read_file.read()
                        for snippet in malicious_codes:
                            if snippet in signature_detection:
                                scan_results.write('[WARNING] ' + targeted_file + '[May be malicious] ' + '\n\n')

if __name__ == "__main__":
    thread = Thread(target = scan_target)
    thread.start()
    thread.join()

# Run GUI in a loop
while True:
    event, values = window.read()
    if event == psg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Custom Scan':
        print('hello')
   # if event == 'Quarantine':

    #if event == 'Results':