import os
import time
import codecs
import win32com.client
from operator import itemgetter

#Files
curDir = os.getcwd()
path = ''
secondary_key_file = 'secondary-key.tmp'
article_path = 'Transcriptions/'

#lists
article = []
newest_list = []
time_keeper = []

#Data
secondary_key = ''
newest_file = ''
newest_file_human = ''

#Windows Text To Speech API
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# 0. Get Key
with codecs.open(secondary_key_file, 'r', encoding='utf-8') as fo:
    for line in fo:
        secondary_key = line
    
# 3
def found_one_newest():
    newest_file_human = newest_file.replace('.tmp', '')
    print('latest transcription for: '+secondary_key+': '+newest_file_human+' '+dated_files2)
    speaker.Speak('latest transcription for:  '+secondary_key+': '+newest_file_human+' '+dated_files2)

# 1. Append all transcripts to list article
for dirName, subdirList, fileList in os.walk(article_path):
    for fname in fileList:
        lnkext = [".tmp", ".txt"]
        if fname.endswith(tuple(lnkext)):
            fname_path = os.path.join(curDir, dirName, fname)
            #print(fname_path)
            article.append(fname_path)

# 2. Get timestamp for all files names containing value & append to newest_plural
i=0
article_length = len(article)
print(article_length)
article_length-=1
for articles in article:
    dated_files = [(os.path.getmtime(article[i]), os.path.basename(article[i]))]
    dated_files2 = time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(article[i])))
    print(dated_files2)
    if secondary_key in article[i]:
        if ' 000bookmark.tmp' not in article[i]:
            if article[i].endswith('.tmp'):
                dated_files.sort()
                dated_files.reverse()
                if len(dated_files) >=1:
                    newest = dated_files[0]
                    newest_list.append(newest)
                    print('checking:',newest)
                    newest_file = max(newest_list,key=itemgetter(0))[1]
                    
    if i == article_length:
        found_one_newest()
    else:
        i+=1
