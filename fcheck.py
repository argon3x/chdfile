#!/bin/python3
# coding: utf-8
from time import sleep
import signal, os, sys, argparse, hashlib

### By: Argon3x
### Supported: Debian Based Systems and Termux
### Version: 1.0

# Colors
green = "\033[01;32m"; blue = "\033[01;34m"; red = "\033[01;31m"
purple = "\033[01;35m"; yellow = "\033[01;33m"; end = "\033[00m"

# Context Box
okey = f"{blue}[{green}+{blue}]{end}"
error = f"{blue}[{red}-{blue}]{end}"
passed = f"{blue}[{purple}*{blue}]{end}"
warning = f"{red}[!]{end}"

# Function Error and Interrupt
def interrupt_handler(signum, frame):
    sys.stdout.write(f"\n {warning} {red}Process Canceled{end} {warning}\n\n")
    sys.exit(1)

def error_handler(type_error):
    sys.stdout.write(f"\n{warning} {blue}script error: {red}{type_error}{end}\n\n")
    sys.exit(1)

# Call the signals
signal.signal(signal.SIGINT, interrupt_handler)
signal.signal(signal.SIGTERM, error_handler)


def main(path_directory, list_files):
    sleep(1)
    path_directory = path_directory.rstrip('/') # removes the last character if it is a (/)
    hashes = {} # Empty dictionary that will contain all the hashes of the files
   
    # Get all file hashes 
    print(f"{okey} {yellow}getting the hashes of the files and checking them{end}...........\n")

    for file in list_files:
        path_file = path_directory + '/' + file
        
        with open(path_file, 'rb') as f:
            content = f.read()
            hash_sha1 = hashlib.sha1(content).hexdigest()

        if hash_sha1 in hashes:
            print(f"{warning} The {purple}{file}{end} file is duplicate, with{purple}", hashes[hash_sha1], f"{end}")

        hashes[hash_sha1] = file

    sleep(1)
    if len(hashes) == len(list_files):
        print(f"{okey} {green}No duplicate files found ...!\n")
    else:
        print(f"\n{error} {red}Found {purple}{(len(list_files)-len(hashes))} {red}duplicate files{end}\n")


if __name__ == '__main__':
    os.system('clear') # Clean the terminal

    # Configure the arguments
    parser = argparse.ArgumentParser(description="Check it if exists files duplicate.")
    parser.add_argument('-d', '--directory', required=True, type=str, metavar='', help="Select a specific directory")
    args = parser.parse_args()
    path_directory = args.directory
    
    # Check if the directory exists
    print(f"{okey} {yellow}Checking if directory exists{end}...........", end="")
    if os.path.isdir(path_directory):
        print(f"{green} ok {end}")
    else:
        print(f"{red} failed {end}")
        error_handler(type_error=f"{path_directory} Directory Not Exists")

    # Check if there are files inside the directory
    print(f"{okey} {yellow}Checking directory content{end}...........", end="")
    list_files = [] # empty file list
    i = 0

    with os.scandir(path_directory) as files:
        for file in files:
            if file.is_file():
                list_files.append(file.name)
                i+=1
    
    if i >= 2: # Check that the directory contains more than two files
        print(f"{green} ok {end}")
    else:
        print(f"{red} failed {end}")
        error_handler(f"The {path_directory} does not contain more that 2 files.")

    # Call the main function 
    main(path_directory, list_files)

