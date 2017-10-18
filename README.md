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
file inside that data folder.
```
> tvc init <path_to_remote_data_folder>
```

├── data
│   ├── .tvc
│       ├── config              # configuration file
│       ├── local_log.csv       # log of local data files and md5 hashes
│       ├── remote_log.csv      # log of remote data files and md5 hashes


