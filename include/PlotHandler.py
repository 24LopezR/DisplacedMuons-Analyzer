import math
import os
import ROOT as r
import numpy as np

from include.utils import passIDSelection, findProbe


class PlotHandler:


    def __init__(self, outdir, histfilename, collections, cuts_selection):    
        self.outdir = outdir
        if self.outdir[-1] != '/': self.outdir = self.outdir + '/'
        self.filename = self.outdir + histfilename
        #self.sampledir = sampledir

        self.h_nmuons = {}
        self.h_nmuons_down = {}
        self.h_nmuons_up = {}
        self.h_pt = {}
        self.h_eta = {}
        self.h_phi = {}
        self.h_dxy = {}
        self.h_dz = {}
        self.h_Nhits = {}
        self.h_NDThits = {}
        self.h_normalizedChi2 = {}
        
        self.h_cosalpha = {}
        self.h_dPhi = {}
        self.h_dEta = {}

        self.h_eff_pt = {}
        self.h_eff_eta = {}
        self.h_eff_dxy = {}
        self.h_eff_dz = {}
        self.h_eff_2D = {}

        self.collections = collections
        for collection in self.collections:
            self.h_nmuons[collection]        = r.TH1F("h_muons_{0}".format(collection),r";Nmu;N events",6,0,6) 
            self.h_nmuons_down[collection]   = r.TH1F("h_muons_down_{0}".format(collection),r";Nmu(#phi<0);N events",6,0,6) 
            self.h_nmuons_up[collection]     = r.TH1F("h_muons_up_{0}".format(collection),r";Nmu(#phi>0);N events",6,0,6) 
            self.h_pt[collection]        = r.TH1F("h_pt_{0}".format(collection),r";pT;N events",100,0,200)
            self.h_eta[collection]       = r.TH1F("h_eta_{0}".format(collection),r";#eta;N events",100,-0.9,0.9)
            self.h_phi[collection]       = r.TH1F("h_phi_{0}".format(collection),r";#phi;N events",100,-3.2,3.2)
            self.h_dxy[collection]       = r.TH1F("h_dxy_{0}".format(collection),r";|dxy|;N events",100,0,800)
            self.h_dz[collection]        = r.TH1F("h_dz_{0}".format(collection),r";|dz|;N events",100,0,800)
            self.h_Nhits[collection]     = r.TH1F("h_Nhits_{0}".format(collection),r";nValidMuonHits;N events",100,0,50)
            self.h_NDThits[collection]   = r.TH1F("h_NDThits_{0}".format(collection),r";nValidMuonDTHits;N events",100,0,50)
            self.h_normalizedChi2[collection]     = r.TH1F("h_normalizedChi2_{0}".format(collection),r";#chi^2/ndof;N events",100,0,5)

            self.h_cosalpha[collection]  = r.TH1F("h_cosalpha_{0}".format(collection),r";cos(#alpha);N events",100,-1,1)
            self.h_dPhi[collection]      = r.TH1F("h_dPhi_{0}".format(collection),r";|#Delta#phi|;N events",100,0,3.2)
            self.h_dEta[collection]      = r.TH1F("h_dEta_{0}".format(collection),r";#Delta#eta;N events",100,-2.4,2.4)

            self.h_eff_pt[collection]    = r.TEfficiency("h_eff_pt_{0}".format(collection), "Efficiency cosmic muons;p_{T} (GeV);#epsilon",    90,0,90)
            self.h_eff_eta[collection]   = r.TEfficiency("h_eff_eta_{0}".format(collection),"Efficiency cosmic muons;#eta;#epsilon",100,-1.2,1.2)
            self.h_eff_dxy[collection]   = r.TEfficiency("h_eff_dxy_{0}".format(collection),"Efficiency cosmic muons;|d_{xy}| (cm);#epsilon",   50,0,200)
            self.h_eff_dz[collection]    = r.TEfficiency("h_eff_dz_{0}".format(collection), "Efficiency cosmic muons;|d_{z}| (cm);#epsilon",    50,0,200)
            self.h_eff_2D[collection]    = r.TEfficiency("h_eff_2D_{0}".format(collection), "Efficiency cosmic muons;|d_{xy}| (cm);|d_{z}| (cm);#epsilon",10,0,80,20,0,160)
        
        ##### Define cuts of the analysis
        self.cuts = {}
        for collection in self.collections:
            self.cuts[collection] = cuts_selection.format(collection)


    def fillVariableHistograms(self, ev, n, collection, cos_alpha=None):        
        self.h_pt[collection].Fill(eval('ev.{0}_pt[n]'.format(collection)))
        self.h_eta[collection].Fill(eval('ev.{0}_eta[n]'.format(collection)))
        self.h_phi[collection].Fill(eval('ev.{0}_phi[n]'.format(collection)))
        self.h_dxy[collection].Fill(eval('ev.{0}_dxy[n]'.format(collection)))
        self.h_dz[collection].Fill(eval('ev.{0}_dz[n]'.format(collection)))
        self.h_Nhits[collection].Fill(eval('ev.{0}_nValidMuonHits[n]'.format(collection)))
        self.h_NDThits[collection].Fill(eval('ev.{0}_nValidMuonDTHits[n]'.format(collection)))
        self.h_normalizedChi2[collection].Fill(eval('ev.{0}_normalizedChi2[n]'.format(collection)))


    def fillDimuonVariableHistograms(self, ev, n, i, cos_alpha, collection):
        self.h_cosalpha[collection].Fill(cos_alpha)
        self.h_dPhi[collection].Fill(eval('abs(ev.{0}_phi[n]-ev.{0}_phi[i])'.format(collection)))
        self.h_dEta[collection].Fill(eval('ev.{0}_eta[n]-ev.{0}_eta[i]'.format(collection)))


    def fillEfficiencyHistograms(self, ev, n, collection, hasProbe=False):
        self.h_eff_pt[collection].Fill(hasProbe, eval('ev.{0}_pt[n]'.format(collection)))
        self.h_eff_eta[collection].Fill(hasProbe, eval('ev.{0}_eta[n]'.format(collection)))
        self.h_eff_dxy[collection].Fill(hasProbe, eval('abs(ev.{0}_dxy[n])'.format(collection)))
        self.h_eff_dz[collection].Fill(hasProbe, eval('abs(ev.{0}_dz[n])'.format(collection)))
        self.h_eff_2D[collection].Fill(hasProbe, eval('abs(ev.{0}_dxy[n])'.format(collection)), eval('abs(ev.{0}_dz[n])'.format(collection)))


    def processEvent(self, ev):
        for collection in self.collections:
            if eval('ev.n{0}'.format(collection)) < 1: continue
            n_up, n_down = 0,0
            for n in range(eval('ev.n{0}'.format(collection))):
                if eval('ev.{0}_phi[n]'.format(collection)) < 0: n_down += 1
                else: n_up += 1 
            for n in range(eval('ev.n{0}'.format(collection))):
                ## Apply cuts
                if np.prod(eval(self.cuts[collection])):
                    
                    ## Check if muon passes ID selection
                    passID = passIDSelection(ev, n, col=collection)
                    cos_alpha_temp = None
                    if passID:
                        self.fillVariableHistograms(ev, n, collection)
                        hasProbe, cos_alpha_temp, i = findProbe(ev, n, print_out=False, col=collection)
                        self.fillEfficiencyHistograms(ev, n, collection, hasProbe)
                        if hasProbe: self.fillDimuonVariableHistograms(ev, n, i, cos_alpha_temp, collection)
                        break
                    
                    self.h_nmuons[collection].Fill(eval('ev.n{0}'.format(collection)))   
                    self.h_nmuons_down[collection].Fill(n_down)
                    self.h_nmuons_up[collection].Fill(n_up)


    def write(self):        
        output = r.TFile(self.filename, 'RECREATE')
        for attr, value in self.__dict__.items():
            if attr[0] == 'h' and type(value) == dict:
                for key in value.keys():
                    value[key].Write()
        output.Close()
