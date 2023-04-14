# Convert Event Logs for LNAV

This is a simple script to convert Windows Event Logs to a format that can be read by [lnav](http://lnav.org/).  
It uses the [python-evtx](https://pypi.org/project/python-evtx/) library as the converter.

## Installation
```bash
    pip install python-evtx
```

You just have to pass a folder name to the script and it will convert all the .evtx 
files in that folder to .log files in jsonLog format.

jsonLog format is a format that lnav can read.  It is a log file where each line is a json object.  
The json object has a timestamp and several fields.

## Usage
```bash
    python ConvertWinEventLogs.py <Folder Name>
```

To use this script, you need to have python installed.  You can get it from [here](https://www.python.org/downloads/).

To use the logs in lnav, you need to have lnav installed.  You can get it from [here](http://lnav.org/downloads.html).

I have included the lnav configuration file that I use to view the logs along with teh main one I use to parse Workspace ONE UEM Logs.
Once you have lnav installed, you can install the parser like this:
```bash
    lnav -i WinEventsLnavFormat.json
    lnav - i WSOneWindowsHubLogFormat.json
```

