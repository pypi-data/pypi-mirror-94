import requests
import urllib
import urllib.request
import time
from pip._internal import main

build = 'Name: ZapURL\nVersion: v0.2.0\nLanguage_Base: Python3\nRequired_Modules: requests, urllib, urllib.request, time, pip._internal\nRelease_Date 2/10/2021'

currver = "v0.2.0"

def short(url):
  shortener = 'http://ZapURL.unaux.com/create.php'
  webinput = {'urlin': url, 'source': "66RnBldNCZZooAklXiip"}
  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
  }

  file = requests.post(shortener, data = webinput, headers = headers)
  file = file.text
  print(file[604:637])

def custom(url, email, name, custom):
  shortener = 'http://ZapURL.unaux.com/create.php'
  webinput = {'urlin': url, 'source': "66RnBldNCZZooAklXiip", 'custom': True, 'email': email, 'name': name, 'cusurl': custom}
  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
  }

  file = requests.post(shortener, data = webinput, headers = headers)
  file = file.text
  if custom in file:
    print(f"http://ZapURL.unaux.com/c/{custom}/")
  else:
    print("Custom Directory already Taken! Choose another name.")

  

def about():
  print(build)

def site():
  print("http://ZapURL.unaux.com/")

def latest():
  url = "https://UpdateServer.jonathan2018.repl.co/ZapURL"
  r = requests.head(url)
  if (r.status_code == 200):
    print("Connected to server!\n----------------------")
    pass
  else:
    print ("Update server currently isn't available to connect... Please check back in later.")
    return "[Shutdown Error] Unable to reach Update Server."
  print("Fetching Latest Info from Server...\n---------------------------")
  file = urllib.request.urlopen(url)
  for line in file:
    processed_line = line.decode("utf-8")
    time.sleep(0.5)
    print(processed_line)
  time.sleep(1)
  print("---------------------------\nAll of the latest information has been retrieved from our servers.")

def update():
  url = "https://UpdateServer.jonathan2018.repl.co/ZapURL/update"
  r = requests.head(url)
  if (r.status_code == 200):
    print("Starting Update!\n----------------------")
    pass
  else:
    print ("Unable to check for new version, please check back in later. :(")
    return "[Shutdown Error] Unable to reach Update Server."
  print("Checking version...\n---------------------------")

  file = urllib.request.urlopen(url)
  for line in file:
    newver = line.decode("utf-8")
    
  if newver == currver:
    print ("You are already running the latest version. No need to update")
    return "[Stop Error] Already running newest version"
  else:
    print("Installing package from PyPi...")
    main.main(['install', '--upgrade', 'Zapurl'])
  time.sleep(1)
  print("---------------------------\nNewest package files of ZapURL has been retrieved & installed.")
  print(newver)
