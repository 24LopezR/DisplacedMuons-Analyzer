import ROOT as r
import os, json
from math import pi
import numpy as np
from argparse import ArgumentParser
import include.drawUtils as draw
from include.Launcher import Launcher
import include.cfg as cfg
from include.DTree import DTree

#r.gStyle.SetLabelFont(42)
################################# GLOBAL VARIABLES DEFINITION ####################################

runningfile = os.path.abspath(__file__)
WORKPATH = ''
for level in runningfile.split('/')[:-1]:
    WORKPATH += level
    WORKPATH += '/'
EOSPATH = '/eos/user/r/rlopezru/DisplacedMuons-Analyzer_out/Analyzer/'

# Read dat file
datFile = WORKPATH + 'dat/Samples_Spring23.json'
dat = json.load(open(datFile,'r'))

# Select datasets to process
datasets = []
#datasets.append('Cosmics_2022C')
datasets.append('HTo2LongLived_400_150_4000')
datasets.append('HTo2LongLived_125_20_1300')
datasets.append('HTo2LongLived_125_20_130')
datasets.append('HTo2LongLived_125_20_13')

if __name__ == '__main__':

    r.gROOT.ProcessLine('.L ./include/tdrstyle.C')
    r.gROOT.SetBatch(1)
    print('WORKPATH: ' + WORKPATH)
    print('EOSPATH: ' + EOSPATH)

    r.gStyle.SetPaintTextFormat("3.2f")
    parser = ArgumentParser()
    parser.add_argument('-c', '--cuts', dest='cuts_filename')
    parser.add_argument('-t', '--tag', dest='tag')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true')
    parser.add_argument('-q', '--queue', dest='condor', action= 'store_true')
    args = parser.parse_args()
   
    gTag = args.tag
    cuts_filename = WORKPATH + args.cuts_filename
 
    # Set debugging mode
    with open(WORKPATH+'include/cfg.py','w') as f:
        f.write('DEBUG = {0}'.format(args.debug))

    # Trees
    trees_originalFilter = []
    trees_originalFilter.append(DTree('HTo2LongLived_400_150_4000','H #rightarrow SS (400,150,4000)', dat['HTo2LongLived_400_150_4000']['MiniAOD-Ntuples'], gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_1300', 'H #rightarrow SS (125,20,1300)',  dat['HTo2LongLived_125_20_1300']['MiniAOD-Ntuples'],  gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_130',  'H #rightarrow SS (125,20,130)',   dat['HTo2LongLived_125_20_130']['MiniAOD-Ntuples'],   gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_13',   'H #rightarrow SS (125,20,13)',    dat['HTo2LongLived_125_20_13']['MiniAOD-Ntuples'],    gTag, isData = False))

    trees_nsegmentsFilter = []
    trees_nsegmentsFilter.append(DTree('HTo2LongLived_400_150_4000_nseg2','H #rightarrow SS (400,150,4000)', dat['HTo2LongLived_400_150_4000']['MiniAOD-Ntuples_nsegments2'], gTag, isData = False))
    trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_1300_nseg2', 'H #rightarrow SS (125,20,1300)',  dat['HTo2LongLived_125_20_1300']['MiniAOD-Ntuples_nsegments2'],  gTag, isData = False))
    trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_130_nseg2',  'H #rightarrow SS (125,20,130)',   dat['HTo2LongLived_125_20_130']['MiniAOD-Ntuples_nsegments2'],   gTag, isData = False))
    trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_13_nseg2',   'H #rightarrow SS (125,20,13)',    dat['HTo2LongLived_125_20_13']['MiniAOD-Ntuples_nsegments2'],    gTag, isData = False))
    
    # Empty condor folder
    if args.condor:
        os.system('rm {0}/condor/{1}/*'.format(WORKPATH, args.tag))

    # Launch jobs
    for dtree in trees_originalFilter:
        if args.condor:
            dtree.launchJobs(cuts_filename)
        else:
            dtree.loop(cuts_filename)

    for dtree in trees_nsegmentsFilter:
        if args.condor:
            dtree.launchJobs(cuts_filename)
        else:
            dtree.loop(cuts_filename)
