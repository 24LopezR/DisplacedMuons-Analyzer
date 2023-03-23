import math
import os
import ROOT as r
import numpy as np
from include.Debugger import Debugger
from include.utils import passIDSelection, angle
from include.DisplacedMuonFilter import DisplacedMuonFilter
import include.cfg as cfg

# Config debugger
debug = Debugger(cfg.DEBUG)

class MCSignalPlotHandler:


    def __init__(self, histfilename, cuts_selection):    
        self.filename = histfilename

        ## MuonFilter object
        #self.mfilter = DisplacedMuonFilter(3.5, 3.5, 0)
        
        ## Define histograms
        self.h_nmuons = {}
        self.h_nmuons_down = {}
        self.h_nmuons_up = {}
        self.h_pt = {}
        self.h_pt_100 = {}
        self.h_eta = {}
        self.h_eta_down = {}
        self.h_eta_up = {}
        self.h_phi = {}
        self.h_dxy = {}
        self.h_dz = {}
        self.h_Nhits = {}
        self.h_NDThits = {}
        self.h_normalizedChi2 = {}
        self.h_numberOfMatches = {}
        
        self.h_charge_pt = {}
        self.h_cosalpha = {}
        self.h_dPhi = {}
        self.h_dEta = {}
        self.h_eff_pt = {}
        self.h_eff_eta = {}
        self.h_eff_Lxy = {}
        self.h_eff_Lxy_cutdz = {}
        self.h_eff_dz = {}
        self.h_eff_dz_cutdxy = {}
        self.h_eff_2D = {}
        self.h_dxy_dz_2D = {}

        self.collections = ['dsa', 'dgl', 'dmu_dsa','dmu_dgl']
        for collection in self.collections:
            self.h_nmuons[collection]          = r.TH1F("h_muons_{0}".format(collection),r";N_{#mu};N events",6,0,6) 
            self.h_nmuons_down[collection]     = r.TH1F("h_muons_down_{0}".format(collection),r";N_{#mu}(#phi<0);N events",6,0,6) 
            self.h_nmuons_up[collection]       = r.TH1F("h_muons_up_{0}".format(collection),r";N_{#mu}(#phi>0);N events",6,0,6) 
            self.h_pt[collection]              = r.TH1F("h_pt_{0}".format(collection),r";p_{T} (GeV);N events",100,0,200)
            self.h_pt_100[collection]          = r.TH1F("h_pt_100_{0}".format(collection),r";p_{T} (GeV);N events",100,0,100)
            self.h_eta[collection]             = r.TH1F("h_eta_{0}".format(collection),r";#eta;N events",100,-0.9,0.9)
            self.h_eta_down[collection]        = r.TH1F("h_eta_down_{0}".format(collection),r";#eta;N events",100,-0.9,0.9)
            self.h_eta_up[collection]          = r.TH1F("h_eta_up_{0}".format(collection),r";#eta;N events",100,-0.9,0.9)
            self.h_phi[collection]             = r.TH1F("h_phi_{0}".format(collection),r";#phi;N events",100,-3.2,3.2)
            self.h_dxy[collection]             = r.TH1F("h_dxy_{0}".format(collection),r";|d_{xy}| (cm);N events",100,0,800)
            self.h_dz[collection]              = r.TH1F("h_dz_{0}".format(collection),r";|d_{z}| (cm);N events",100,0,800)
            self.h_Nhits[collection]           = r.TH1F("h_Nhits_{0}".format(collection),r";nValidMuonHits;N events",100,0,50)
            self.h_NDThits[collection]         = r.TH1F("h_NDThits_{0}".format(collection),r";nValidMuonDTHits;N events",100,0,50)
            self.h_normalizedChi2[collection]  = r.TH1F("h_normalizedChi2_{0}".format(collection),r";#chi^{2}/ndof;N events",100,0,5)
            self.h_charge_pt[collection]       = r.TH1F("h_charge_pt_{0}".format(collection),r";Q/p_{T};N events",100,-0.1,0.1)
            self.h_cosalpha[collection]        = r.TH1F("h_cosalpha_{0}".format(collection),r";cos(#alpha);N events",100,-1,1)
            self.h_dPhi[collection]            = r.TH1F("h_dPhi_{0}".format(collection),r";|#Delta#phi|;N events",100,0,3.2)
            self.h_dEta[collection]            = r.TH1F("h_dEta_{0}".format(collection),r";#Delta#eta;N events",100,-2.4,2.4)
            self.h_eff_pt[collection]          = r.TEfficiency("h_eff_pt_{0}".format(collection), "Efficiency;p_{T} (GeV);Efficiency",    90,0,90)
            self.h_eff_eta[collection]         = r.TEfficiency("h_eff_eta_{0}".format(collection),"Efficiency;#eta;Efficiency",100,-1.2,1.2)
            self.h_eff_Lxy[collection]         = r.TEfficiency("h_eff_Lxy_{0}".format(collection),"Efficiency;|L_{xy}| (cm);Efficiency", 9, 
                                                               np.array([0., 2., 5., 10., 20., 30., 40., 50., 60., 70.]))
            self.h_eff_Lxy_cutdz[collection]   = r.TEfficiency("h_eff_Lxy_cutdz_{0}".format(collection),"Efficiency;|L_{xy}| (cm);Efficiency", 9, 
                                                               np.array([0., 2., 5., 10., 20., 30., 40., 50., 60., 70.]))
            self.h_eff_dz[collection]          = r.TEfficiency("h_eff_dz_{0}".format(collection), "Efficiency;|d_{z}| (cm);Efficiency", 6, 
                                                               np.array([0., 8., 20., 40., 60., 90., 140.]))
            self.h_eff_dz_cutdxy[collection]   = r.TEfficiency("h_eff_dz_cutdxy_{0}".format(collection),"Efficiency;|d_{z}| (cm);Efficiency", 6, 
                                                               np.array([0., 8., 20., 40., 60., 90., 140.]))
            self.h_eff_2D[collection]          = r.TEfficiency("h_eff_2D_{0}".format(collection), "Efficiency;|d_{0}| (cm);|d_{z}| (cm);Efficiency",6,
                                                               np.array([0., 2., 5., 10., 30., 50., 70.]), 6,np.array([0., 8., 20., 40., 60., 90., 140.]))
            self.h_dxy_dz_2D[collection]       = r.TH2F("h_dxy_dz_2D_{0}".format(collection), "Displacement;|d_{0}| (cm);|d_{z}| (cm);N events",100,0,500,100,0,700)
        
        ##### Define cuts of the analysis
        self.cuts = {}
        for collection in self.collections:
            self.cuts[collection] = cuts_selection.format(collection)


    def fillVariableHistograms(self, ev, n, collection):
        self.h_pt[collection].Fill(eval('ev.{0}_pt[n]'.format(collection)))
        self.h_pt_100[collection].Fill(eval('ev.{0}_pt[n]'.format(collection)))
        self.h_eta[collection].Fill(eval('ev.{0}_eta[n]'.format(collection)))
        self.h_phi[collection].Fill(eval('ev.{0}_phi[n]'.format(collection)))
        self.h_dxy[collection].Fill(eval('abs(ev.{0}_dxy[n])'.format(collection)))
        ### Fill dxy filter stages plots
        #if self.passMuonFilter(ev, n, toApply=[0,1,1]): self.h_dxy_1.Fill(ev.dmu_dsa_dxy[n])
        #if self.passMuonFilter(ev, n, toApply=[1,0,1]): self.h_dxy_2.Fill(ev.dmu_dsa_dxy[n])
        #if self.passMuonFilter(ev, n, toApply=[1,1,0]): self.h_dxy_3.Fill(ev.dmu_dsa_dxy[n])
        self.h_dz[collection].Fill(eval('abs(ev.{0}_dz[n])'.format(collection)))
        self.h_Nhits[collection].Fill(eval('ev.{0}_nValidMuonHits[n]'.format(collection)))
        self.h_NDThits[collection].Fill(eval('ev.{0}_nValidMuonDTHits[n]'.format(collection)))
        self.h_normalizedChi2[collection].Fill(eval('ev.{0}_normalizedChi2[n]'.format(collection)))
        self.h_charge_pt[collection].Fill(eval('ev.{0}_charge[n]/ev.{0}_pt[n]'.format(collection)))
        self.h_dxy_dz_2D[collection].Fill(eval('abs(ev.{0}_dxy[n])'.format(collection)), eval('abs(ev.{0}_dz[n])'.format(collection))) 


    def fillDimuonVariableHistograms(self, ev, n, i, cos_alpha, collection):
        self.h_cosalpha[collection].Fill(cos_alpha)
        self.h_dPhi[collection].Fill(eval('abs(ev.{0}_phi[n]-ev.{0}_phi[i])'.format(collection)))
        self.h_dEta[collection].Fill(eval('ev.{0}_eta[n]-ev.{0}_eta[i]'.format(collection)))
        self.h_eta_down[collection].Fill(eval('ev.{0}_eta[n]'.format(collection)))
        self.h_eta_up[collection].Fill(eval('ev.{0}_eta[i]'.format(collection)))


    def fillEfficiencyHistograms(self, ev, n, collection, hasProbe=False):
        self.h_eff_pt[collection].Fill(hasProbe, ev.HardProcessParticle_pt[n])
        self.h_eff_eta[collection].Fill(hasProbe, ev.HardProcessParticle_eta[n])
        self.h_eff_Lxy[collection].Fill(hasProbe, abs(self.Lxy_value(ev,n)))
        #if abs(ev.HardProcessParticle_dz[n]) < 8: self.h_eff_Lxy_cutdz[collection].Fill(hasProbe, abs(Lxy_value(ev,n)))
        #self.h_eff_dz[collection].Fill(hasProbe, abs(ev.HardProcessParticle_dz[n]))
        #if abs(ev.HardProcessParticle_dxy[n]) < 2: self.h_eff_dz_cutdxy[collection].Fill(hasProbe, abs(ev.HardProcessParticle_dz[n]))
        #self.h_eff_2D[collection].Fill(hasProbe, abs(ev.HardProcessParticle_dxy[n]), abs(ev.HardProcessParticle_dz[n]))


    def processEvent(self, ev):
        ## First, process tracks
        for collection in self.collections[0:2]:
            if eval('ev.n{0}'.format(collection)) < 1: continue
            for n in range(eval('ev.n{0}'.format(collection))):
                ## Apply cuts
                if np.prod(eval(self.cuts[collection])):
                    ## Fill variable plots
                    self.fillVariableHistograms(ev, n, collection)
            ## Compute efficiencies wrt generation
            ##     Loop over hard process particles
            for i in range(ev.nHardProcessParticle):
                if abs(ev.HardProcessParticle_pdgId[i]) != 13: continue
                hasProbe, n = self.findProbeTracks(ev, i, collection)
                self.fillEfficiencyHistograms(ev, i, collection, hasProbe)

        ## Secondly, process displacedMuon collection
        ndsa_ids, ndgl_ids = self.count_muons(ev)
        for ndsa in ndsa_ids:
            ### Apply cuts
            if np.prod(eval(self.cuts['dmu_dsa'])): 
                ## Fill variable plots
                self.fillVariableHistograms(ev, ndsa, 'dmu_dsa')
        for ndgl in ndgl_ids:
            ### Apply cuts
            if np.prod(eval(self.cuts['dmu_dgl'])):
                ## Fill variable plots
                self.fillVariableHistograms(ev, ndgl, 'dmu_dgl')
        ## Compute efficiencies wrt generation
        ##     Loop over hard process particles
        for i in range(ev.nHardProcessParticle):
            if abs(ev.HardProcessParticle_pdgId[i]) != 13: continue
            hasProbe_DSA, n_DSA, hasProbe_DGL, n_DGL = self.findProbeMuons(ev, i)
            self.fillEfficiencyHistograms(ev, i, 'dmu_dsa', hasProbe_DSA)
            self.fillEfficiencyHistograms(ev, i, 'dmu_dgl', hasProbe_DGL)


    '''
    Given one muon (tag), loop through the generated particles in the event to find a matching probe.
    '''
    def findProbeMuons(self, ev, i):
        hasProbe_DSA = False
        hasProbe_DGL = False
        nDSA = -1
        nDGL = -1

        phi_tag = ev.HardProcessParticle_phi[i]
        eta_tag = ev.HardProcessParticle_eta[i]
        for n in range(ev.ndmu):
            if ev.dmu_isDSA[n]:
                phi_temp   = ev.dmu_dsa_phi[n]
                eta_temp   = ev.dmu_dsa_eta[n]
                dR = self.deltaR(phi_tag, eta_tag, phi_temp, eta_temp)
                if dR < 0.2:
                    hasProbe_DSA = True
                    nDSA = n
            if ev.dmu_isDGL[n]:
                phi_temp   = ev.dmu_dgl_phi[n]
                eta_temp   = ev.dmu_dgl_eta[n]
                dR = self.deltaR(phi_tag, eta_tag, phi_temp, eta_temp)
                if dR < 0.2:
                    hasProbe_DGL = True
                    nDGL = n
        return hasProbe_DSA, nDSA, hasProbe_DGL, nDGL


    '''
    Given one muon (tag), loop through the generated particles in the event to find a matching probe.
    '''
    def findProbeTracks(self, ev, i, collection):

        if collection=='dsa':
            phi_tag = ev.HardProcessParticle_phi[i]
            eta_tag = ev.HardProcessParticle_eta[i]
            for n in range(ev.ndsa):
                phi_temp   = ev.dsa_phi[n]
                eta_temp   = ev.dsa_eta[n]
                dR = self.deltaR(phi_tag, eta_tag, phi_temp, eta_temp)
                if dR < 0.2: 
                    return True, n
            return False, -1

        if collection=='dgl': 
            phi_tag = ev.HardProcessParticle_phi[i]
            eta_tag = ev.HardProcessParticle_eta[i]
            for n in range(ev.ndgl):
                phi_temp   = ev.dgl_phi[n]
                eta_temp   = ev.dgl_eta[n]
                dR = self.deltaR(phi_tag, eta_tag, phi_temp, eta_temp)
                if dR < 0.2:
                    return True, n
            return False, -1


    def count_muons(self, ev):
        # Count number of muons that are dsa and dgl
        ndsa_ids = []
        ndgl_ids = []
        nmuons = [0,0]
        nmuons_up   = [0,0]
        nmuons_down = [0,0]
        for n in range(ev.ndmu):
            if ev.dmu_isDSA[n]:
                ndsa_ids.append(n)
                nmuons[0] += 1
                if ev.dmu_dsa_phi[n]<0: nmuons_down[0] += 1
                else: nmuons_up[0] += 1
            if ev.dmu_isDGL[n]:
                ndgl_ids.append(n)
                nmuons[1] += 1
                if ev.dmu_dgl_phi[n]<0: nmuons_down[1] += 1
                else: nmuons_up[1] += 1
        for i,col in enumerate(self.collections[2:4]):
            self.h_nmuons[col].Fill(nmuons[i])
            self.h_nmuons_up[col].Fill(nmuons_up[i])
            self.h_nmuons_down[col].Fill(nmuons_down[i])
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
                    self.h_muons_filter.Fill(0)
                    debug.print("Muon lost at layer 1 of filter", "INFO")
                    return False
            else:
                if toApply[1] and not self.mfilter.layerTwoFilter(ev, n): 
                    self.h_muons_filter.Fill(1)
                    debug.print("Muon lost at layer 2 of filter", "INFO")
                    return False
        else:
            if ev.dmu_isDGL[n] or ev.dmu_isDTK[n]:
                if toApply[2] and not self.mfilter.layerThreeFilter(ev, n): 
                    self.h_muons_filter.Fill(2)
                    debug.print("Muon lost at layer 3 of filter", "INFO")
                    return False
            else: 
                debug.print("Muon that has not standalone nor tracker track.", "WARNING")
                return False
        return True

    def deltaR(self, phi1, eta1, phi2, eta2):
        dPhi = abs(phi1 - phi2)
        if dPhi > math.pi: dPhi = 2*math.pi - dPhi
        dEta = eta1 - eta2
        dR = np.sqrt(dPhi*dPhi + dEta*dEta)
        return dR

    def Lxy_value(self, ev, i):
        vx = ev.HardProcessParticle_vx[i]
        vy = ev.HardProcessParticle_vy[i]
        phi = ev.HardProcessParticle_phi[i]
        pv_vx = ev.PV_vx
        pv_vy = ev.PV_vy

        dxy = -(vx-pv_vx)*np.sin(phi) + (vy-pv_vy)*np.cos(phi)
        Lxy = np.sqrt((vx-pv_vx)*(vx-pv_vx) + (vy-pv_vy)*(vy-pv_vy))
        return Lxy

    def write(self):
        output = r.TFile(self.filename, "RECREATE")
        for attr, value in self.__dict__.items():
            if attr[0] == 'h' and type(value) == dict:
                for key in value.keys():
                    value[key].Write()
                    debug.print(value[key].GetName()+" written to "+self.filename, "SUCCESS")
        '''
        self.h_muons_filter.Write()
        self.h_dxy_1.Write()
        self.h_dxy_2.Write()
        self.h_dxy_3.Write()
        self.h_nsegments_dmu_dsa.Write()
        self.h_numberOfMatches_dmu_dsa.Write()
        self.h_nmatches_nsegments_2D_dmu_dsa.Write()
        self.h_nstations_dmu_dsa.Write()
        self.h_nsegments_nstations_2D_dmu_dsa.Write()
        '''
        output.Close()
