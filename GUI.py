'''
A signature detection tool that identifies malicious code.
Helps in determining desired functionality of predefined executable files and code.
At scale this application would not identify malicious code using strings, but by way of weights within a trained neural network.
'''

import PySimpleGUI as psg
import os
import shutil
from malicious_codes_list import malicious_codes

# List of most commonly used for malicious code injection.
target_filees = ('.py', '.exe', '.doc', '.docx', '.docm', '.xlsm', '.hta', '.html',
                '.htm', '.js', '.jar', '.vbs', '.vb', 'pdf')

#Create the window
layout = [[psg.Text('MalProtectAV', size=(10,2), key = "process_update")],
           [psg.Button('Scan'), psg.Button('Results'), psg.Button('Quarantine'), psg.Button('Custom Scan'), psg.FileBrowse(), psg.Button('Exit')]]

window = psg.Window('MalProtect Antivirus', layout, margins=(150, 150))
process_text = window['process_update']

#def scan_target():
#def scan_complete():

# Run GUI in a loop
while True:
    event, values = window.read()
    if event == psg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Custom Scan':
        print('hello')
   # if event == 'Quarantine':

    #if event == 'Results':