import sys,os,re,socket,binascii,time,json,random,threading,queue,pprint,urllib.parse,smtplib,telnetlib,os.path,hashlib,string,urllib.request,glob,sqlite3,urllib,argparse,marshal,base64,colorama,requests
from colorama import *
from random import choice
from colorama import Fore,Back,init
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import system
from colorama import Fore, Back, Style
import queue
from time import strftime
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.parse import urljoin
colorama.init()


# Now regular ANSI codes should work, even in Windows
CLEAR_SCREEN = '\033[2J'
RED = '\033[31m'   # mode 31 = red forground
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
        colors = [36, 32, 34, 35, 31, 37  ]

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
        for N, line in enumerate(x.split("\n")):
            sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
            time.sleep(0.05)
logo()


def scan(empas):
	sabi = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+:[a-zA-Z0-9._-]+')
	empas = sabi.findall(cfile.read())
	
	valid = len(empas)
	for i in range(valid):
		open(input_save,'a').write("\n")
		open(input_save,'a').write(str(cfile[i]))
		
    print(r"Keur Nga-PROSES >" + GREEN + str(empas) + RED + str(i) )
    open(input_save,'a').write(str(empas) + str(i) + '\n')

nam = input('Abuskeun Nomer Janda na  :')
input_save = input(tai+'[!] Nama Jandanya .txt : ')
with open(nam) as f:
    for empas in f:
        scan(empas)
