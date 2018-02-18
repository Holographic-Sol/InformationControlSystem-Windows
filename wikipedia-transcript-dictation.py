import os
import codecs
import win32com.client
import requests
from bs4 import BeautifulSoup
import distutils.dir_util
import re
import webbrowser

#Key
key = False

#Windows Text To Speech API
speaker = win32com.client.Dispatch("SAPI.SpVoice")

#Files
curDir = os.getcwd()
path = 'Transcriptions/'
wikipath = 'Transcriptions/WikiTranscription/'
secondary_key = 'secondary-key.tmp'
bookmarkfile = ''
humanoldbookmark = ''

distutils.dir_util.mkpath(path)

#Bookmark
newbookmark = ''
oldbookmark = ''

#Data
availabletranscription = []
targettranscription = ()
textA = []
textB = []
pages = []
name = ''
show_browser = False
dictation = False
use_local_server = False
local_server_addr = ''
local_server_port = ''

def found():
    global local_server_addr
    global local_server_port
    global use_local_server
    global name
    url = ''

    if use_local_server == True:
        # if we use a local wiki we wont have the luxury of modern browser auto complete.
        # we will have to replace spaces with underscores and capitalize first letter of every new word.
        # and append '.html'
        name = name.title()
        name = name.replace(' ', '_')
        url = (local_server_addr+':'+local_server_port+'/wikipedia/A/'+name+'.html')
        url = url.strip()
        print('searching local url:',url)
    elif use_local_server == False:
        url = ("https://www.wikipedia.org/wiki/" + name)

    if show_browser == True:
        webbrowser.open(url)
    if dictation == True:
        speaker.Speak('transcription: '+name)
        articlename = availabletranscription[i]
        bookmarkfile = (availabletranscription[i].replace('.tmp',' 000bookmark.tmp'))
        if os.path.exists(bookmarkfile):
            with codecs.open(bookmarkfile, 'r', encoding='utf-8') as fo:
                for line in fo:
                    idx = line.strip()
                    idxint = int(idx)
                    if idxint>0:
                        speaker.Speak('bookmark found, paragraph: '+idx)
        else:
            with codecs.open(bookmarkfile, 'w', encoding='utf-8') as fo:
                fo.write('0')
                fo.close()
                idxint = 0
        with codecs.open(articlename, 'r', encoding='utf-8') as infile:
            for line in infile:
                textA.append(line)
        number_of_paragraphs = (len(textA)-1)
        
        # print('bookmark:',idxint,'/',number_of_paragraphs)
        if idxint == number_of_paragraphs:
            idxint = 0
        
        for textAs in textA:
            idxint = int(idxint)
            idxstring = str(idxint)
            # print('bookmark:',idxint,'/',number_of_paragraphs)
            with codecs.open(bookmarkfile, 'w', encoding='utf-8') as fo:
                fo.write(idxstring)
                fo.close()
                speaker.Speak(textA[idxint])
                if idxint < number_of_paragraphs:
                    idxint+=1

def not_found():
    global name
    global local_server_port
    global local_server_addr
    url = ''
    # print('creating new bookmark: 0')
    articlename = (wikipath+name+'.tmp')

    if use_local_server == True:
        # if we use a local wiki we wont have the luxury of modern browser auto complete.
        # we will have to replace spaces with underscores and capitalize first letter of every new word.
        # and append '.html'
        name = name.title()
        name = name.replace(' ', '_')
        url = (local_server_addr+':'+local_server_port+'/wikipedia/A/'+name+'.html')
        url = url.strip()
        print('searching local url:',url)
    elif use_local_server == False:
        url = ("https://www.wikipedia.org/wiki/" + name)

    print('searching',url)
    rHead  = requests.get(url)
    data = rHead.text
    soup = BeautifulSoup(data, "html.parser")
    
    #opt 1
    open(articlename, 'w').close()
    for row in soup.find_all('p'):
        text = row.get_text()
        text = re.sub(r'\[.*?\]', '', text)
        text = (text+'\n')
        outFile = codecs.open(articlename, "a", encoding="utf-8")
        outFile.writelines(text)
        outFile.close()
        
    #opt 2
    if "refer to:" in text:
        open(articlename, 'w').close()
        for row in soup.find_all('a'):
            ref = row.get_text()
            ref = ref.lower()
            if ref.startswith(name):
                ref = ref.strip(name)
                outFile = codecs.open(articlename, "a", encoding="utf-8")
                outFile.writelines(ref)
        outFile.close()

    #opt 3
    if "Other reasons this message may be displayed:" in text:
        open(articlename, 'w').close()
        for link in soup.find_all('a'):
            y = (link.get('href'))
            if y == None:
                pass
            else:
                ystring = y.lower()
                valuestring = name.replace(' ', '+')
                if valuestring in ystring:
                    pages.append(ystring)
        url = pages[0]
        url = ('https:'+url)
        rHead = requests.get(url)
        data = rHead.text
        soup = BeautifulSoup(data, "html.parser")
        for link in soup.find_all('a'):
            y = (link.get('href'))
            if y == None:
                pass
            else:
                ystring = y.lower()
                ystring = ystring.replace('(', '')
                ystring = ystring.replace(')', '')
                valuestring = name.replace(' ','_')
                valuestring = ('/wiki/'+valuestring)
                if valuestring in ystring:
                    # print('FOUND: '+y)
                    url = ('https://en.wikipedia.org'+y)
                    # print(url)
                    rHead  = requests.get(url)
                    data = rHead.text
                    soup = BeautifulSoup(data, "html.parser")
                    for row in soup.find_all('p'):
                        text = row.get_text()
                        text = re.sub(r'\[.*?\]', '', text)
                        text = (text+'\n')
                        outFile = codecs.open(articlename, "a", encoding="utf-8")
                        outFile.writelines(text+'\n')
        outFile.close()
    with codecs.open(articlename, 'r', encoding='utf-8') as infile:
        for line in infile:
            textB.append(line)
        infile.close()
            
    textlen = (len(textB)-1) # number of paragraphs
    if textlen>0:
        # print('creating new bookmark: 0')
        articlename = (wikipath+name+'.tmp')
        bookmarkfile = (wikipath+name+' 000bookmark.tmp')
        with codecs.open(bookmarkfile, 'w', encoding='utf-8') as fo:
            bookmark = '0'
            fo.writelines('0')
            fo.close()
        i=0
        if show_browser == True:
            url = ("https://www.wikipedia.org/wiki/" + name)
            webbrowser.open(url)
        for textBs in textB:
            iint = int(i)
            istring = str(i)
            # print('bookmark:',iint,'/',textlen)
            with codecs.open(bookmarkfile, 'w', encoding='utf-8') as fo:
                fo.write(istring)
                fo.close()
                if dictation == True:
                    speaker.Speak(textB[i])
                    if iint < textlen:
                        i+=1
                else:
                    break
    else:
        os.remove(articlename)
        speaker.Speak('nothing found for'+name)

# Get spoken value key
# print('1. retrieving stored search string')        
with codecs.open(secondary_key, 'r', encoding='utf-8') as infile:
    for line in infile:
        name = line
        name = name.strip()
    # print('2. requested transcription:',name)
    bookmarkfile = (path+name+' 000bookmark.tmp')
    infile.close()

with open('config.conf', 'r') as fo:
    for line in fo:
        line = line.strip()
        if line == 'WIKI_TRANSCRIPT_SHOW_BROWSER: enabled':
            print('show browser: enabled')
            show_browser = True
        if line == 'WIKI_TRANSCRIPT_SHOW_BROWSER: disabled':
            print('show browser: disabled')
            show_browser = False

with open('config.conf', 'r') as fo:
    for line in fo:
        line = line.strip()
        if line == 'WIKI_TRANSCRIPT_DICTATE: enabled':
            print('dictation: enabled')
            dictation = True
        if line == 'WIKI_TRANSCRIPT_DICTATE: disabled':
            print('dictation: disabled')
            dictation = False

def get_local_config_func():
    global local_server_port
    global local_server_addr
    global use_local_server
    with open('config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('WIKI_LOCAL_SERVER: '):
                local_server_addr = line.replace('WIKI_LOCAL_SERVER: ', '')
                local_server_addr = local_server_addr.strip()
                print('local wiki server:', local_server_addr)
            if line.startswith('WIKI_LOCAL_SERVER_PORT: '):
                local_server_port = line.replace('WIKI_LOCAL_SERVER_PORT: ', '')
                local_server_port = local_server_port.strip()
                print('local wiki port:', local_server_port)
    # after further checks enable
    use_local_server = True

with open('config.conf', 'r') as fo:
    for line in fo:
        line = line.strip()
        if line.startswith('ALLOW_WIKI_LOCAL_SERVER: enabled'):
            get_local_config_func()
            print('local wiki enabled: getting address and port configuration')
        if line.startswith('ALLOW_WIKI_LOCAL_SERVER: disabled'):
            print('local wiki server disabled: using world wide web')

        
# print('3. retrieving stored transcripts')
for dirName, subdirList, fileList in os.walk(path):
    for fname in fileList:
        if fname.endswith('.tmp'):
            fullPath = os.path.join(curDir, dirName, fname)
            availabletranscription.append(fullPath)

i=0
nf = True
# print('4. comparing request to available transcriptions')
for availabletranscriptions in availabletranscription:
    loosetranscriptionname = availabletranscription[i]
    if name in loosetranscriptionname:
        if not loosetranscriptionname.endswith('000bookmark.tmp'):
            if loosetranscriptionname.endswith('.tmp'):
                # print('5. transcription found:', availabletranscription[i])
                nf = False
                found()
                break
                
            else:
                i+=1
                nf = True
        else:
            i+=1
            nf = True
    else:
        i+=1
        nf = True

if nf == True:
    not_found()
