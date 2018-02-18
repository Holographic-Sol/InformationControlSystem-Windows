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
rawUserProg = (mainDir+'/Raw-Indexes/raw-user-program-index.py')
csvUserProg = (mainDir+'/CSV-Indexes/csv-user-program-index.py')

# Data
configB = []
directory = []
rootDir = []
livePath = []
indexedPath = []
startTime = datetime.datetime.now()
iteration=1
rewrite_request = False
progext = [".lnk", ".bat"]
program_dir = 'UserPrograms/'
cwd = os.getcwd()

def rewrite():
    refreshIndex = open(rawUserProg, "w").close()
    for dirName, subdirList, fileList in os.walk(program_dir):
        for fname in fileList:
            if fname.endswith(tuple(progext)):
                fullPath = os.path.join(cwd+'/'+program_dir+fname)
                #print(fullPath)
                txtFile = codecs.open(rawUserProg, "a", encoding="utf-8")
                txtFile.writelines(fullPath + "\n")
                txtFile.close()
    open(csvUserProg, "w").close
    ifile  = codecs.open(rawUserProg, "r", encoding="utf-8")
    reader = csv.reader(ifile)
    ofile  = codecs.open(csvUserProg, "w", encoding="utf-8")
    writer = csv.writer(ofile, delimiter='	', quotechar='"', quoting=csv.QUOTE_ALL)
    for row in reader:
        writer.writerow(row)
    ifile.close()
    ofile.close()
    rewrite_request = False

while 1==1:
    if not os.path.exists(rawUserProg):
        rewrite()

    if os.path.exists(rawUserProg):
        # Read Index File
        with codecs.open(rawUserProg, 'r', encoding='utf-8') as fo:
            for line in fo:
                line=line.strip()
                if line not in indexedPath:
                    indexedPath.append(line)
        # Read Directory
        for dirName, subdirList, fileList in os.walk(program_dir):
            for fname in fileList:
                if fname.endswith(tuple(progext)):
                    fullPath = os.path.join(cwd+'/'+program_dir+fname)
                    if fullPath not in livePath:
                        livePath.append(fullPath)
        # Is livePath in indexedPath
        i=0
        for livePaths in livePath:
            if livePath[i] not in indexedPath:
                #print('not in index',livePath[i])
                rewrite_request = True
            i+=1
        # Is indexedPath in livePath
        i=0
        for indexedPaths in indexedPath:
            if indexedPath[i] not in livePath:
                #print('not in filesystem',indexedPath[i])
                rewrite_request = True
            i+=1
        if rewrite_request == True:
            rewrite()
            rewrite_request = False
    indexedPath = []
    livePath = []
    configB = []
    directory = []
    rootDir = []
    time.sleep(5)
