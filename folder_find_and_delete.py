#!/usr/bin/python
import os
import re
import fnmatch
from hurry.filesize import size

def traverse_folders(curr_dir, compiled, volume):
    dirmatchlist = []
    filematchlist = []
    total_space_saved = 0

    # build a list of all 1st level directories, and parse vs regex
    print('Parsing subdirectories located in ' + os.getcwd())
    for subdiriterator in os.listdir(curr_dir):
        for founddir in compiled.finditer(subdiriterator):
            dirmatchlist.append(founddir.string)

    # iterate over directories adding files to a list and track size
    for working_dir in dirmatchlist:
        os.chdir(os.path.join(curr_dir, working_dir))
        for matchfile in os.listdir(os.getcwd()):
            if fnmatch.fnmatch(matchfile, '*.ARW'):
                filematchlist.append(matchfile.__str__())
                # print(os.stat(matchfile).st_size)
                total_space_saved += os.stat(matchfile).st_size

    print('Raw file count on ' + volume + ' hdd for 2018 and month of ' + two_digit_month + ': ' + str(
        len(filematchlist)))
    print('Total space used on ' + volume + ' is: ' + size(total_space_saved))

print('Welcome to the fancy file cleaner. We will first confirm your raw files are backed up,')
print('and then we will confirm your desire to delete local copies of raw files.')
two_digit_month = input("Which two digit month would you like to check from 2018? ")
built_regex = r'2018-' + two_digit_month + r'-\d\d'
# print('regex created to search for: ' + built_regex)

# Check attached backup first to get counts of backed up files meeting criteria
os.chdir('/Volumes/2018 Backup/Pictures/2018')
initial_backup_dir = os.getcwd()
backup_dir_pattern = re.compile(built_regex)
volume_to_scan = "backup"
traverse_folders(initial_backup_dir, backup_dir_pattern, volume_to_scan)

# now run again for local filesystem
os.chdir('/Users/madsen/Pictures/2018')
initial_local_dir = os.getcwd()
local_dir_pattern = re.compile(built_regex)
volume_to_scan = "local"
traverse_folders(initial_local_dir, local_dir_pattern, volume_to_scan)

continue_with_delete = input("Would you like to proceed with local raw file delete? (yes/no): ")

if continue_with_delete == 'yes':
    for doomed_file in filematchlist:
        # add actual code to delete - problem here is tha twe didn't save the file/folder structure
        print('Deleting file ' + doomed_file + ' .... deleted!')
    print('files deleted!')
else:
    print('file deletion ABORTED')
    quit(0)