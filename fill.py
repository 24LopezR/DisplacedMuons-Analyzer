import ROOT as r
import os
from math import pi
import numpy as np
from argparse import ArgumentParser
import include.drawUtils as draw
from include.Launcher import Launcher
import include.cfg as cfg

#r.gStyle.SetLabelFont(42)
################################# GLOBAL VARIABLES DEFINITION ####################################

runningfile = os.path.abspath(__file__)
WORKPATH = ''
for level in runningfile.split('/')[:-1]:
    WORKPATH += level
    WORKPATH += '/'
EOSPATH = '/eos/user/r/rlopezru/Cosmics-Analyzer_out/Analyzer/'


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
    
    # Set debugging mode
    with open(WORKPATH+'include/cfg.py','w') as f:
        f.write('DEBUG = {0}'.format(args.debug))

    # Directory where samples are stored 
    _filedir_MiniAOD = '/eos/user/r/rlopezru/Samples/NoBPTX/CosmicsAnalysis_Run2022C_MiniAOD-Ntuples/230421_160633/0000/'
    _filedir_AOD = '/eos/user/r/rlopezru/Samples/NoBPTX/CosmicsAnalysis_Run2022C_AOD-Ntuples/230421_130233/0000/'
    #_filedir = '/eos/user/r/rlopezru/HTo2LongLivedTo2mu2jets_MH-400_MFF-150_CTau-4000mm_TuneCP5_13p6TeV_pythia8/HTo2LongLivedTo2mu2jets_MH-400_MFF-150_CTau-4000mm_displacedFilter_fromAOD/230310_122743/0000/'
    #_filedir = '/eos/user/r/rlopezru/Cosmics/NoBPTX/CosmicsAnalysis_Run2022C/230310_122707/0000/'
    launch = Launcher(_filedir_AOD, args.tag, args.cuts_filename)
    if args.condor:
        launch.launchJobs()
    else:
        launch.loop()
