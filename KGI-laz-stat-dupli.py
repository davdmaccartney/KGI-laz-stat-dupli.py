import os
import numpy as np
from laspy.file import File
import time
import easygui
from imutils import paths
import fnmatch
import sys
import pandas as pd
from timeit import default_timer as timer



pd.options.display.float_format = '{:.6f}'.format

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def update_progress(progress):
    barLength = 30 # Modify this to change the length of the progress bar
    
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% ".format( "#"*block + "-"*(barLength-block), int(progress*100))
    sys.stdout.write(text)
    sys.stdout.flush()



dirname1 = easygui.diropenbox(msg=None, title="Please select the target directory", default=None )
total_con=len(fnmatch.filter(os.listdir(dirname1), '*.las'))
D1 = str(total_con)
msg = str(total_con) +" files do you want to continue?"
title = "Please Confirm"
if easygui.ynbox(msg, title, ('Yes', 'No')): # show a Continue/Cancel dialog
    pass # user chose Continue else: # user chose Cancel
else:
    exit(0)


   
file_Dir1 = os.path.basename(dirname1)

ci=0
cls()
eR=0

f = open(dirname1+"\Stat-Duplication.txt", "w")


for filename in os.listdir(dirname1):
     if filename.endswith(".las"):
        ci  += 1
        #print('Reading LiDAR')
        #start = timer()
              
        try:
            inFile1 = File(dirname1+'\\'+filename, mode='r')


        except OSError:
           easygui.msgbox('No file:'+filename+' in :'+dirname2+' the process will end')
           sys.exit(0) 

        # header offset and scallling
        hXori = inFile1.header.offset[0]
        hYori = inFile1.header.offset[1]
        hZori = inFile1.header.offset[2]
        hSori = inFile1.header.scale[0]
        
        
               
        # creating the Panda array with the joint attributes
        #
        #ori = pd.DataFrame(np.empty(0, dtype=[('ori',np.int),('gps_time',np.float64), ('gps_time_int',np.uint32),('flag_byte',np.int),('intensity',np.int),('return_num',np.int),('num_returns',np.int),('angle',np.ubyte)]))
        ori = pd.DataFrame(np.empty(0, dtype=[('gps_time',np.float64)]))

        # feeding the Panda array

        ori['gps_time'] = (inFile1.gps_time)
        #ori['gps_time_int'] =round(ori.gps_time*1000000)
        #ori['intensity'] = (inFile1.intensity)
        #ori['return_num'] = (inFile1.return_num)
        #ori['num_returns'] = (inFile1.num_returns)
        #ori['flag_byte'] = (inFile1.flag_byte)
        #ori['angle'] = (inFile1.scan_angle_rank)
        #ori['ori'] = ori.index
        
        # getting the stat
        num = len(ori.index)
        #num_gps_dup=ori.duplicated(subset=['gps_time','intensity','flag_byte','angle'], keep='first').sum()
        num_gps_dup=ori.duplicated(subset=['gps_time'], keep='first').sum()
        
        # writing to the file
        f.write(filename+'    '+str(num)+'    '+str(num_gps_dup)+'\n')
        f.flush
        inFile1.close()

        update_progress(ci/int(D1))

 
if eR>0:
   print('Process finnihed :'+str(eR)+' errors read Comp-result.txt in the source folder')
else:
   print('Process finnihed with no errors')
   

exit(0)