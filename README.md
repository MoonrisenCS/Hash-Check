# HashCheck
### A command-line integrity checker for files, written in Python.

## About
HashCheck is a personal Python learning project that generates file hashes and verifies file integrity using SHA-256 and MD%. It uses JSON to store hash records and associates unlock keys with those records for verification

The project was created to practise my understanding of Python, whils't integrating modules i haven't used before, that i will need to be familiar with when i go into work. The modules that I familiarised myself with for this project were: File Handling with pathlib, Hashing with hashlib and creating a CMI using argsparce

## Features
- Generate SHA-256 and MD5 File Hashes
- Reads files in chunks when calculating hashes
- Store hash records in JSON
- Verify files against previously stored hashes
- Use command-line sub-commands and arguments

## Requirements
- Python 3

## Usage:
### Generating a hash (sha256 default):
    python hashCheck.py generate example.txt
    
### Selecting an algorithm:
    python hashCheck.py generate example.txt -a "sha256/md5"
    python hashCheck.py generate example.txt --algo "sha256/md5"

### Verifying a file (sha256 default):
    python hashCheck.py verify example.txt FILE_UNLOCK_KEY 
    
### Selecting an algorithm:
    python hashCheck.py verify example.txt FILE_UNLOCK_KEY -a "sha256/md5"
    python hashCheck.py verify example.txt FILE_UNLOCK_KEY --algo "sha256/md5"

## What I Learned:
- File Handling with pathlib
- Hash Generation with hashlib
- Command-line interfaces with argparse

## Project Status
Completed as a personal learning project. further changes may occur as i learn more python, but for the time being, enjoy hashCheck!
