import os
import requests
import win32com.client
from bs4 import BeautifulSoup

speaker = win32com.client.Dispatch("SAPI.SpVoice")
secondary_key_store = 'secondary-key.tmp'

with open(secondary_key_store, 'r', encoding='utf-8') as fo:
    for line in fo:
        value=line
url = ("https://en.wiktionary.org/wiki/"+value)
#print('searching '+url)
rHead  = requests.get(url)
data = rHead.text
soup = BeautifulSoup(data)
#print('Define Word:',value)
speaker.Speak(value)
for row in soup.find_all('ol'):
    text = row.get_text()
    text = text.strip()
    if text != value:
        #print('Definition:',text)
        speaker.Speak(text)
