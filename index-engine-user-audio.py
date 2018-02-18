# FILE-INDEXER/VALUE-GENERATOR, Written by Benjamin Jack Cullen

import os
import csv
import time
import codecs
import distutils.dir_util

# Files & Paths
mainDir = 'Indexes'
encode = u'\u5E73\u621015\u200e,'
config = 'config.conf'
rawPath = (mainDir+'/Raw-Indexes')
csvPath = (mainDir+'/CSV-Indexes')
distutils.dir_util.mkpath(rawPath)
distutils.dir_util.mkpath(csvPath)
rawUserAudio = (mainDir+'/Raw-Indexes/raw-user-audio-index.py')
csvUserAudio = (mainDir+'/CSV-Indexes/csv-user-audio-index.py')

# Data

audioext = [".3gp", ".aa", ".aac", ".aax", ".act", ".aiff", ".amr", ".ape", ".au",
            ".awb", ".dct", ".dss", ".dvf", ".flac", ".gsm", ".iklax", ".ivs", ".m4a", ".m4b",
            ".m4p", ".mmf", ".mp3", ".mpc", ".msv", ".ogg", ".oga", ".opus", ".ra", ".rm", ".raw",
            ".sln", ".tta", ".vox", ".wav", ".wma", ".wv", ".webm"]

target_aud = ''
target_root_aud = ''

live_path = []
indexed_path = []
to_file_path = []

write_request = False

def write_index():
    global target_aud
    global target_root_aud
    global rawUserAudio
    global csvUserAudio
    global audioext
    global fullpath
    global write_request
    print('index user audio: writing ...')
    refreshIndex = open(rawUserAudio, "w").close()
    for dirName, subdirList, fileList in os.walk(target_aud):
        for fname in fileList:
            if fname.endswith(tuple(audioext)):
                fullpath = os.path.join(target_root_aud, dirName, fname)
                # print('writing path:',fullpath)
                to_file_path.append(fullpath)

    i = 0
    for to_file_paths in to_file_path:
        txtFile = codecs.open(rawUserAudio, "a", encoding="utf-8")
        # print('writing path:', to_file_path[i])
        txtFile.writelines(to_file_path[i] + "\n")
        txtFile.close()
        i += 1
    time.sleep(2)
    open(csvUserAudio, "w").close
    ifile  = codecs.open(rawUserAudio, "r", encoding="utf-8")
    reader = csv.reader(ifile)
    ofile  = codecs.open(csvUserAudio, "w", encoding="utf-8")
    writer = csv.writer(ofile, delimiter='	', quotechar='"', quoting=csv.QUOTE_ALL)
    for row in reader:
        writer.writerow(row)
    ifile.close()
    ofile.close()
    print('index user audio: wrote ...')
    time.sleep(2)
    write_request = False

def get_live_paths():
    global target_aud
    global target_root_aud
    global live_path
    global audioext
    for dirName, subdirList, fileList in os.walk(target_aud):
        for fname in fileList:
            if fname.endswith(tuple(audioext)):
                fullpath = os.path.join(target_root_aud, dirName, fname)
                live_path.append(fullpath)
                # print(fullpath)

def get_indexed_paths():
    global indexed_path
    global csvUserAudio
    global csvUserAudio
    with codecs.open(rawUserAudio, 'r', encoding='utf-8') as fo:
        for line in fo:
            line = line.strip()
            line = line.replace('"','')
            if line not in indexed_path:
                # print('indexed path:', line)
                indexed_path.append(line)

def compare_index_to_live_path():
    global live_path
    global indexed_path
    global write_request
    # print('comparing indexed paths to live paths')
    i = 0
    for indexed_paths in indexed_path:
        if indexed_path[i] not in live_path:
            # print('not in fs:', indexed_path[i])
            write_request = True
        i += 1

def compare_live_path_to_index():
    global live_path
    global indexed_path
    global write_request
    # print('comparing live paths to indexed paths')
    i = 0
    for live_paths in live_path:
        if live_path[i] not in indexed_path:
            # print('not indexed:',live_path[i])
            write_request = True
        i += 1
    
def get_config():
    global target_aud
    global target_root_aud
    with open(config, 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DIRAUD:'):
                target_aud = line.replace('DIRAUD:', '')
                target_aud = target_aud.strip()
                target_root_aud = str(target_aud.split('\\')[0]+'\\')
                # print(target_root_aud, target_aud)

while 1 == 1:
    if not os.path.exists(rawUserAudio):
        open(rawUserAudio, 'w').close()
    if not os.path.exists(csvUserAudio):
        open(csvUserAudio, 'w').close()
    get_config()
    get_live_paths()
    get_indexed_paths()
    compare_index_to_live_path()
    compare_live_path_to_index()
    to_file_path = []
    indexed_path = []
    live_path = []
    if write_request == True:
        # print('re-write request: True')
        write_index()
##    elif write_request == False:
##        print('re-write request: False')
    time.sleep(1)
