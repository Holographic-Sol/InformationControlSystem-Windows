import os
import time
import re
from bs4 import BeautifulSoup
import requests
import win32com.client
import codecs
import distutils.dir_util


#Windows Text To Speech API
speaker = win32com.client.Dispatch("SAPI.SpVoice")

#Files
secondary_key_store = 'secondary-key.tmp'
path = 'Transcriptions/Google/'
googlevalue = 'Transcriptions/Google/googlequestion.tmp'
googlesearch = []

distutils.dir_util.mkpath(path)

with codecs.open(secondary_key_store, 'r', encoding='utf-8') as infile:
    for line in infile:
        value=line
    

url = ("https://www.google.co.uk/search?site=&source=hp&q="+value)
#print('searching https://www.google.co.uk/search?...')
rHead  = requests.get(url)
data = rHead.text
soup = BeautifulSoup(data)
open(googlevalue, 'w').close()
for row in soup.find_all('span'):
    text = row.get_text()
    googlesearch.append(text)
#print('Question:',value)
text = str(googlesearch[4])
#print('Found:',text)
outFile = codecs.open(googlevalue, "a", encoding="utf-8")
outFile.writelines(text)
time.sleep(.5)
googlesearch = []
outFile.close()

with codecs.open(googlevalue, 'r', encoding='utf-8') as infile:
    for line in infile:
        speaker.Speak(line)
