import os
import codecs
from pathlib import Path
import win32com.client
import time
import re
import datetime
import distutils.dir_util

curDir = os.getcwd()
path = 'Transcriptions/'
secondary_key = 'secondary-key.tmp'
target_transcript = ''
distutils.dir_util.mkpath(path)

target_found = False

#Windows Text To Speech API
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# print('1. retrieving stored search string')        
with codecs.open(secondary_key, 'r', encoding='utf-8') as infile:
    for line in infile:
        secondary_key_str = line
        secondary_key_str = secondary_key_str.strip()
    print('requested transcript:',secondary_key_str)
    infile.close()

# print('3. retrieving stored transcripts')
for dirName, subdirList, fileList in os.walk(path):
    for fname in fileList:
        if fname.endswith('.tmp'):
            if secondary_key_str in fname:
                if not fname.endswith('000bookmark.tmp'):
                    target_transcript = os.path.join(curDir, dirName, fname)
                    print('found:',target_transcript)
                    target_found  = True
                    
if target_found == True:         
    with codecs.open(target_transcript, 'r', encoding='utf-8') as fo:
        for line in fo:
            #print(line)
            speaker.Speak(line)
else:
    print("couldn't find anything...")
