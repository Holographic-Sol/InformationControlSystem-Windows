import time
import win32clipboard
import win32com.client
import win32api
import requests
import webbrowser
from bs4 import BeautifulSoup
from pywinauto.SendKeysCtypes import SendKeys
from pywinauto.SendKeysCtypes import SendInput

shell = win32com.client.Dispatch("WScript.Shell")
time.sleep(2)

with open('secondary-key.tmp', 'r') as fo:
    for line in fo:
        line = line.strip()
        value = line

value = value[14:]
search_string = value.lower()
SendKeys("%D")
time.sleep(0.1)
SendKeys("^C")
time.sleep(0.1)
win32clipboard.OpenClipboard()
url = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()
time.sleep(0.1)
print(url)
rHead  = requests.get(url)
data = rHead.text
soup = BeautifulSoup(data)
for link in soup.find_all('a'):
    x = (link.get('title'))
    y = (link.get('href'))
    if x == None:
        pass
    else:
        extCom = ".com"
        extOrg = ".org"
        extCoUk = ".co.uk"
        extNet = ".net"
        if extCom in url:
            idx = url.find('.com')
            subs = url[:idx+4]
            y = str(subs + y)
            xy = (x, y)
            for line in xy:
                line = line.lower()
                if search_string in line:
                    print(line, " ", y, " " + "found")
                    webbrowser.open(y)
                    pass
                elif search_string not in line:
                    pass
        if extOrg in url:
            idx = url.find('.org')
            subs = url[:idx+4]
            y = str(subs + y)
            xy = (x, y)
            for line in xy:
                line = line.lower()
                if search_string in line:
                    print(line, " ", y, " " + "found")
                    webbrowser.open(y)
                    pass
                elif search_string not in line:
                    pass
        if extCoUk in url:
            idx = url.find('.co.uk')
            subs = url[:idx+6]
            y = str(subs + y)
            xy = (x, y)
            for line in xy:
                line = line.lower()
                if search_string in line:
                    print(line, " ", y, " " + "found")
                    webbrowser.open(y)
                    pass
                elif search_string not in line:
                    pass
        if extNet in url:
            idx = url.find('.net')
            subs = url[:idx+4]
            y = str(subs + y)
            xy = (x, y)
            for line in xy:
                line = line.lower()
                if search_string in line:
                    print(line, " ", y, " " + "found")
                    webbrowser.open(y)
                    pass
                elif search_string not in line:
                    pass
