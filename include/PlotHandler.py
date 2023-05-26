import math
import os, json
import ROOT as r
import numpy as np
from include.Debugger import Debugger
from include.utils import passIDSelection, angle
from include.DisplacedMuonFilter import DisplacedMuonFilter
import include.cfg as cfg

# Config debugger
debug = Debugger(cfg.DEBUG)

class PlotHandler:


    def __init__(self, histfilename, cutsFilePath, sampleName):    
        self.filename = histfilename
        self.cutsFilePath = cutsFilePath
        self.sampleName = sampleName
        self.mfilter = DisplacedMuonFilter()

    def processEvent(self, ev):
        return


    def readCuts(self):
        with open(self.cutsFilePath, 'r') as f:
            ##### Define cuts of the analysis
            self.triggers = []
            self.cuts = {}
            cutsData = json.load(f)
        key = self.sampleName.replace('_nseg2','')
        sampleData = cutsData[key]
        ### Set the triggers
        for trigger in sampleData['triggers']:
            self.triggers.append("ev.{0} == True".format(trigger))
        ### Set the cuts in the variables for each collection
        for collection in self.collections:
            self.cuts[collection] = []
            if 'dmu' not in collection: cuts = sampleData['tracks']
            else: cuts = sampleData['muons']
            for cut in cuts:
                if 'ID' in cut: self.cuts[collection].append("ID")
                else: self.cuts[collection].append("ev.{0}_{1}[n]{2}{3}".format(*([collection]+cut.split(' '))))
        ### Print the cuts
        print(20*'#' + ' SELECTION ' + 20*'#')
        print('>> Triggers:       ' + str(self.triggers))
        print('>> Selection cuts:')
        for collection in self.collections:
            print('    - {0}: {1}'.format(collection, self.cuts[collection]))
        print(51*'#')


    def count_muons(self, ev):
        # Count number of muons that are dsa and dgl
        ndsa_ids = []
        ndgl_ids = []
        #nmuons = [0,0]
        #nmuons_up   = [0,0]
        #nmuons_down = [0,0]
        for n in range(ev.ndmu):
            if ev.dmu_isDSA[n]:
                ndsa_ids.append(n)
                #nmuons[0] += 1
                #if ev.dmu_dsa_phi[n]<0: nmuons_down[0] += 1
                #else: nmuons_up[0] += 1
            if ev.dmu_isDGL[n]:
                ndgl_ids.append(n)
                #nmuons[1] += 1
                #if ev.dmu_dgl_phi[n]<0: nmuons_down[1] += 1
                #else: nmuons_up[1] += 1
        #for i,col in enumerate(self.collections[2:4]):
            #self.h_nmuons[col].Fill(nmuons[i])
            #self.h_nmuons_up[col].Fill(nmuons_up[i])
            #self.h_nmuons_down[col].Fill(nmuons_down[i])
        return ndsa_ids, ndgl_ids


    '''
    Function to apply DisplacedMuonFilter. It fills a histogram telling, in case of returning False,
    in which stage of the filter the muon was dropped.
    Args:
        - ev               : event
        - n                : id of muon in event
        - toApply = [x,x,x]: indicates with 1 and 0 if each stage of the filter is applied
    '''
    def passMuonFilter(self, ev, n, toApply=[1,1,1]):
        if ev.dmu_isDSA[n]:
            if ev.dmu_isDGL[n] or ev.dmu_isDTK[n]:
                if toApply[0] and not self.mfilter.layerOneFilter(ev, n):
                    #self.h_muons_filter.Fill(0)
                    debug.print("Muon lost at layer 1 of filter", "INFO")
                    return False
            else:
                if toApply[1] and not self.mfilter.layerTwoFilter(ev, n): 
                    #self.h_muons_filter.Fill(1)
                    debug.print("Muon lost at layer 2 of filter", "INFO")
                    return False
        else:
            if ev.dmu_isDGL[n] or ev.dmu_isDTK[n]:
                if toApply[2] and not self.mfilter.layerThreeFilter(ev, n): 
                    #self.h_muons_filter.Fill(2)
                    debug.print("Muon lost at layer 3 of filter", "INFO")
                    return False
            else: 
                debug.print("Muon that has not standalone nor tracker track.", "WARNING")
                return False
        return True


    def passDSAID(self, ev, n, collection):
        nCSChits = eval('ev.{0}_nValidMuonCSCHits[n]'.format(collection))
        nDThits = eval('ev.{0}_nValidMuonDTHits[n]'.format(collection))
        if nCSChits + nDThits <= 12: return False
        if nCSChits == 0 and nDThits <= 18: return False
        normChi2 = eval('ev.{0}_normalizedChi2[n]'.format(collection))
        if normChi2 >= 2.5: return False
        ptRelError = eval('ev.{0}_ptError[n]/ev.{0}_pt[n]'.format(collection))
        if ptRelError >= 1: return False
        return True


    def write(self):
        output = r.TFile(self.filename, "RECREATE")
        for attr, value in self.__dict__.items():
            if attr[0] == 'h' and type(value) == dict:
                for key in value.keys():
                    value[key].Write()
                    debug.print(value[key].GetName()+" written to "+self.filename, "SUCCESS")
        output.Close()
