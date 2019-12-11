"""
Created October 2019
@author: JRS, script kiddie from gracer
"""

#!/usr/bin/python
#get onsets

import numpy
import os
import glob

handles=[]

## Change this path to match where you have the onset files
basepath='/Users/jennygilbert/Desktop/bbx_log_copies_october28_2019'
os.chdir(basepath)


ignore = ['DATA 	Keypress: o','Level post injecting via pump at address']

#files = [file for file in os.listdir(".") if (file.lower().endswith('.log'))]
#files.sort(key=os.path.getmtime)

#get the global info about the run. 

for file in glob.glob(os.path.join(basepath,'*.log')):
    print(file)
    
#for file in glob.glob(os.path.join(basepath,'*_pre_*.log')):
    #print(file)
     
#for file in glob.glob(os.path.join(basepath,'*.log')):
    #print(file)

    #This will change dependign on the path -- rememeber to count starting at 0 before the first '/'
    sub=file.split('/')[5].split('_')[1]
    run=file.split('/')[5].split('_')[2]
    wave=file.split('/')[5].split('_')[3]
    print([sub,run,wave])
    
#   open the script and read in log data
    with open(file,'r') as infile:
        ssb_cue_onset=[]
        ssb_taste_onset=[]
        usb_cue_onset=[]
        usb_taste_onset=[]
        h2o_cue_onset=[]
        h2o_taste_onset=[]
        neu_onset=[]
        start_time=None
        
        for x in infile.readlines():
#            if x.find('Keypress: q'):
#                continue
            
            if not x.find(ignore[0])>-1 or x.find(ignore[1])>-1:
                
                l_s=x.strip().split()
                
                if x.find('Level start key press')>-1:#find the start
                    l_s=x.strip().split()
                    start_time=float(l_s[0])
                    
                #if x.find('at time= ')>1:
                    #l_s=x.strip().split()
                    #RT.append(l_s[5])
                
                #SSB CUE AND TASTE
                #The SSBs are  either "C0" or "SL" -- no one will receive both, so we can repeat in the parser :)  
                if x.find('image=CO.jpg')>-1:
                    l_s=x.strip().split()
                    print(l_s)
                    ssb_cue_onset.append(float(l_s[0]))

                if x.find('image=SL.jpg')>-1:
                    l_s=x.strip().split()
                    print(l_s)
                    ssb_cue_onset.append(float(l_s[0]))
                 
                #NOTE: we use the post injecting time because it is only listed once 
                if x.find('Level post injecting via pump at address 1')>-1:
                    l_s=x.strip().split()
                    print(l_s)
                    ssb_taste_onset.append(float(l_s[0]))
                
                #USB CUE AND TASTE
                #Just like the SSBs are we can repeat the USB names in the parser 
                if x.find('image=UCO.jpg')>-1:
                    l_s=x.strip().split()
                    print(l_s)
                    usb_cue_onset.append(float(l_s[0]))

                if x.find('image=USL.jpg')>-1:
                    l_s=x.strip().split()
                    print(l_s)
                    usb_cue_onset.append(float(l_s[0]))
                  
                if x.find('Level post injecting via pump at address 2')>-1:
                    l_s=x.strip().split()
                    print(l_s)
                    usb_taste_onset.append(float(l_s[0]))
                
                #WATER CUE AND TASTE
                if x.find('image=water.jpg')>-1:
                    l_s=x.strip().split()
                    print(l_s)
                    h2o_cue_onset.append(float(l_s[0]))

                if x.find('Level post injecting via pump at address 0')>-1:
                    l_s=x.strip().split()
                    print(l_s)
                    h2o_taste_onset.append(float(l_s[0]))
                       
                #rinse
                if x.find('Level RINSE 	25')>-1:
                    neu_onset.append(l_s[0])
                    print(neu_onset)
        
        ssb_cue_onsets=(numpy.asarray(ssb_cue_onset,dtype=float))-start_time 
        usb_cue_onsets=(numpy.asarray(usb_cue_onset,dtype=float))-start_time 
        h2o_cue_onsets=(numpy.asarray(h2o_cue_onset,dtype=float))-start_time                 
 
        ssb_taste_onsets=(numpy.asarray(ssb_taste_onset,dtype=float))-start_time 
        usb_taste_onsets=(numpy.asarray(usb_taste_onset,dtype=float))-start_time
        h2o_taste_onset=(numpy.asarray(h2o_taste_onset,dtype=float))-start_time  
        neu_onsets=(numpy.asarray(neu_onset,dtype=float))-start_time

        files2make=['ssb_cue','usb_cue','h2o_cue','ssb_taste','usb_taste','h2o_cue','h2o_taste','neu']
        mydict={}
        try:
            for files in files2make:
                path='/Users/jennygilbert/Desktop/bbx_log_copies_october28_2019/onsets_for_fsl/%s_%s_%s_%s.txt'%(sub,run,wave,files)
                if os.path.exists(path) == True:
                    print ('exists')
                    break
                else:
                    mydict[files] = path
            
            f_ssbc=open(mydict['ssb_cue'], 'w')
            for t in range(len(ssb_cue_onsets)):
                f_ssbc.write('%f\t1\t1\n'%(ssb_cue_onsets[t]))
            f_ssbc.close()
            
            f_ssbt=open(mydict['ssb_taste'], 'w')
            for t in range(len(ssb_taste_onsets)):
                f_ssbt.write('%f\t6\t1\n' %(ssb_taste_onsets[t]))
            f_ssbt.close()
            
            f_usbc=open(mydict['usb_cue'], 'w')
            for t in range(len(usb_cue_onsets)):
                f_usbc.write('%f\t1\t1\n'%(usb_cue_onsets[t]))
            f_usbc.close()
            
            f_usbt=open(mydict['usb_taste'], 'w')
            for t in range(len(usb_taste_onsets)):
                f_usbt.write('%f\t6\t1\n' %(usb_taste_onsets[t]))
            f_usbt.close()
            
            f_h2oc=open(mydict['h2o_cue'], 'w')
            for t in range(len(h2o_cue_onsets)):
                f_h2oc.write('%f\t1\t1\n'%(h2o_cue_onsets[t]))
            f_h2oc.close()
            
            f_h2ot=open(mydict['h2o_taste'], 'w')
            for t in range(len(h2o_taste_onset)):
                f_h2ot.write('%f\t6\t1\n' %(h2o_taste_onset[t]))
            f_h2ot.close()
            
            f_neu=open(mydict['neu'], 'w')
            for t in range(len(neu_onsets)):
                f_neu.write('%f\t3\t1\n' %(neu_onsets[t]))
            f_neu.close()

        except KeyError:
            pass                                                         