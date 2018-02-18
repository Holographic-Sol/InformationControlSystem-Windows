import os
import codecs
import win32com.client
import time
import re
import speech_recognition as sr

#Speech Recognition
r = sr.Recognizer()
m = sr.Microphone()

#Windows Text To Speech API
speaker = win32com.client.Dispatch("SAPI.SpVoice")

#Files
curDir = os.getcwd()
path = 'Transcriptions/'
secondary_key_file = 'secondary-key.tmp'

#Data
secondary_key = ''
bookmark_found = []
bookmark_found_name = []
response = False
repeat=False

def reset_bookmark():
    with codecs.open(bookmark_found[0], 'w', encoding='utf-8') as fo:
        fo.write('0')
        fo.close()
    speaker.Speak(secondary_key+' bookmark'+' has been removed.')
# 0 Begin
with codecs.open(secondary_key_file, 'r', encoding='utf-8') as fo:
    for line in fo:
        line = line.strip()
        secondary_key = line
    fo.close()
# 1 Get Bookmarks containing secondary-key
for dirName, subdirList, fileList in os.walk(path):
    for fname in fileList:
        if fname.endswith('.tmp'):
            fullPath = os.path.join(curDir, dirName, fname)
            if secondary_key in fname:
                if ' 000bookmark.tmp' in fname:
                    bookmark_found.append(fullPath)
                    bookmark_found_name.append(fname)
if len(bookmark_found)>1:
    i=0
    speaker.Speak('please be more specific. more than one bookmarks found.')
    for bookmark_found_names in bookmark_found_name:
        human_fname = bookmark_found_name[i].replace(' 000bookmark.tmp', ' bookmark')
        speaker.Speak(human_fname)
        i+=1
else:
    speaker.Speak('bookmark found.')
    try:
        with m as source: r.adjust_for_ambient_noise(source)
        speaker.Speak('are you sure you want to remove '+secondary_key+' bookmark')
        while response==False:
            if repeat == True:
                speaker.Speak('are you sure')
            with m as source: audio = r.listen(source)
            try:
                value = r.recognize_google(audio).lower()
                if value=='yes':
                    reset_bookmark()
                    response=True
                if value=='no':
                    speaker.Speak('keeping '+secondary_key+' bookmark')
                    response=True
                repeat=True
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                pass
    except KeyboardInterrupt:
        pass
    
            
