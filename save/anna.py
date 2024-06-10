import urllib.request
import threading
import re
import sys
import queue
import time
from urllib.parse import urlparse
import random

# No .pyc files
sys.dont_write_bytecode = True

# Colors
red = "\033[1;31m"
green = "\033[1;32m"
yellow = "\033[1;33m"
orange = "\033[1;33m"
blue = "\033[1;34m"
defcol = "\033[0m"

def error(msg):
    print(red + "[" + yellow + "!" + red + "] - " + defcol + msg)

def action(msg):
    print(red + "[" + green + "+" + red + "] - " + defcol + msg)

def errorExit(msg):
    sys.exit(red + "[" + yellow + "!" + red + "] - " + defcol + "Fatal - " + msg)

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
   |||  K.E.U.R - I.P - A.N.N.A.Q.I.T.T.Y
   |||    ╔═╦═╦╦═╦╦═╗╔═╦╦══╦══╦╦╗
   |||    ║╩║║║║║║║╩║║╚║╠╗╔╩╗╔╩╗║
___|||___ ╚╩╩╩═╩╩═╩╩╝╚═╩╝╚╝ ╚╝ ╚╝
   
  By : AnnaQitty
  Github : github.com/annaqitty    
                                                                
              
              
                          """
    for N, line in enumerate(x.split("\n")):
        sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
        time.sleep(0.05)

def get_orders():
    name = "output_proxy.txt"
    leech_list = "sites.txt"
    return [name, leech_list]

class ScanThread(threading.Thread):
    def run(self):
        while True:
            url = thread_pool.get()
            try:
                if not url.startswith("http://") and not url.startswith("https://"):
                    url = "http://" + url
                if detect_json_format(url):
                    action("URL contains JSON data")
                    # Handle JSON data
                else:
                    action("URL does not contain JSON data")
                    get = urllib.request.urlopen(url)
                    data = get.read().decode('utf-8')
                    domain = urlparse(url).netloc  # Extract domain
                    valid_proxies = re.findall(r'(?:[\d]{1,3}\.){3}[\d]{1,3}:[\d]{2,5}', data)
                    action("%s proxies found on %s" % (len(valid_proxies), domain))
                    for proxy in valid_proxies:
                        proxy_list.write(proxy + "\n")
                    if len(valid_proxies) > 0:
                        good_sites.write(domain + "\n")
            except IOError:
                pass
            finally:
                thread_pool.task_done()

def detect_json_format(url):
    try:
        response = urllib.request.urlopen(url)
        content_type = response.headers.get('Content-Type')
        if content_type and 'application/json' in content_type:
            return True
    except Exception as e:
        print("Error:", e)
    return False

if __name__ == "__main__":
    logo()
    
    if len(sys.argv) < 3:
        errorExit("Usage: python proxies.py <output.txt> <num_threads> [-l yourlist]")

    orders = get_orders()
    try:
        proxy_list = open(orders[0], "a")
        good_sites = open("good_sites.txt", "w")
    except IOError as e:
        errorExit("Could not create/open files: %s" % e)

    try:
        sites = open(orders[1], "r")
    except IOError as e:
        errorExit("Could not open %s: %s" % (orders[1], e))

    # Number of threads
    num_threads = int(sys.argv[2])

    thread_pool = queue.Queue(0)

    for i in range(num_threads):
        thread = ScanThread()
        thread.start()

    try:
        for url in sites:
            url = url.strip()
            thread_pool.put(url)
    except KeyboardInterrupt:
        errorExit("Keyboard interrupt detected. Exiting...")

    while True:
        if thread_pool.empty():
            break
        time.sleep(1)

    thread_pool.join()

    proxy_list.close()
    good_sites.close()

    total_proxies = sum(1 for line in open(orders[0]))

    if total_proxies > 2000:
        print(yellow + "Total proxies found: %s" % total_proxies + defcol)
    else:
        print(orange + "Total proxies found: %s" % total_proxies + defcol)

    action("Done leeching.")

    # Option to remove duplicate proxies
    remove_duplicates = input("Do you want to remove duplicate proxies? (yes/no): ").strip().lower()
    if remove_duplicates == "yes":
        try:
            with open(orders[0], "r") as f:
                lines = f.readlines()
            lines = set(lines)
            with open(orders[0], "w") as f:
                f.writelines(lines)
            action("Duplicate proxies removed.")
        except Exception as e:
            error("Error while removing duplicates: %s" % e)
    elif remove_duplicates == "no":
        action("Duplicate proxies not removed.")
    else:
        error("Invalid option. Please enter 'yes' or 'no'.")
