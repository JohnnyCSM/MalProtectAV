'''
A signature based detection tool that identifies malicious code.
Helps in determining desired functionality of predefined executable files and code.
'''

import threading
import PySimpleGUI as psg
import os
from malicious_codes_list import malicious_codes
import shutil
from btn_images import scan_btn, results_btn, quarantine_btn, exit_btn

# Tool targets a list of executable files to check for malicious code
target_files_ext = ('.py', '.exe', '.doc', '.docx', '.docm', '.xlsm', '.hta', '.html',
                '.htm', '.js', '.jar', '.vbs', '.vb', 'pdf')

# Thread will only process something as -SCAN-
thread_process = '-SCAN-'

# The location of TheFatRat generated files within the tool
fatrat_generated_files = [
    'TheFatRat_Files/April_Invoice.exe',
    'TheFatRat_Files/Bank_Statement.exe',
    'TheFatRat_Files/Payroll20-04.exe',
]


def scanner(window):
    window.write_event_value('-SCAN-', ('Starting Scan.', values["dir_to_scan"])) # write process to screen
    scan_target_dir = values["dir_to_scan"] # scan target
    with open('scan_results.txt', 'a+') as scan_results, open('to_be_quarantined.txt',
                                                             'a+') as quarantine_results: # create a results file (.txt) and use it
        for root, dirs, files in os.walk(scan_target_dir): # initialize os.walk as loop
            for filename in files: # loop through files
                if any(filename.endswith(extension) for extension in 
                       target_files_ext): # identify file types from the target_files_ext list
                    targeted_file = os.path.join(root,filename) #store file iteration as variable
                    window.write_event_value('-SCAN-', ('Scanning... ', targeted_file)) # write process to the screen
                    with open(targeted_file, errors = 'ignore') as read_file: # open the file
                        signature_detection = read_file.read() # read the file
                        for snippet in malicious_codes: # loop through malicious code snippets 
                            if snippet in signature_detection: # identify snippet in file and write to results
                                scan_results.write(
                                    '[WARNING] ' + targeted_file + ' [MAY CONTAIN MALICIOUS CODE AND SHOULD BE QUARANTINED ] ' + '\n\n')
                                quarantine_results.write(targeted_file + "\n")
                                window.write_event_value('-SCAN-', ('POSSIBLE VIRUS FOUND: ', targeted_file)) # write process to screen
                        if targeted_file.endswith('.exe'): # find .exe files
                            with open(targeted_file, 'rb') as exe_binaries: # open .exe file as binary
                                signature_detection_hex = exe_binaries.read() # read .exe hex values (binary)
                                for files in fatrat_generated_files: # loop through fatrat generated .exe files stored within the tool
                                    with open(files, 'rb') as check_file: # open each file as part of loop as binary
                                        check_bins = check_file.read() # read file as binary
                                        if check_bins == signature_detection_hex: # identify snippet in file and write to results
                                            scan_results.write(
                                                '[WARNING] ' + targeted_file + '[MAY BE A TheFatRat GENERATED FILE AND SHOULD BE QUARANTINED.]' + '\n\n')
                                            quarantine_results.write(targeted_file + "\n\n")
                                            window.write_event_value('-SCAN-', (
                                                'POSSIBLE FatRat FILE FOUND: ', targeted_file )) # write process to screen
    window.write_event_value('-SCAN-', 'Scan Complete.' + '\n') # write process to screen


def see_results():
    with open('scan_results.txt',
              'r') as view_results: # results are stored in .txt file (at scale this would be a database)
        for lines in view_results: # loop through file paths in .txt
            print(lines) # display results 

def quarantine_from_results():
    user_desktop = os.path.expanduser("~/Desktop") # locate Desktop
    q_directory = os.path.join(user_desktop, r'Quarantine') # quarantine directory variable 
    if not os.path.exists(q_directory):
        os.makedirs(q_directory) # create quarantine directory if it does not already exist (Desktop)
    with open('to_be_quarantined.txt', 
              'r') as files_to_be_quarantined: # files to be quarantined are stored in a .txt file
        for line in files_to_be_quarantined: # loop through file paths in .txt file
            try:
                shutil.move(line.strip("\n"), q_directory) # move file to quarantine
            except: # error handling back for the tool trying to move a file that has already been quarantined
                continue
    print('Quarantined Files. Check quarantine!' + '\n') 


def main():
    global values # global variable to use outside of function
    
    # set theme
    psg.theme('LightGrey4')

    # initiate GUI window elements in a list called 'layout'. 
    layout = [[psg.Text('MalProtectAV', font='Any 15', text_color = 'black', background_color = 'white')],
              [psg.Text("Choose folder to scan: ", font='Any 15', text_color = 'black'), 
               psg.FolderBrowse(key = "dir_to_scan")],

              [psg.Multiline(size=(93, 20), key='-ML-', autoscroll=True, reroute_stdout=True, write_only=True,
                                reroute_cprint=True)],
              [psg.Button('', image_data=scan_btn, button_color='white', key= 'Start'), 
               psg.Button('', image_data=results_btn, button_color='white', key= 'Results'), 
               psg.Button('', image_data=quarantine_btn, button_color='white', key= 'Quarantine'), 
               psg.Button('', image_data=exit_btn, button_color='white', key= 'Exit')],
              [psg.Text('Scan', pad=(35,0)), psg.Text('Results', pad=(35,0)), 
               psg.Text('Quarantine', pad=(15,0)), psg.Text('Exit', pad=(45,0))]]

    window = psg.Window('MalProtect Antivirus', layout, background_color='white' ) # initialize the GUI window

    while True: # GUI event loop (Standard way to launch PySimpleGUI)
        event, values = window.read() # Read events happening in the GUI window
        if event == psg.WIN_CLOSED or event == 'Exit': # Exit
            break
        if event.startswith('Start'): # Start
            threading.Thread(target=scanner, args=(window,), daemon=False).start() # Initiate Threading
        if event == thread_process: # Return Thread values if used
            psg.cprint(f'{values[thread_process]}', colors='white on red')
        if event == 'Results': # Results
            see_results()
        if event == 'Quarantine': # Quarantine
            quarantine_from_results()
    window.close()


if __name__ == '__main__':
    main()