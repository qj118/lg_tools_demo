# LG Tools Demo

## Key Issue Check - Command Line

### Script Function

- Check the key issue automatically. 

### How to use it?

- `python keyIssueCheck_Command.py -h` to get help
- `python keyIssueCheck_Command.py -d <sas_address> -u <AD account> -p <password>`, if you don't supply AD or password, the scripts will open Chrome with default configuration
 
### Installation Guide

- Install python 2.7
- Install selenium `pip install -U selenium`
- Download [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) file and add it to system path.

## Key Issue Check - UI

### How to use it?

- `python keyIssueCheck_UI.py`

### Installation Guide

- Install python 3.5
- Install selenium `pip install -U selenium`
- Download [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) file and add it to system path.
- Install PyQt5 `pip install PyQt5`
