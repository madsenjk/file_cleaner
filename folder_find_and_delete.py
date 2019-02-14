#!/usr/bin/python
import os
import re
import fnmatch

print('Welcome to the fancy file cleaner. We will first confirm your raw files are backed up,')
print('and then we will confirm your desire to delete local copies of raw files.')
print('')

two_digit_month = raw_input("Which two digit month would you like to delete from 2018? ")
built_regex = r'2018-' + two_digit_month + r'-\d\d'
print('regex created to search for: ' + built_regex)


# Check attached backup first to get counts of backed up files meeting criteria
# initialize variables for current directory, regex compiled pattern, and result lists
os.chdir('/Volumes/2018 Backup/Pictures/2018')
initial_backup_dir = os.getcwd()
backup_dir_pattern = re.compile(built_regex)
backup_dir_match_list = []
backup_file_match_list = []

# build a list of all 1st level directories, and parse vs regex
print('Parsing subdirectories located in ' + os.getcwd())
for backup_sub_dir_iterator in os.listdir(initial_backup_dir):
    for backup_found_dir in backup_dir_pattern.finditer(backup_sub_dir_iterator):
        backup_dir_match_list.append(backup_found_dir.string)

# iterate over list of directories and add raw files to a list
for backup_working_dir in backup_dir_match_list:
    os.chdir(os.path.join(initial_backup_dir, backup_working_dir))
    for backup_match_file in os.listdir(os.getcwd()):
        if fnmatch.fnmatch(backup_match_file, '*.ARW'):
            backup_file_match_list.append(backup_match_file.__str__())

# show count of located files in local hdd
print('Raw file count on backup hdd for 2018 and month of ' + two_digit_month + ': ' + str(len(backup_file_match_list)))

# now run again for local filesystem - optimize this all into one function :)

# now - init all variables for local (current directory, regex compiled pattern, and result lists)
os.chdir('/Users/madsen/Pictures/2018')
initial_dir = os.getcwd()
dirpattern = re.compile(built_regex)
dirmatchlist = []
filematchlist = []

# build a list of all 1st level directories, and parse vs regex
print('Parsing subdirectories located in ' + os.getcwd())
for subdiriterator in os.listdir(initial_dir):
    for founddir in dirpattern.finditer(subdiriterator):
        dirmatchlist.append(founddir.string)

# iterate over list of directories and add raw files to a list
for working_dir in dirmatchlist:
    os.chdir(os.path.join(initial_dir, working_dir ))
    for matchfile in os.listdir(os.getcwd()):
        if fnmatch.fnmatch(matchfile, '*.ARW'):
            filematchlist.append(matchfile.__str__())

# show count of located files in local hdd
print('Raw file count on local hdd for 2018 and month of ' + two_digit_month + ': ' + str(len(filematchlist)))

continue_with_delete = raw_input("Would you like to proceed with local raw file delete? (yes/no): ")

if continue_with_delete == 'yes':
    for doomed_file in filematchlist:
        # add actual code to delete - problem here is tha twe didn't save the file/folder structure
        print('Deleting file ' + doomed_file + ' .... deleted!')
    print('files deleted!')
else:
    print('file deletion ABORTED')
    quit(0)
