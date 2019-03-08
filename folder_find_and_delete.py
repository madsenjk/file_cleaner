#!/Users/madsen/file_cleaner/bin/python
import os
import re
import fnmatch
from hurry.filesize import size

def traverse_folders(curr_dir, compiled, volume, operation = 'read'):
    dirmatchlist = []
    filematchlist = []
    total_space_saved = 0

    # build a list of all 1st level directories, and parse vs regex
    print('Parsing subdirectories located in ' + os.getcwd())
    for subdiriterator in os.listdir(curr_dir):
        for founddir in compiled.finditer(subdiriterator):
            dirmatchlist.append(founddir.string)

    # iterate over directories adding files to a list and track size, branches for read vs purge
    for working_dir in dirmatchlist:
        os.chdir(os.path.join(curr_dir, working_dir))
        if operation == 'read':
            for matchfile in os.listdir(os.getcwd()):
                if fnmatch.fnmatch(matchfile, '*.ARW') or fnmatch.fnmatch(matchfile, '*.CR2'):
                    # or fnmatch.fnmatch(matchfile, '*.MP4'):
                    filematchlist.append(matchfile.__str__())
                    total_space_saved += os.stat(matchfile).st_size
        elif operation == 'purge':
            for matchfile in os.listdir(os.getcwd()):
                if fnmatch.fnmatch(matchfile, '*.ARW') or fnmatch.fnmatch(matchfile, '*.CR2'):
                    # or fnmatch.fnmatch(matchfile, '*.MP4'):
                    total_space_saved += os.stat(matchfile).st_size
                    filematchlist.append(matchfile.__str__())
                    # print('Deleting file ' + matchfile.__str__())
                    print('Deleting: ' + (os.path.join(os.getcwd(), matchfile.__str__())))
                    os.remove(os.path.join(os.getcwd(), matchfile.__str__()))
            if working_dir == dirmatchlist[len(dirmatchlist)-1]:
                print(str(len(filematchlist)) + ' files deleted!')
                print(size(total_space_saved) + ' in space freed up!')
                return

    print('Large file count on ' + volume + ' hdd for 2018 and month of '
          + two_digit_month + ': ' + str(len(filematchlist)))
    print('Total space used on ' + volume + ' is: ' + size(total_space_saved))


print('Welcome to the fancy file cleaner. We will first confirm your large files are backed up,')
print('and then we will confirm your desire to delete local copies of those files.')
two_digit_year = input("Which two digit year would you like to check? ")
two_digit_month = input("Which two digit month would you like to check from " + "20" + two_digit_year + "? ")
built_regex = r'20' + two_digit_year + '-' + two_digit_month + r'-\d\d'
skip_backup = False

# Check attached backup first to get counts of backed up files meeting criteria
try:
    os.chdir('/Volumes/2018 Backup/Pictures/20' + two_digit_year)
except FileNotFoundError:
    print('Backup volume not found. Skipping backup verification')
    skip_backup = True
if skip_backup == False:
    initial_backup_dir = os.getcwd()
    backup_dir_pattern = re.compile(built_regex)
    volume_to_scan = "backup"
    traverse_folders(initial_backup_dir, backup_dir_pattern, volume_to_scan)

# Now run again for local filesystem
os.chdir('/Users/madsen/Pictures/20' + two_digit_year)
initial_local_dir = os.getcwd()
local_dir_pattern = re.compile(built_regex)
volume_to_scan = "local"
traverse_folders(initial_local_dir, local_dir_pattern, volume_to_scan)

# Lastly, check for and run delete traversal
continue_with_delete = input("Would you like to proceed with local large file delete? (yes/no): ")
if continue_with_delete == 'yes':
    os.chdir('/Users/madsen/Pictures/20' + two_digit_year)
    directory_to_clean = os.getcwd()
    local_dir_pattern = re.compile(built_regex)
    volume_to_scan = "local"
    traverse_folders(directory_to_clean, local_dir_pattern, volume_to_scan, 'purge')
    quit()
else:
    print('file delete ABORTED')
    quit(0)