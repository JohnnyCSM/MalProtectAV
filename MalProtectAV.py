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

# List of most commonly used for malicious code injection.
target_files_ext = ('.py', '.exe', '.doc', '.docx', '.docm', '.xlsm', '.hta', '.html',
                '.htm', '.js', '.jar', '.vbs', '.vb', 'pdf')

thread_process = '-SCAN-'

fatrat_generated_files = [
    'TheFatRat_Files/April_Invoice.exe',
    'TheFatRat_Files/Bank_Statement.exe',
    'TheFatRat_Files/Payroll20-04.exe',
]


def scanner(window):
    window.write_event_value('-SCAN-', ('Starting Scan.', values["dir_to_scan"]))
    scan_target_dir = values["dir_to_scan"]
    with open('scan_results.txt', 'a+') as scan_results, open('to_be_quarantined.txt', 'a+') as quarantine_results:
        for root, dirs, files in os.walk(scan_target_dir):
            for filename in files:
                if any(filename.endswith(extension) for extension in target_files_ext):
                    targeted_file = os.path.join(root,filename)
                    window.write_event_value('-SCAN-', ('Scanning... ', targeted_file))
                    with open(targeted_file, errors = 'ignore') as read_file:
                        signature_detection = read_file.read()
                        for snippet in malicious_codes:
                            if snippet in signature_detection:
                                scan_results.write(
                                    '[WARNING] ' + targeted_file + ' [MAY CONTAIN MALICIOUS CODE AND SHOULD BE QUARANTINED ] ' + '\n\n')
                                quarantine_results.write(targeted_file + "\n")
                                window.write_event_value('-SCAN-', ('POSSIBLE VIRUS FOUND: ', targeted_file))
                        if targeted_file.endswith('.exe'):
                            with open(targeted_file, 'rb') as exe_binaries:
                                signature_detection_hex = exe_binaries.read()
                                for files in fatrat_generated_files:
                                    with open(files, 'rb') as check_file:
                                        check_bins = check_file.read() 
                                        if check_bins == signature_detection_hex:
                                            scan_results.write(
                                                '[WARNING] ' + targeted_file + '[MAY BE A TheFatRat GENERATED FILE AND SHOULD BE QUARANTINED.]' + '\n\n')
                                            quarantine_results.write(targeted_file + "\n\n")
                                            window.write_event_value('-SCAN-', (
                                                'POSSIBLE FatRat FILE FOUND: ', targeted_file ))
    window.write_event_value('-SCAN-', 'Scan Complete.' + '\n')


def see_results():
    with open('scan_results.txt',
              'r') as view_results:
        for lines in view_results:
            print(lines)

def quarantine_from_results():
    user_desktop = os.path.expanduser("~/Desktop")
    q_directory = os.path.join(user_desktop, r'Quarantine')
    if not os.path.exists(q_directory):
        os.makedirs(q_directory)
    with open('to_be_quarantined.txt', 'r') as files_to_be_quarantined:
        for line in files_to_be_quarantined:
            try:
                shutil.move(line.strip("\n"), q_directory)
            except:
                continue
    print('Quarantined Files. Check quarantine!' + '\n')


def main():
    global values
    #Create the window
    psg.theme('LightGrey4')
    layout = [[psg.Text('MalProtectAV', font='Any 15', text_color = 'black', background_color = 'white')],
              [psg.Text("Choose folder to scan: ", font='Any 15', text_color = 'black'), 
               psg.FolderBrowse(key = "dir_to_scan")],

              [psg.Multiline(size=(93, 20), key='-ML-', autoscroll=True, reroute_stdout=True, write_only=True,
                                reroute_cprint=True)],
              [psg.B('', image_data=scan_btn, button_color='white', key= 'Start'), 
               psg.Button('', image_data=results_btn, button_color='white', key= 'Results'), 
               psg.Button('', image_data=quarantine_btn, button_color='white', key= 'Quarantine'), 
               psg.Button('', image_data=exit_btn, button_color='white', key= 'Exit')],
              [psg.Text('Scan', pad=(35,0)), psg.Text('Results', pad=(35,0)), 
               psg.Text('Quarantine', pad=(15,0)), psg.Text('Exit', pad=(45,0))]]

    window = psg.Window('MalProtect Antivirus', layout, background_color='white' )

    # Run GUI in a loop
    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED or event == 'Exit':
            break
        if event.startswith('Start'):
            threading.Thread(target=scanner, args=(window,), daemon=False).start()
        if event == thread_process:
            psg.cprint(f'{values[thread_process]}', colors='white on red')
        if event == 'Results':
            see_results()
        if event == 'Quarantine':
            quarantine_from_results()
    window.close()


if __name__ == '__main__':
    main()