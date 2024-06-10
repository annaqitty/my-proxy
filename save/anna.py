import urllib.request
import threading
import re
import sys
import queue
import time
from urllib.parse import urlparse
from urllib.error import URLError
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

def get_orders():
    name = "output_proxy.txt"
    leech_list = "sites.json"  # JSON file containing URLs
    return [name, leech_list]

class ScanThread(threading.Thread):
    def __init__(self, thread_pool, proxy_list, good_sites, debug=False):
        threading.Thread.__init__(self)
        self.thread_pool = thread_pool
        self.proxy_list = proxy_list
        self.good_sites = good_sites
        self.debug = debug

    def run(self):
        while True:
            url = self.thread_pool.get()
            try:
                if not url.startswith("http://") and not url.startswith("https://"):
                    url = "http://" + url
                get = urllib.request.urlopen(url, timeout=10)  # Adjust timeout value as needed
                data = get.read().decode('utf-8')
                if self.debug:
                    print(blue + "Debug HTML content for %s:" % url + defcol)
                    print(data)
                domain = urlparse(url).netloc  # Extract domain
                valid_proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{2,5})', data)
                action("%s proxies found on %s" % (len(valid_proxies), domain))
                for proxy in valid_proxies:
                    self.proxy_list.put("%s:%s\n" % proxy)
                if len(valid_proxies) > 0:
                    self.good_sites.put(domain + "\n")
            except URLError as e:
                error("Error: %s" % e.reason)
            except Exception as e:
                error("Error: %s" % e)
            finally:
                self.thread_pool.task_done()

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
   |||  K.E.U.R - I.P - R.A.N.G.E.R
   |||    ╔═╦═╦╦═╦╦═╗╔═╦╦══╦══╦╦╗
   |||    ║╩║║║║║║║╩║║╚║╠╗╔╩╗╔╩╗║
___|||___ ╚╩╩╩═╩╩═╩╩╝╚═╩╝╚╝ ╚╝ ╚╝

  By : AnnaQitty
  Github : github.com/annaqitty    

                        
                      
                      """
    for N, line in enumerate(x.split("\n")):
        sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
        time.sleep(0.05)

def remove_duplicates_notice():
    logo()
    action("Removing duplicate proxies...")

def end_notice():
    logo()
    action("Done leeching.")

if len(sys.argv) < 3:
    errorExit("Usage: python proxies.py <output.txt> <num_threads> [-l yourlist]")

orders = get_orders()
try:
    proxy_list = queue.Queue()
    good_sites = queue.Queue()
except Exception as e:
    errorExit("Error creating queues: %s" % e)

try:
    with open(orders[1], "r") as file:
        json_data = json.load(file)
        sites = [entry['url'] for entry in json_data['sites'] if 'url' in entry]
except Exception as e:
    errorExit("Error reading JSON file: %s" % e)

# Number of threads
num_threads = int(sys.argv[2])
debug = "--debug" in sys.argv

thread_pool = queue.Queue(0)

for i in range(num_threads):
    thread = ScanThread(thread_pool, proxy_list, good_sites, debug=debug)
    thread.start()

try:
    for url in sites:
        thread_pool.put(url)
except KeyboardInterrupt:
    errorExit("Keyboard interrupt detected. Exiting...")

while True:
    if thread_pool.empty():
        break
    time.sleep(1)

thread_pool.join()

try:
    with open(orders[0], "w") as f:
        while not proxy_list.empty():
            f.write(proxy_list.get())
    action("Proxy list written to %s" % orders[0])
except Exception as e:
    error("Error writing to output file: %s" % e)

try:
    with open("good_sites.txt", "w") as f:
        while not good_sites.empty():
            f.write(good_sites.get())
    action("Good sites written to good_sites.txt")
except Exception as e:
    error("Error writing to good sites file: %s" % e)

total_proxies = sum(1 for line in open(orders[0]))

if total_proxies > 2000:
    print(yellow + "Total proxies found: %s" % total_proxies + defcol)
else:
    print(orange + "Total proxies found: %s" % total_proxies + defcol)

# Option to remove duplicate proxies
remove_duplicates = input("Do you want to remove duplicate proxies? (yes/no): ").strip().lower()
if remove_duplicates == "yes":
    remove_duplicates_notice()
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

end_notice()
