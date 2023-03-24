import ROOT as r
import os
from argparse import ArgumentParser
from include.MuonPlotHandler import MuonPlotHandler
from include.TrackPlotHandler import TrackPlotHandler
from include.MCSignalPlotHandler import MCSignalPlotHandler
from include.CosmicsPlotHandler import CosmicsPlotHandler
from include.Debugger import Debugger
import include.cfg as cfg

# Config debugger
debug = Debugger(cfg.DEBUG)
'''
Script that loops over the events of a given ntuple
'''
if __name__ == '__main__':
    
    parser = ArgumentParser()
    parser.add_argument('-i', '--filename', dest='fname') # name of file containing the Ntuple
    parser.add_argument('-o', '--histfilename', dest='hfname') # name of the output file with the hists
    parser.add_argument('-c', '--cuts', dest='cuts_filename')
    parser.add_argument('-n', '--name', dest='name')
    args = parser.parse_args()
    ### Read args
    inputFileName = args.fname
    outHistsFileName = args.hfname
    cutsFilePath = args.cuts_filename
    sampleName = args.name

    ### Open data file
    _file = r.TFile(inputFileName)
    _tree = _file.Get("Events")

    ### Define Plot Handler
    if 'HTo2LL' in sampleName:
        plotHandle  = MCSignalPlotHandler(outHistsFileName, cutsFilePath, sampleName)
    if 'Cosmics' in sampleName:
        plotHandle  = CosmicsPlotHandler(outHistsFileName, cutsFilePath, sampleName)
    
    ### Process events
    for i,ev in enumerate(_tree):
        if i%1000==0: print("    - Events processed: {0}".format(str(i)))
        plotHandle.processEvent(ev)
     
    ### Write out to file
    if os.path.exists(outHistsFileName): os.system('rm {0}'.format(outHistsFileName))
    plotHandle.write()
