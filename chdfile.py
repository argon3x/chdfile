#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- decoding: utf-8 -*-
from sys import stdout, exit as status_exit
from os import path, listdir
import argparse
import signal
import hashlib
import io

__version__='2.0.1'

# Colors
green='\033[01;32m'
blue='\033[01;34m'
red='\033[01;31m'
end='\033[00m'

def interrupt_handler(signum, frame):
    """signal for process canceled"""
    status_exit(1)

def error_handler(type_error):
    """signal for process terminated"""
    stdout.write(f'[{red}ERROR{end}] {type_error}\n')
    status_exit(1)


def get_hash(fpath):
    """Get the hash of all file and filter out duplicates"""
    with open(fpath, 'rb') as f:
        bytes_io = io.BytesIO(f.read())

        md5_hash = hashlib.md5()
        md5_hash.update(bytes_io.read())
        md5sum = md5_hash.hexdigest()

    return md5sum


def filter_data(dpath):
    """filter duplicates files using hash"""
    # Removes the last character if it is a /
    directory = dpath.rstrip('/')
    # stores unique hashes (list hashes)
    lhash = set()
    # counter
    count = 0

    print(f'{green}[+]{end} getting file hashes...')

    for file in listdir(directory):
        fpath = directory + '/' + file
        if not path.isdir(fpath):
            fhash = get_hash(fpath)

            if fhash not in lhash:
                lhash.add(fhash)
            else:
                print(f'{blue}[{red}duplicate file{blue}]{end}', fpath)
                count+=1

    print(f'\n {blue}[{green}{count}{blue}]{end} duplicates files\n')


if __name__ == '__main__':
    # Call the signal
    signal.signal(signal.SIGINT, interrupt_handler)
    signal.signal(signal.SIGTERM, error_handler)

    # Set arguments
    parser = argparse.ArgumentParser(prog='chdfile',
                                      description='check that files are not duplicates, '
                                      'gets the hash of eatch file checking for duplicates.')
    parser.add_argument('-d', type=str, required=True, metavar='[directory path]',
                        help='select a directory with files.')

    parser.add_argument('-v', action='version', version=f'%(prog)s {__version__}',
                        help='script version.')

    args = parser.parse_args()

    # Check the integrity of the directory and that it contains files
    print(f'{green}[+]{end} checking directory...')

    if path.isdir(args.d) and listdir(args.d):
        filter_data(args.d)
    else:
        error_handler('the directory does not exist or is emtpy')
