# MalProtectAV
This project consists of an Antivirus program with a simple and acceptable Graphical User Inteface. This software is signature based only for now that detects non executable malicious files using predefined code snippets from verified vulnerabilities. Small snippets of the code targeting Windows vulnerabilities used to identify the malware were taken from the https://www.exploit-db.com/?platform=windows&type=local. 
The tool detects executable files (.exe) as well generated with the help of TheFatRat tool. These (.exe) files are stored in the "TheFatRat_Files" directory as binary files where the script is run. 
The tool is not using.

## Requirements
* **Python** 3.7+
* **PySimpleGUI** package
* **pip** toin case if not include by default with the Python binary installers as it should.

## PySimpleGUI Install
* pip install pysimplegui
  or
* pip3 install pysimplegui

## How to Run
For Windows:

1. Open `cmd`
