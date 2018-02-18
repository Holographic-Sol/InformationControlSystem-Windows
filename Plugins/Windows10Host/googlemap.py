import webbrowser
import codecs
import win32api
import time
import win32clipboard
from pywinauto.SendKeysCtypes import SendKeys
from pywinauto.SendKeysCtypes import SendInput

with codecs.open('secondary-key.tmp', 'r', encoding='utf-8') as fo:
    for line in fo:
        value = line[10:]

webbrowser.open("https://www.google.com/maps/place/" + value)
time.sleep(2)
SendKeys("%D")
time.sleep(2)
SendKeys("^C")
win32clipboard.OpenClipboard()
url = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()
