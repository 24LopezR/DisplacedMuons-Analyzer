import ROOT as r
import os
from math import pi
import numpy as np
from argparse import ArgumentParser
from include.PlotHandler import PlotHandler
import include.drawUtils as draw
from include.Launcher import Launcher

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
    args = parser.parse_args()
    
    # Directory where samples are stored 
    _filedir = '/eos/user/r/rlopezru/Cosmics/NoBPTX/CosmicsAnalysis_Run2022C/230131_152319/0000/'
    collections = ['dsa', 'dgl']
      
    launch = Launcher(_filedir, args.tag, collections, args.cuts_filename)
    launch.launchJobs() 
