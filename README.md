# Convert WS ONE Windows Logs for LNAV

This is a simple script to convert output from gathering logs using Workspace ONE to a format that can be read by [lnav](http://lnav.org/).  
It uses the [python-evtx](https://pypi.org/project/python-evtx/) library as the converter.

Normally when you gather logs from a Windows device using Workspace ONE, you get a log bundle
that contains the Workspace ONE Agent Logs, Install logs, etc.  It can also contain the Windows Event Logs.

If, during deployment, the  time changes on your computer, the json logs may become disordered.  This will
lead to LNAV not being able to parse the logs.  Step one in this script is to sort the json logs by timestamp.

Step 2 is to add a timestamp to the Installerlog files which have a time stamp but no date.

Step 3 is to take any Windows Event Logs and convert them to a json format in a similar style to the
standard Workspace ONE logs.   This is done using the python-evtx library.

## Installation
```bash
    pip install python-evtx pandas xmltodict
    
    # OR to use the requirements.txt file
    pip install -r requirements.txt
```

You just have to pass a folder name to the script and it will convert all the 
files in that folder as specified above.

Normally, when you get a log bundle from Workspace ONE, you will have a zip file named like
this System_{date}.zip.  Once you unzip the file, the folder tree will look like this:

>System_{date}
>Agents
  * > Application Deployment Agent
    * `AirWatchMDM-InstallCA-x64-22.6.0.15-{date}.log`
    * `AirWatchMDM-x64-22.6.0.15-{date}.log`
    * `DeployCmdExit.log`
    * `RegistryExport.txt`
    * `VMware.Hub.SfdAgent.DeployCmd-{date}.log`
    * `VMware.Hub.SfdAgent.DeployCmd.nondeploy-{date}.log`
  * > CbLauncher
    * `CbLauncher.log`
  * > DEEM Telemetry Agent
    * `vmwetlm-info-{date}-112340.txt`
    * `vmwetlm-info-{date}-123656.txt`
  * > Factory Provisioning Package
    * `PpkgInstallerLog.txt`
  * > Provisioning Agent
  * > Remote Management Client
  * > Workspace ONE Intelligent Hub
    * `3a392e31-6cbb-48a7-9556-d52c4ac4ebc5-Configure.log`
    * `AW.ProtectionAgent.PowershellExecutor64-{date}.log`
    * `AW.ProtectionAgent.PowershellExecutor86-{date}.log`
    * `AWACMClient-{date}.log`
    * `AWProcessCommands-{date}.log`
    * `Baseline-{date}.log`
    * `DSM-20230321.log`
    * `DeemInstall_{date}_112329.log`
    * `DeemInstall_{date}_112329_001_vmwosquery.msi.log`
    * `DeemInstall_{date}_112329_002_vmwetlm_hub.msi.log`
    * `DeviceEnrollment-{date}.log`
    * `HubStatus.html`
    * `InstallerLog_{date}_111940.log`
    * `Logging.Default.json`
    * `MasterSecedit-Export.log`
    * `MasterSecedit-Rollback.log`
    * `NativeEnrollment-20230321.log`
    * `RegistryExport.txt`
    * `TaskScheduler-{date}.log`
    * `VMware.Hub.Win32Agent.AppXInstaller-{date}.log`
    * `VMwareHubHealthMonitoring-{date}.log`
    * `Workflow-{date}.log`
    * > userlogs_dlat9533
      * `AwWindowsIpc-{date}.log`
      * `CommunicationService{date}.log`
      * `HubStatus.html`
      * `IntelligentHubLogs{date}.log`
* Device
  * PCRefresh
  * > Windows
    * `Application_EventLogs.evtx`
    * > Environment
      * `Processes.txt`
      * `Services.txt`
    * `Microsoft-Windows-DeviceManagement-Enterprise-Diagnostics-Provider_Admin_EventLogs.evtx`
    * `RegistryExport.txt`
    * `System_EventLogs.evtx`

By default, new files will be created in the following way:
* The original json files will be renamed to filename_sorted.log
* The original InstallerLog files will be renamed to filename_new.log
* The original Windows Event Logs will be renamed to filename.log

jsonLog format is a format that lnav can read.  It is a log file where each line is a json object.  
The json object has a timestamp and several fields.

## Usage
```bash
    python ConvertWSOneLogs.py <Folder Name>
    
    # then to use lnav on those files
    lnav -r foldername
```

To use this script, you need to have python installed.  You can get it from [here](https://www.python.org/downloads/).

To use the logs in lnav, you need to have lnav installed.  You can get it from [here](http://lnav.org/downloads.html).

I have included the lnav configuration file that I use to view the logs along with teh main one I use to parse Workspace ONE UEM Logs.
Once you have lnav installed, you can install the parser like this:
```bash
    lnav -i AllWindowsParsers.json
```

## License
This project is licensed under the MIT License by Leon Letto - see the [LICENSE](LICENSE) file for details

## Acknowledgments
* [python-evtx](https://pypi.org/project/python-evtx/)
* [lnav](http://lnav.org/)

## Support
This is an open source project and is not officially supported by VMware.  If you have any issues, please log
them in the issues tab and I will try to address them as soon as I can.

