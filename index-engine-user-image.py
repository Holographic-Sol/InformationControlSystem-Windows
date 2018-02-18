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
rawPath = (mainDir+'/Raw-Indexes')
csvPath = (mainDir+'/CSV-Indexes')
distutils.dir_util.mkpath(rawPath)
distutils.dir_util.mkpath(csvPath)
rawUserImg = (mainDir+'/Raw-Indexes/raw-user-image-index.py')
csvUserImg = (mainDir+'/CSV-Indexes/csv-user-image-index.py')

# Data
imgext = [".png", ".jpg", ".jpeg", ".gif", ".ico", ".PNG"]

target_img = ''
target_root_img = ''

live_path = []
indexed_path = []
to_file_path = []

write_request = False

def write_index():
    global target_img
    global target_root_img
    global rawUserImg
    global csvUserImg
    global imgext
    global fullpath
    global write_request
    print('index user image: writing ...')
    refreshIndex = open(rawUserImg, "w").close()
    for dirName, subdirList, fileList in os.walk(target_img):
        for fname in fileList:
            if fname.endswith(tuple(imgext)):
                fullpath = os.path.join(target_root_img, dirName, fname)
                # print('writing path:',fullpath)
                to_file_path.append(fullpath)

    i = 0
    for to_file_paths in to_file_path:
        txtFile = codecs.open(rawUserImg, "a", encoding="utf-8")
        # print('writing path:', to_file_path[i])
        txtFile.writelines(to_file_path[i] + "\n")
        txtFile.close()
        i += 1
    time.sleep(2)
    open(csvUserImg, "w").close
    ifile  = codecs.open(rawUserImg, "r", encoding="utf-8")
    reader = csv.reader(ifile)
    ofile  = codecs.open(csvUserImg, "w", encoding="utf-8")
    writer = csv.writer(ofile, delimiter='	', quotechar='"', quoting=csv.QUOTE_ALL)
    for row in reader:
        writer.writerow(row)
    ifile.close()
    ofile.close()
    print('index user image: wrote ...')
    time.sleep(2)
    write_request = False

def get_live_paths():
    global target_img
    global target_root_img
    global live_path
    global audioext
    for dirName, subdirList, fileList in os.walk(target_img):
        for fname in fileList:
            if fname.endswith(tuple(imgext)):
                fullpath = os.path.join(target_root_img, dirName, fname)
                live_path.append(fullpath)
                # print(fullpath)

def get_indexed_paths():
    global indexed_path
    global csvUserImg
    global csvUserImg
    with codecs.open(rawUserImg, 'r', encoding='utf-8') as fo:
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
    global target_img
    global target_root_img
    with open(config, 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DIRIMG:'):
                target_img = line.replace('DIRIMG:', '')
                target_img = target_img.strip()
                target_root_img = str(target_img.split('\\')[0]+'\\')
                # print(target_root_img, target_img)

while 1 == 1:
    if not os.path.exists(rawUserImg):
        open(rawUserImg, 'w').close()
    if not os.path.exists(csvUserImg):
        open(csvUserImg, 'w').close()
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
