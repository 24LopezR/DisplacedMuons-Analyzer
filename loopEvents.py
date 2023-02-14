import ROOT as r
import os
from argparse import ArgumentParser
from include.PlotHandler import PlotHandler

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
 
    collections = ['dsa', 'dgl']
    with open(args.cuts_filename, 'r') as f:
        cuts_selection = ''.join(f.readlines())

    pltHandle = PlotHandler(args.hfname, collections, cuts_selection)
    for i,ev in enumerate(_tree):
        if i%100000==0: print("Events processed: {0}".format(str(i)))
        pltHandle.processEvent(ev)
    pltHandle.write()
