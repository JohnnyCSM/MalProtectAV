# MalProtectAV
This project consists of an Antivirus program with a simple and acceptable Graphical User Inteface. This software is signature based only for now that detects non executable malicious files using predefined code snippets from verified vulnerabilities. Small snippets of the code targeting Windows vulnerabilities used to identify the malware were taken from the [Windows Vulnerabilities] (https://www.exploit-db.com/?platform=windows&type=local). 
The tool detects executable files (.exe) as well generated with the help of TheFatRat tool. These (.exe) files are stored in the "TheFatRat_Files" directory as binary files where the script is run. 
The tool is not using.

## Requirements
* **Python** 3.7+
* **PySimpleGUI** package
* **pip** in case if not include by default with the Python binary installers as it should be.

## PySimpleGUI Install
* pip install pysimplegui
* or
* pip3 install pysimplegui
* **upgrading**: `python -m pip install --upgrade --no-cache-dir PySimpleGUI`

## How to Run
For Windows:

1. Clone the repository: `https://github.com/JohnnyCSM/MalProtectAV.git` or download it as `zip`
2. Open `cmd` (command prompt)
3. Locate the file directory and change directory: `cd` `C:\FilePath\MalProtectAV\`
4. Start the application using `python MalProtectAV.py` 
