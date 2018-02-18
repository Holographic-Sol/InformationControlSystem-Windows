import time
import win32clipboard
import win32com.client
import win32api
from pywinauto.SendKeysCtypes import SendKeys
from pywinauto.SendKeysCtypes import SendInput

shell = win32com.client.Dispatch("WScript.Shell")

SendKeys("%D")
time.sleep(0.1)
SendKeys("^C")
time.sleep(0.1)
win32clipboard.OpenClipboard()
url = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()
time.sleep(0.1)
print(url)
if "https://www.youtube" in url:
    SendKeys("{TAB}")
    time.sleep(0.1)
    SendKeys("{TAB}")
    time.sleep(0.1)
    SendKeys("{TAB}")
    time.sleep(0.1)
    SendKeys("{TAB}")
    time.sleep(0.1)
    SendKeys("{TAB}")
    time.sleep(0.1)
    SendKeys("{TAB}")
    time.sleep(0.1)
    SendKeys("{TAB}")
    time.sleep(0.1)
    SendKeys("{TAB}")
    time.sleep(0.1)
    SendKeys("{TAB}")
    time.sleep(0.2)
    shell.SendKeys("0")
else:
    print(url)
    print("must be lost")
