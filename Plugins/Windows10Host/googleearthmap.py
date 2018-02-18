import webbrowser
import codecs
import win32clipboard
import win32api
import time
from pywinauto.SendKeysCtypes import SendKeys
from pywinauto.SendKeysCtypes import SendInput

with codecs.open('secondary-key.tmp', 'r', encoding='utf-8') as fo:
    for line in fo:
        value = line
        print(value)


win32clipboard.OpenClipboard()
url = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()
if "https://www.google.com/maps/" in url:
        webbrowser.open(url + "/data=!3m1!4b1!")
        SendKeys("%D")
        SendKeys("^C")
        win32clipboard.OpenClipboard()
        url = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        url = url.replace("/data=!3m1!4b1!", "/data=!3m1!1e3!")
        webbrowser.open(url)
else:
    print("First tell me to Google map somewhere")
