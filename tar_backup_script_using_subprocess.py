# The script uses subprocess to run tar command.
# First it generates backup file name then checks if enough arguments have been provided.
# Then script verifies that files/dirs provided as command line arguments actually exist.
# Then it generate tar command in list format which subprocess.Popen requires.
# And then it runs the command and saves errors and backup log in different files.

## Import Section ##

from os import path
import sys
import subprocess
import time

## Variable Section. ##


backup_destination_directory = "/tmp"
#Prepare backup file name. Add date and time in file name using time.strftime.
backup_file_name = path.join(backup_destination_directory, time.strftime("full_backup_%Y-%m-%d_%H-%M.tar.gz"))            #Use %S for seconds
# sys.argv[0] stores the script name therefore excluded that.
file_argv = sys.argv[1:]
# Open backup file in write mode. Add date and time in log and error file to make separate file for each backup.
backup_log = open(time.strftime("/tmp/backup_%Y-%m-%d_%H-%M.log"), 'w+')
error_log = open(time.strftime("/tmp/backup_%Y-%m-%d_%H-%M.err"), 'w+')

backup_util = "/bin/tar"
zip_backup_file = True
# Initialize backup_argv list. later file/dir argv that exists will be added to this list.
backup_argv = []

## Pre execution checking ##

if len(sys.argv) < 2:

    print(f"""
At least one argument is required.

Usage:

 {sys.argv[0]}   Space separated list of files and/or directories with absolute to backup.
 {sys.argv[0]}   /etc /bin /usr/bin /data/images/adobe
""")
    exit(1)
for item in sys.argv[1:]:
    if not path.exists(item):
        print(f"""
Error: 
 {item} does not exists. Removing it from the list.
""")
    else:
        backup_argv.append(item)            # add all files/dir in the backup_argv which exists.


if zip_backup_file:
    backup_options = "cvf"
else:
    backup_options = "cvzf"

## Prepration of tar command ##

# Backup command contains tar, tar options and backup file name.
backup_command = [backup_util, backup_options, backup_file_name]

# Combine two lists together to make complete tar command in List form whicn subprocess.Popen requires.
backup_list = backup_command + backup_argv

# Run command and save output and errors in backup_output object.
# and later use .communicate() method to separate out errors and output.
backup_output = subprocess.Popen(backup_list, stdout=backup_log, stderr=error_log, universal_newlines=True)
output, errors = backup_output.communicate()

# Close backup and error logs
backup_log.close()
error_log.close()

