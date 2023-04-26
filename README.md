# WSOneLogConverterForLNAV

A handy tool to convert some incompatible logs into a format compatible with the powerful LNAV log file viewer.  Designed 
for use with Workspace ONE windows Log Bundles.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)

## Introduction

WSOneLogConverterForLNAV is designed to simplify the process of analyzing and troubleshooting Workspace ONE log files. It converts log files into a format that can be easily read and analyzed using the LNAV log file viewer, enabling you to make the most of LNAV's powerful features, such as filtering, search, and real-time updates.

Normally when you gather logs from a Windows device using Workspace ONE, you get a log bundle
that contains the Workspace ONE Agent Logs, Install logs, etc.  It can also contain the Windows Event Logs.

However, if you want to use LNAV to analyze the logs, you need to add support into LNAV and convert the files
which have issues, into a format that LNAV can read.  This script does that.

For Example:  If, during deployment, the  time changes on your computer, the json logs may become disordered.  This will
lead to LNAV not being able to parse the logs.  Step one in this script is to sort the json logs by timestamp.

Step 1 Sorts the json logs by timestamp.

Step 2 is to add a timestamp to the Installerlog files which have a time stamp but no date and is not parsable.

Step 3 is to take any Windows Event Logs and convert them to a json format in a similar style to the
standard Workspace ONE logs.   This is done using the python-evtx library.

## Note

By default, new files will be created in the following way:
* The original json files will be renamed to filename_sorted.log
* The original InstallerLog files will be renamed to filename_new.log
* The original Windows Event Logs will be renamed to filename.log

You can change the python file to change these options.

## Prerequisites

Before using WSOneLogConverterForLNAV, ensure you have the following prerequisites installed:

- Python 3.x
- LNAV log file viewer (available at https://lnav.org/)
- The following Python packages:
  - python-evtx
  - pandas
  - xmltodict

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/leonletto/WSOneLogConverterForLNAV.git
```

2. Change directory to the cloned repository:

```bash
cd WSOneLogConverterForLNAV
```

3. Install the required packages:

```bash
pip install python-evtx pandas xmltodict
# OR to use the requirements.txt file
pip install -r requirements.txt
```

4. Run the WSOneLogConverterForLNAV Python script with the appropriate arguments:

*Replace*`<path_to_log_folder>` *with the path to your Workspace ONE log files which have been unzipped*

```bash
python WSOneLogConverterForLNAV.py
Enter the root directory to search for json files: <path_to_log_folder>
```

5 Launch LNAV and load the converted log files:

```bash
lnav -r <path_to_log_folder>

```

Now you can use LNAV's powerful features to analyze and troubleshoot Workspace ONE log files with ease.

## Contributing

We welcome contributions to the WSOneLogConverterForLNAV project! Please feel free to submit issues, bug reports, and pull requests.

## License

WSOneLogConverterForLNAV is released under the [MIT License](LICENSE).

