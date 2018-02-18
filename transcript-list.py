import os
import codecs
import win32com.client
import time
import re

import distutils.dir_util

#Windows Text To Speech API
speaker = win32com.client.Dispatch("SAPI.SpVoice")

#Files
curDir = os.getcwd()
path = 'Transcriptions/'
latestpath = 'Transcriptions/Articles/'
secondary_key_file = 'secondary-key.tmp'

distutils.dir_util.mkpath(path)

#Data
secondary_key = ''
availabletranscription = []
speakavailabletranscription = []

# List All
def list_all():
    #print('2. retrieving stored transcripts')
    for dirName, subdirList, fileList in os.walk(path):
        for fname in fileList:
            if fname.endswith('.tmp'):
                fullPath = os.path.join(curDir, dirName, fname)
                availabletranscription.append(fullPath)
                if secondary_key in fname:
                    if ' 000bookmark.tmp' not in fname:
                        spokenfname = fname
                        spokenfname = spokenfname.replace('.tmp', '')
                        if spokenfname not in speakavailabletranscription:
                            speakavailabletranscription.append(spokenfname)
    speaker.Speak('available transcriptions for '+secondary_key)
    i=0
    for speakavailabletranscriptions in speakavailabletranscription:
        if len(speakavailabletranscription[i])>1:
            #print(speakavailabletranscription[i])
            speaker.Speak(speakavailabletranscription[i])
        i+=1
    
# 0 Begin
with codecs.open(secondary_key_file, 'r', encoding='utf-8') as fo:
    for line in fo:
        secondary_key = line
        secondary_key = secondary_key.strip()
    #print('1. list transcriptions containing:',secondary_key)
    fo.close()

    if len(secondary_key)>1:
        list_all()
