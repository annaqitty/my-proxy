#import telnetlib
#Python3 Code
#./Annaqitty
import sys
import os
import re
import socket
import binascii
import time
import json
import random
import threading
import queue
import pprint
import urllib.parse
import smtplib
import hashlib
import string
import urllib.request
import glob
import sqlite3
import urllib
import argparse
import marshal
import base64
import requests
from colorama import Fore, Back, Style, init
from random import choice
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import system
from time import strftime
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen

# Initialize colorama
init()

# Now regular ANSI codes should work, even in Windows
CLEAR_SCREEN = '\033[2J'
RED = '\033[31m'   # mode 31 = red foreground
RESET = '\033[0m'  # mode 0  = reset
BLUE  = "\033[34m"
CYAN  = "\033[36m"
GREEN = "\033[32m"
RESET = "\033[0m"
BOLD    = "\033[m"
REVERSE = "\033[m"
tai = Fore.YELLOW

def logo():
    clear = "\x1b[0m"
    colors = [36, 32, 34, 35, 31, 37]

    x = """ 

       ___
     o|* *|o  ╔╦═╦╗╔╦╗╔╦═╦╗
     o|* *|o  ║║╔╣╚╝║║║║║║║
     o|* *|o  ║║╚╣╔╗║╚╝║╩║║
      \===/   ║╚═╩╝╚╩══╩╩╝║
       |||    ╚═══════════╝
       |||  K.E.U.R - C.O.M.B.O.S
       |||    ╔═╦═╦╦═╦╦═╗╔═╦╦══╦══╦╦╗
       |||    ║╩║║║║║║║╩║║╚║╠╗╔╩╗╔╩╗║
    ___|||___ ╚╩╩╩═╩╩═╩╩╝╚═╩╝╚╝ ╚╝ ╚╝
   
      By : AnnaQitty
      Github : github.com/annaqitty    
                                                              
                              """
    for line in x.split("\n"):
        sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
        time.sleep(0.05)
logo()

def scan(empas, input_save):
    sabi = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+:[a-zA-Z0-9._-]+')
    matches = sabi.findall(empas)
    
    with open(input_save, 'a') as f:
        for match in matches:
            f.write(f"{match}\n")

def read_file(filename, encoding):
    try:
        with open(filename, encoding=encoding) as file:
            return file.read()
    except UnicodeDecodeError as e:
        print(f"Error reading {filename} with encoding {encoding}: {e}")
        return None

nam = input('Abuskeun Nomer Janda na  :')
input_save = input(tai + '[!] Nama Jandanya .txt : ')

# Try reading the file with different encodings
encodings = ['utf-8', 'latin-1', 'cp1252']

file_content = None
for encoding in encodings:
    file_content = read_file(nam, encoding)
    if file_content is not None:
        break

if file_content:
    for empas in file_content.splitlines():
        scan(empas, input_save)
else:
    print("Failed to read the file with all attempted encodings.")
