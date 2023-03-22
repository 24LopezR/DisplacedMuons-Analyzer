import ROOT as r
import os
from argparse import ArgumentParser
from include.MuonPlotHandler import MuonPlotHandler
from include.TrackPlotHandler import TrackPlotHandler
from include.PlotHandler import PlotHandler
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
    parser.add_argument('-t', '--tag', dest='tag')
    args = parser.parse_args()


    # Open data file
    _file = r.TFile(args.fname)
    _tree = _file.Get("Events")
 
    with open(args.cuts_filename, 'r') as f:
        cuts_selection = ''.join(f.readlines())

    #trackPlotHandle = TrackPlotHandler(args.hfname+'_tracks.root', cuts_selection)
    #muonPlotHandle  = MuonPlotHandler(args.hfname+'_muons.root', cuts_selection)
    plotHandle  = PlotHandler(args.hfname, cuts_selection)
    for i,ev in enumerate(_tree):
        if i%1000==0: print("    - Events processed: {0}".format(str(i)))
        plotHandle.processEvent(ev)
        #muonPlotHandle.processEvent(ev)
        #if i>10000: break
    if os.path.exists(args.hfname): os.system('rm {0}'.format(args.hfname))
    plotHandle.write()
    #muonPlotHandle.write()
