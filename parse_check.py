#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 10:46:43 2018
Updated on Wed Dec 12 13:27 2019
@author: gracer
"""

#!/usr/bin/python
#get onsets


import numpy
import os
import glob
import pdb
import argparse
import pandas as pd
def parsely(arglist):
    # print(arglist)
    ignore = ['DATA 	Keypress: o']
    handles=[]

    for file in glob.glob(os.path.join(arglist['BASEPATH'],'bbx*%s*.log'%(arglist['WAVE']))):
        print(file)
        #define all the strings
        fi=file.split('/')[-1]
        sub=fi.split('_')[1]
        run=file.split('_')[2]
        session=arglist['WAVE']
        print('this is the subject %s\nthis is the run %s'%(sub,run))

        with open(file,'r') as infile:
            cue_onsets=[]
            cues=[]
            taste_onsets=[]
            tastes=[]
            SSB_taste_onset=[]
            USB_taste_onset=[]
            H2O_taste_onset=[]
            SSB_cue_onsets=[]
            SSB_cue=[]
            USB_cue_onsets=[]
            USB_cue=[]
            H2O_cue_onsets=[]
            H2O_cue=[]
            rinse=[]
            start_time=None
            # create 4 arrays with the cue onsets, taste onsets, cues, tastes
            for x in infile.readlines():
                if not x.find(ignore[0])>-1:
                    l_s=x.strip().split()
                    if x.find('Level start key press')>-1:#find the start
                        l_s=x.strip().split()
                        start_time=float(l_s[0])
                        print(start_time)
                    if x.find('Level onset of trial')>-1:
                        l_s=x.strip().split()
                        print(l_s)
                        cue_onsets.append(float(l_s[0]))
                    if x.find('Level image')>-1:
                        l_s=x.strip().split()
                        print(l_s)
                        cues.append(l_s[2])
                    if x.find('Level post injecting via pump at address ')>-1:
                        l_s=x.strip().split()
                        print(l_s)
                        taste_onsets.append(l_s[0])
                        tastes.append(l_s[8])
                    if x.find('Level RINSE 	25')>-1:
                        rinse.append(l_s[0])
        print("got the arrays time to adjust onsets")
        columnTitles = ['onsets', 'duration', 'metric']
        # CUES
        cue_df = pd.DataFrame(
            {'onsets': cue_onsets,
             'metric': cues
            })
        cue_df['duration']='1'
        cue_df = cue_df.reindex(columns=columnTitles)
        cue_df['onsets']=cue_df['onsets']-start_time
        H2O_df=cue_df.loc[cue_df['metric'] == 'image=water.jpg']
        SSBcue = ['image=CO.jpg','image=SL.jpg']
        SSBcue_df=cue_df.loc[(cue_df['metric'] == SSBcue[0]) | (cue_df['metric'] == SSBcue[1])]
        USBcue = ['image=UCO.jpg','image=USL.jpg']
        USBcue_df=cue_df.loc[(cue_df['metric'] == USBcue[0]) | (cue_df['metric'] == USBcue[1])]
        # TASTES
        taste_df = pd.DataFrame(
            {'onsets': taste_onsets,
             'metric':tastes
            })
        taste_df['duration']='6'
        taste_df['onsets']=taste_df['onsets'].astype('float32')-start_time
        taste_df = taste_df.reindex(columns=columnTitles)
        H2O_df=taste_df.loc[taste_df['metric'] == '0']
        SSB_df=taste_df.loc[taste_df['metric'] == '1']
        USB_df=taste_df.loc[taste_df['metric'] == '2']
        # RINSE
        rinse_df = pd.DataFrame(
            {'onsets': rinse
            })
        rinse_df['duration']=3
        rinse_df['metric']=1


        pdb.set_trace()


def main():
    parser=argparse.ArgumentParser(description='Generate FSL style onset files from logfile')

    parser.add_argument('-basepath', dest='BASEPATH', action='store',
                        default=False, help='Where dem files at boo?')
    parser.add_argument('-wave',dest='WAVE', action='store',
                        default=False, help='Waves don die, which we using?')
    parser.add_argument('-outpath', dest='OUTPATH', action='store',
                        default=False, help='Where to save these toasty toasts')

    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]
    parsely(arglist)
main()
"""
        r_onsets=(numpy.asarray(rinse,dtype=float))-start_time
        TT_onsets=(numpy.asarray(TT_onset,dtype=float))-start_time
        UU_onsets=(numpy.asarray(UU_onset,dtype=float))-start_time
        NN_onsets=(numpy.asarray(NN_onset,dtype=float))-start_time

        Tcue_onsets=(numpy.asarray(tasty_cue_onsets,dtype=float))-start_time
        Ucue_onsets=(numpy.asarray(nottasty_cue_onsets,dtype=float))-start_time
        Ncue_onsets=(numpy.asarray(neu_cue_onsets,dtype=float))-start_time

        files2make=['rinse','TT','UU','NN','Tcue','Ucue','Ncue']
        mydict={}
        try:
            for files in files2make:
                path='/Users/gracer/Desktop/Output/test/%s_%s_%s_%s.txt'%(sub,session,files,run)
                if os.path.exists(path) == True:
                    print ('exists')
                    break
                else:
                    mydict[files] = path
            f_rinse=open(mydict['rinse'], 'w')
            for t in range(len(r_onsets)):
                f_rinse.write('%f\t3\t1\n'%(r_onsets[t]))
            f_rinse.close()

            f_TT=open(mydict['TT'], 'w')
            for t in range(len(TT_onsets)):
                f_TT.write('%f\t6\t1\n' %(TT_onsets[t]))
            f_TT.close()

            f_Tcue=open(mydict['Tcue'], 'w')
            for t in range(len(Tcue_onsets)):
                f_Tcue.write('%f\t1\t1\n' %(Tcue_onsets[t]))
            f_Tcue.close()

            f_UU=open(mydict['UU'], 'w')
            for t in range(len(UU_onsets)):
                f_UU.write('%f\t6\t1\n' %UU_onsets[t])
            f_UU.close()

            f_Ucue=open(mydict['Ucue'], 'w')
            for t in range(len(Ucue_onsets)):
                f_Ucue.write('%f\t1\t1\n' %(Ucue_onsets[t]))
            f_Ucue.close()

            f_NN=open(mydict['NN'], 'w')
            for t in range(len(NN_onsets)):
                f_NN.write('%f\t6\t1\n' %NN_onsets[t])
            f_NN.close()

            f_Ncue=open(mydict['Ncue'], 'w')
            for t in range(len(Ncue_onsets)):
                f_Ncue.write('%f\t1\t1\n' %(Ncue_onsets[t]))
            f_Ncue.close()

        except KeyError:
            pass
"""
