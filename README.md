## tvc - Temporary Version Control System

This is a temporary data version control system. Current version has only been
tested on Windows 7 and with Python 3.5.3. It requires python, but can be
accessed as a command line utility. It handles the transfer and version control
of data between a local (software version controlled) data folder and a remote
data folder (i.e. on the P drive) that acts as a store for all the data. md5 
hashes of each data file are used to guarantee provenance of local data; hashes
of each data file are created, and a list of these hashes is then tracked by svc
(rather than the data itself)

### Command Options
```
> tvc -h
usage: tvc [-h] {init,pull,add_extension,update_logs} ...

positional arguments:
  {init,pull,add_extension,update_logs}
                        subparsers help
    init                initiate a tvc repository
    pull                synch local data with remote
    add_extension       add file extension to list of tracked file types
    update_logs         update logs and hash associations of data

optional arguments:
  -h, --help            show this help message and exit

```

### Usage Example

In some local data folder, initialise a repository. This should created a .tvc
file inside that data folder. Include, as an argument, the directory path of
the remote data. All subsequent tvc commands should be run inside the data folder.
```
> tvc init <path_to_remote_data_folder>
```

Add a file extension to track, e.g. ".mp4" or ".mat"
```
> tvc add_extension <file_extension>
```

Update the log files to list the hashes and filepaths of the tracked files. 
```
> tvc update_logs
```
It may take some time for the hash function to run over large data files. Doing this
will create two log files in the .tvc folder: 'remote_log.csv' and 'local_log.csv'.
Both simply list the contents of their respective folders. The idea is that the 
log files can be checked in to software version control, so that, if one reverts
back an old version of software, the local log at that version can be used with 
tvc pull to copy the correct files down to the local data folder.

Inspects the local log and pulls everything from the remote data store to the 
local data folder.
```
> tvc pull
```

### Directory Structure

  ├── data  
  │&nbsp;&nbsp;├── some data files  
  │&nbsp;&nbsp;├── .tvc  
  │&nbsp;&nbsp;&nbsp;&nbsp;├── config  
  │&nbsp;&nbsp;&nbsp;&nbsp;├── local_log.csv  
  │&nbsp;&nbsp;&nbsp;&nbsp;├── remote_log.csv  

