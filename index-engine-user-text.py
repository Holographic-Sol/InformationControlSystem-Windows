# FILE-INDEXER/VALUE-GENERATOR, Written by Benjamin Jack Cullen

import os
import sys
import csv
import time
import codecs
import distutils.dir_util
import fileinput
import datetime

# Files & Paths
mainDir = 'Indexes'
encode = u'\u5E73\u621015\u200e,'
config = 'config.conf'
rawPath = (mainDir+'\\Raw-Indexes')
csvPath = (mainDir+'\\CSV-Indexes')
distutils.dir_util.mkpath(rawPath)
distutils.dir_util.mkpath(csvPath)
rawUserText = (mainDir+'/Raw-Indexes/raw-user-text-index.py')
csvUserText = (mainDir+'/CSV-Indexes/csv-user-text-index.py')

# Data

txtext = [".txt", ".log", ".tmp", ".pdf", ".text"]

target_txt = ''
target_root_txt = ''

live_path = []
indexed_path = []

write_request = False

def write_index():
    global target_txt
    global target_root_txt
    global rawUserText
    global csvUserText
    global audioext
    global fullpath
    global write_request
    print('index user text: writing ...')
    refreshIndex = open(rawUserText, "w").close()
    for dirName, subdirList, fileList in os.walk(target_txt):
        for fname in fileList:
            if fname.endswith(tuple(txtext)):
                fullpath = os.path.join(target_root_txt, dirName, fname)
                # print('writing path:',fullpath)
                to_file_path.append(fullpath)

    i = 0
    for to_file_paths in to_file_path:
        txtFile = codecs.open(rawUserText, "a", encoding="utf-8")
        # print('writing path:', to_file_path[i])
        txtFile.writelines(to_file_path[i] + "\n")
        txtFile.close()
        i += 1
    time.sleep(2)
    open(csvUserText, "w").close
    ifile  = codecs.open(rawUserText, "r", encoding="utf-8")
    reader = csv.reader(ifile)
    ofile  = codecs.open(csvUserText, "w", encoding="utf-8")
    writer = csv.writer(ofile, delimiter='	', quotechar='"', quoting=csv.QUOTE_ALL)
    for row in reader:
        writer.writerow(row)
    ifile.close()
    ofile.close()
    print('index user text: wrote ...')
    time.sleep(2)
    write_request = False

def get_live_paths():
    global target_txt
    global target_root_txt
    global live_path
    global audioext
    for dirName, subdirList, fileList in os.walk(target_txt):
        for fname in fileList:
            if fname.endswith(tuple(txtext)):
                fullpath = os.path.join(target_root_txt, dirName, fname)
                live_path.append(fullpath)
                # print(fullpath)

def get_indexed_paths():
    global indexed_path
    global csvUserText
    global csvUserText
    with codecs.open(rawUserText, 'r', encoding='utf-8') as fo:
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
    global target_txt
    global target_root_txt
    with open(config, 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DIRTXT:'):
                target_txt = line.replace('DIRTXT:', '')
                target_txt = target_txt.strip()
                target_root_txt = str(target_txt.split('\\')[0]+'\\')
                # print(target_root_txt, target_txt)

while 1 == 1:
    if not os.path.exists(rawUserText):
        open(rawUserText, 'w').close()
    if not os.path.exists(csvUserText):
        open(csvUserText, 'w').close()
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
