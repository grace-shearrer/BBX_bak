#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 10:46:43 2018
Updated on Wed Dec 12 13:27 2019
@author: gracer
This is a script to parse the onset files from psychopy to FSL readable format. There is an additonal option to create a "sanity check" plot to ensure it is working.
"""
import os
import glob
import pdb
import argparse
import pandas as pd

def plottin(df, arglist):
    import matplotlib
    # matplotlib.use("Qt5Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    dates = df['onsets']
    names = df['metric']
    # Choose some nice levels
    levels = np.tile([-5, 5, -3, 3, -1, 1],
                     int(np.ceil(len(dates)/6)))[:len(dates)]

    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(25, 4), constrained_layout=True)
    ax.set(title="Matplotlib release dates")

    markerline, stemline, baseline = ax.stem(dates, levels,
                                             linefmt="C3-", basefmt="k-",
                                             use_line_collection=True)

    plt.setp(markerline, mec="k", mfc="w", zorder=3)

    # Shift the markers to the baseline by replacing the y-data by zeros.
    markerline.set_ydata(np.zeros(len(dates)))

    # annotate lines
    vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
    for d, l, r, va in zip(dates, levels, names, vert):
        ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),textcoords="offset points",
                     va=va, ha="center")

    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    # remove y axis and spines
    ax.get_yaxis().set_visible(False)
    for spine in ["left", "top", "right"]:
        ax.spines[spine].set_visible(False)

    ax.margins(y=0.1)
    # plt.show()
    plt.savefig(os.path.join(arglist['OUTPATH'],'%s_%s.png'%(arglist['sub'],arglist['run'])))




def parsely(arglist):
    # print(arglist)
    ignore = ['DATA 	Keypress: o']
    handles=[]

    for file in glob.glob(os.path.join(arglist['BASEPATH'],'bbx*%s*.log'%(arglist['WAVE']))):
        print(file)
        #define all the strings
        fi=file.split('/')[-1]
        sub=fi.split('_')[1]
        run=file.split('_')[2].split('0')[-1]
        session=arglist['WAVE']
        arglist.update({'sub':sub})
        arglist.update({'run':run})
        print('this is the subject %s\nthis is the run %s'%(sub,run))

        with open(file,'r') as infile:
            cue_onsets=[]
            cues=[]
            taste_onsets=[]
            tastes=[]
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
                        # print(l_s)
                        cue_onsets.append(float(l_s[0]))
                    if x.find('Level image')>-1:
                        l_s=x.strip().split()
                        # print(l_s)
                        cues.append(l_s[2])
                    if x.find('Level post injecting via pump at address ')>-1:
                        l_s=x.strip().split()
                        # print(l_s)
                        taste_onsets.append(l_s[0])
                        tastes.append(l_s[8])
                    if x.find('Level RINSE 	25')>-1:
                        rinse.append(l_s[0])
        print("got the arrays time to adjust onsets")
        check_dict={}
        columnTitles = ['onsets', 'duration', 'metric']
        # CUES
        cue_df = pd.DataFrame(
            {'onsets': cue_onsets,
             'metric': cues
            })
        cue_df['duration']='1'
        cue_df = cue_df.reindex(columns=columnTitles)
        cue_df['onsets']=cue_df['onsets']-start_time
        ## make individual dataframes
        ### H2O cue
        H2Ocue_df=cue_df.loc[cue_df['metric'] == 'image=water.jpg']
        x=cue_df.loc[cue_df['metric'] == 'image=water.jpg'] #this is just for the dict and I don't know why
        #### check dataframe
        check_dict.update({'H2Ocue':x})
        ####################
        H2Ocue_df['metric'].replace({'image=water.jpg': 1}, inplace=True)
        H2Ocue_df.to_csv(os.path.join(arglist['OUTPATH'],'%s'%session,'sub-%s_task-H2Ocue-run-%s.tsv'%(sub,run)), header=False, index=False, sep='\t')
        ### SSB cue
        SSBcue = ['image=CO.jpg','image=SL.jpg']
        SSBcue_df=cue_df.loc[(cue_df['metric'] == SSBcue[0]) | (cue_df['metric'] == SSBcue[1])]
        #### check dataframe
        y=cue_df.loc[(cue_df['metric'] == SSBcue[0]) | (cue_df['metric'] == SSBcue[1])]
        check_dict.update({'SSBcue':y})
        ####################
        SSBcue_df['metric'].replace({SSBcue[0]: 1, SSBcue[1]: 1}, inplace=True)
        SSBcue_df.to_csv(os.path.join(arglist['OUTPATH'],'%s'%session,'sub-%s_task-SSBcue-run-%s.tsv'%(sub,run)), header=False, index=False, sep='\t')
        ### USB cue
        USBcue = ['image=UCO.jpg','image=USL.jpg']
        USBcue_df=cue_df.loc[(cue_df['metric'] == USBcue[0]) | (cue_df['metric'] == USBcue[1])]
        #### check dataframe
        z=cue_df.loc[(cue_df['metric'] == USBcue[0]) | (cue_df['metric'] == USBcue[1])]
        check_dict.update({'USBcue':z})
        ###################
        USBcue_df['metric'].replace({USBcue[0]: 1, USBcue[1]: 1}, inplace=True)
        USBcue_df.to_csv(os.path.join(arglist['OUTPATH'],'%s'%session,'sub-%s_task-USBcue-run-%s.tsv'%(sub,run)), header=False, index=False, sep='\t')
        # TASTES
        taste_df = pd.DataFrame(
            {'onsets': taste_onsets,
             'metric':tastes
            })
        taste_df['duration']='6'
        taste_df['onsets']=taste_df['onsets'].astype('float32')-start_time
        taste_df = taste_df.reindex(columns=columnTitles)
        ## make individual dataframes
        ### H2O
        H2O_df=taste_df.loc[taste_df['metric'] == '0']
        #### check dataframe
        a=taste_df.loc[taste_df['metric'] == '0']
        check_dict.update({'H2O':a})
        ###################
        H2O_df['metric'].replace({'0': 1}, inplace=True)
        H2O_df.to_csv(os.path.join(arglist['OUTPATH'],'%s'%session,'sub-%s_task-H2O-run-%s.tsv'%(sub,run)), header=False, index=False, sep='\t')
        ## SSB
        SSB_df=taste_df.loc[taste_df['metric'] == '1']
        #### check dataframe
        b=taste_df.loc[taste_df['metric'] == '1']
        check_dict.update({'SSB':b})
        ####################
        SSB_df['metric'].replace({'1': 1}, inplace=True)
        SSB_df.to_csv(os.path.join(arglist['OUTPATH'],'%s'%session,'sub-%s_task-SSB-run-%s.tsv'%(sub,run)), header=False, index=False, sep='\t')
        ## USB
        USB_df=taste_df.loc[taste_df['metric'] == '2']
        #### check dataframe
        c=taste_df.loc[taste_df['metric'] == '2']
        check_dict.update({'USB':c})
        ####################
        USB_df['metric'].replace({'2': 1}, inplace=True)
        USB_df.to_csv(os.path.join(arglist['OUTPATH'],'%s'%session,'sub-%s_task-USB-run-%s.tsv'%(sub,run)), header=False, index=False, sep='\t')
        ## RINSE
        rinse_df = pd.DataFrame(
            {'onsets': rinse
            })
        rinse_df['onsets']=rinse_df['onsets'].astype('float32')-start_time
        rinse_df['duration']=3
        check_dict.update({'rinse':rinse_df})
        rinse_df['metric']=1
        rinse_df.to_csv(os.path.join(arglist['OUTPATH'],'%s'%session,'sub-%s_task-rinse-run-%s.tsv'%(sub,run)), header=False, index=False, sep='\t')

        check_dict['rinse']['metric']='rinse'
        DF=pd.concat(check_dict.values()).sort_values('onsets')
        DF.to_csv(os.path.join(arglist['OUTPATH'],'%s'%session,'sub-%s_task-ALL-run-%s.csv'%(sub,run)))
        if arglist['PLOT'] == True:
            plottin(DF, arglist)



def main():
    parser=argparse.ArgumentParser(description='Generate FSL style onset files from logfile')

    parser.add_argument('-basepath', dest='BASEPATH', action='store',
                        default=False, help='Where dem files at boo?')
    parser.add_argument('-wave',dest='WAVE', action='store',
                        default=False, help='Waves don die, which we using?')
    parser.add_argument('-outpath', dest='OUTPATH', action='store',
                        default=False, help='Where to save these toasty toasts')
    parser.add_argument('-plot', dest='PLOT', action='store',
                        default=False, help='You want a plot?')

    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]
    parsely(arglist)
main()
