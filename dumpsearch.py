####################################################
#
#Version 1.0 for Python 3
# by hadmagic
#https://github.com/hadmagic
#
####################################################
import re
import os
import argparse
import sys
import datetime

#Arguments parser#
parser = argparse.ArgumentParser()
parser.add_argument("PATH", help="precise path of disk")
args = parser.parse_args()

fileList = []
fileSize = 0
folderCount = 0
rootdir = args.PATH

for root, subFolders, files in os.walk(rootdir): #List All files of the path
    folderCount += len(subFolders)
    for file in files:
        f = os.path.join(root,file)
        try:
            fileSize = fileSize + os.path.getsize(f)
        except:
            continue
        fileList.append(f)

        
print(("Total Size    : {0} Mo".format(fileSize // 1024 //1024)))
print("Total Files   :", len(fileList))
print("Total Folders :", folderCount)

config = open('config.cfg')
lines = config.readlines()
name = [] #Name of regex pattern in config.cfg
regex = [] #the regex pattern
worklist = []

for line in lines: #Search in the regex config all the patterns
    match = re.search(r'^([A-Z]*="\(.*\)")', line)
    if match: #Is true
        list_pattern = line.split('=', 1)
        name = list_pattern[0]
        regex = list_pattern[1].strip('\n')
        
        if name is not '' or regex is not '':
            worklist.append([name, regex])
            
config.close()

date = datetime.datetime.now()
print('\nStart at {0}'.format(date.strftime("%Y-%m-%d %H:%M") + "\n"))

lines_seen = set()

for s in range(0, len(worklist)):
    sys.stdout.write('Searching for ' + worklist[s][0] + '\n\n')
    
    out_file = open(worklist[s][0] +".txt", "w")

    for i in range(0, len(fileList)):
        sys.stdout.write('\r' + str(i) + ' / ' + str(len(fileList)) +'\r' )
        rex = (worklist[s][1].replace('"', '')) # Strip " symbole
        try:
            fopen = open(fileList[i], 'rb+') # open all files of the dirs
        except:
            continue

        strings = re.findall(rex, fopen.read().decode('latin1'))
        for string in strings:
            if string not in lines_seen: # Remove duplicate result
                lines_seen.add(string)
                out_file.write(string[0] + '\n')

        fopen.close()
    out_file.close()

   
date = datetime.datetime.now()
print('')
print('\nEnd At {0}'.format(date.strftime("%Y-%m-%d %H:%M") + "\n"))
print('\nLogs are save in {0}'.format(os.path.abspath('.')))
    

        
            
        
        

