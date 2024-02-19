**Folder Synchronization Script**

This Python script implements a folder synchronization utility. 

Its primary functions are:

Synchronization from Source to Replica: Maintains an updated replica of a source folder, including creating new files/directories, deleting removed items, and overwriting modified files.

Monitoring & Logging: Tracks and logs changes within the synchronized folders.

Periodic Execution: Allows defining a synchronization interval.


**How it Works**

The script compares the contents (files and directories) of the source and replica folders.

Detects the following changes:

  - New Items: Files or directories present in the source but not in the replica are copied over.
  
  - Deleted Items: Files or directories present in the replica but not in the source are deleted.
  
  - Modified Items: Files with differing MD5 hashes in the source and replica are overwritten in the replica.
  
Logs synchronization actions to a specified log file.

**Usage**

Install Requirements: The script uses the hashlib, shutil, os, argparse, and typing modules. If you don't have them, install them using pip: pip install hashlib shutil os argparse typing

Execute the Script:

python FolderSync.py <source_folder_path> <replica_folder_path> <log_file_path> -i <interval>

**Arguments**

<source_folder_path>: The absolute path to the source folder you want to synchronize.

<replica_folder_path>: The absolute path to the replica folder.

<log_file_path>: The absolute path where the synchronization log should be saved.

-i <interval>: (Optional) The synchronization interval in seconds (defaults to 60 seconds).


Important Notes

The replica folder will be overwritten to mirror the source folder's current state.
Ensure you have permissions to read and write files/directories in both the source and replica folders.
