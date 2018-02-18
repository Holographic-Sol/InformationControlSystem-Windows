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
rawUserVideo = (mainDir+'/Raw-Indexes/raw-user-video-index.py')
csvUserVideo = (mainDir+'/CSV-Indexes/csv-user-video-index.py')

# Data

vidext = [".webm", ".mkv", ".flv", ".vob", ".ogb", ".ogg", ".gif", ".gifv", ".mng", ".avi",
          ".mov", ".wmv", ".yuv", ".rm", ".rmvb", ".asf", ".mp4", ".m4p", ".m4v", ".mpg", ".mp2",
          ".mpeg", ".mpe", ".mpv", ".m2v", ".svi", ".3gp", ".3g2", ".mxf", ".roq", ".nsv", ".f4v", ".f4p",
          ".f4a", ".f4b"]

target_vid = ''
target_root_vid = ''
live_path = []
indexed_path = []

write_request = False

def write_index():
    global target_vid
    global target_root_vid
    global rawUserVideo
    global csvUserVideo
    global vidext
    global fullpath
    global write_request
    print('index user video: writing ...')
    refreshIndex = open(rawUserVideo, "w").close()
    for dirName, subdirList, fileList in os.walk(target_vid):
        for fname in fileList:
            if fname.endswith(tuple(vidext)):
                fullpath = os.path.join(target_root_vid, dirName, fname)
                # print('writing path:',fullpath)
                to_file_path.append(fullpath)

    i = 0
    for to_file_paths in to_file_path:
        txtFile = codecs.open(rawUserVideo, "a", encoding="utf-8")
        # print('writing path:', to_file_path[i])
        txtFile.writelines(to_file_path[i] + "\n")
        txtFile.close()
        i += 1
    time.sleep(2)
    open(csvUserVideo, "w").close
    ifile  = codecs.open(rawUserVideo, "r", encoding="utf-8")
    reader = csv.reader(ifile)
    ofile  = codecs.open(csvUserVideo, "w", encoding="utf-8")
    writer = csv.writer(ofile, delimiter='	', quotechar='"', quoting=csv.QUOTE_ALL)
    for row in reader:
        writer.writerow(row)
    ifile.close()
    ofile.close()
    print('index user video: wrote ...')
    time.sleep(2)
    write_request = False

def get_live_paths():
    global target_vid
    global target_root_vid
    global live_path
    global vidext
    for dirName, subdirList, fileList in os.walk(target_vid):
        for fname in fileList:
            if fname.endswith(tuple(vidext)):
                fullpath = os.path.join(target_root_vid, dirName, fname)
                live_path.append(fullpath)
                # print(fullpath)

def get_indexed_paths():
    global indexed_path
    global csvUserVideo
    global csvUserVideo
    with codecs.open(rawUserVideo, 'r', encoding='utf-8') as fo:
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
    global target_vid
    global target_root_vid
    with open(config, 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DIRVID:'):
                target_vid = line.replace('DIRVID:', '')
                target_vid = target_vid.strip()
                target_root_vid = str(target_vid.split('\\')[0]+'\\')
                # print(target_root_vid, target_vid)

while 1 == 1:
    if not os.path.exists(rawUserVideo):
        open(rawUserVideo, 'w').close()
    if not os.path.exists(csvUserVideo):
        open(csvUserVideo, 'w').close()
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

