import math
import os
import ROOT as r
import numpy as np
from include.Debugger import Debugger
from include.utils import passIDSelection, angle
from include.DisplacedMuonFilter import DisplacedMuonFilter
from include.PlotHandler import PlotHandler
import include.cfg as cfg

# Config debugger
debug = Debugger(cfg.DEBUG)

'''
In this script I will only take care about DSA
'''
class MCSignalPlotHandler(PlotHandler):


    def __init__(self, histfilename, cutsFilePath, sampleName):    
        
        super().__init__(histfilename, cutsFilePath, sampleName)

        self.collections = ['dsa','dmu_dsa']
         
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
        self.h_pt_residual = {}
        self.h_cosalpha = {}
        self.h_dPhi = {}
        self.h_dEta = {}
        self.h_eff_pt = {}
        self.h_eff_pt_resptcut = {}
        self.h_eff_eta = {}
        self.h_eff_eta_resptcut = {}
        self.h_eff_Lxy = {}
        self.h_eff_Lxy_300 = {}
        self.h_eff_Lxy_resptcut = {}
        self.h_eff_Lxy_cutdz = {}
        self.h_eff_dz = {}
        self.h_eff_dz_cutdxy = {}
        self.h_eff_2D = {}
        self.h_dxy_dz_2D = {}
        self.h_matched_IDS_2D = {}
        self.h_check_if_tracks_and_muons_are_identical = {}

        for collection in self.collections:
            self.h_nmuons[collection]          = r.TH1F("h_muons_{0}".format(collection),r";N_{#mu};N events",6,0,6) 
            self.h_nmuons_down[collection]     = r.TH1F("h_muons_down_{0}".format(collection),r";N_{#mu}(#phi<0);N events",6,0,6) 
            self.h_nmuons_up[collection]       = r.TH1F("h_muons_up_{0}".format(collection),r";N_{#mu}(#phi>0);N events",6,0,6) 
            self.h_pt[collection]              = r.TH1F("h_pt_{0}".format(collection),r";p_{T} (GeV);N events",50,0,200)
            self.h_pt_100[collection]          = r.TH1F("h_pt_100_{0}".format(collection),r";p_{T} (GeV);N events",50,0,100)
            self.h_eta[collection]             = r.TH1F("h_eta_{0}".format(collection),r";#eta;N events",30,-0.9,0.9)
            self.h_eta_down[collection]        = r.TH1F("h_eta_down_{0}".format(collection),r";#eta;N events",30,-0.9,0.9)
            self.h_eta_up[collection]          = r.TH1F("h_eta_up_{0}".format(collection),r";#eta;N events",30,-0.9,0.9)
            self.h_phi[collection]             = r.TH1F("h_phi_{0}".format(collection),r";#phi;N events",30,-3.2,3.2)
            self.h_dxy[collection]             = r.TH1F("h_dxy_{0}".format(collection),r";|d_{xy}| (cm);N events",100,0,800)
            self.h_dz[collection]              = r.TH1F("h_dz_{0}".format(collection),r";|d_{z}| (cm);N events",100,0,800)
            self.h_Nhits[collection]           = r.TH1F("h_Nhits_{0}".format(collection),r";nValidMuonHits;N events",100,0,50)
            self.h_NDThits[collection]         = r.TH1F("h_NDThits_{0}".format(collection),r";nValidMuonDTHits;N events",100,0,50)
            self.h_normalizedChi2[collection]  = r.TH1F("h_normalizedChi2_{0}".format(collection),r";#chi^{2}/ndof;N events",100,0,5)
            self.h_charge_pt[collection]       = r.TH1F("h_charge_pt_{0}".format(collection),r";Q/p_{T};N events",100,-0.1,0.1)
            self.h_pt_residual[collection]     = r.TH1F("h_pt_residual_{0}".format(collection),r";(p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen};N events",30,-1.2,1.7)
            self.h_cosalpha[collection]        = r.TH1F("h_cosalpha_{0}".format(collection),r";cos(#alpha);N events",100,-1,1)
            self.h_dPhi[collection]            = r.TH1F("h_dPhi_{0}".format(collection),r";|#Delta#phi|;N events",100,0,3.2)
            self.h_dEta[collection]            = r.TH1F("h_dEta_{0}".format(collection),r";#Delta#eta;N events",100,-2.4,2.4)
            self.h_eff_pt[collection]          = r.TEfficiency("h_eff_pt_{0}".format(collection), "Efficiency;p_{T} (GeV);Efficiency",18,0,90)
            self.h_eff_pt_resptcut[collection] = r.TEfficiency("h_eff_pt_resptcut_{0}".format(collection), "Efficiency;p_{T} (GeV);Efficiency",18,0,90)
            self.h_eff_eta[collection]         = r.TEfficiency("h_eff_eta_{0}".format(collection),"Efficiency;#eta;Efficiency",18,-1.2,1.2)
            self.h_eff_eta_resptcut[collection]= r.TEfficiency("h_eff_eta_resptcut_{0}".format(collection),"Efficiency;#eta;Efficiency",18,-1.2,1.2)
            self.h_eff_Lxy[collection]         = r.TEfficiency("h_eff_Lxy_{0}".format(collection),"Efficiency;|L_{xy}| (cm);Efficiency", 9, 
                                                               np.array([0., 2., 5., 10., 20., 30., 40., 50., 60., 70.]))
            self.h_eff_Lxy_300[collection]     = r.TEfficiency("h_eff_Lxy_300_{0}".format(collection),"Efficiency;|L_{xy}| (cm);Efficiency", 16, 
                                                               np.array([0., 2., 5., 10., 20., 30., 40., 50., 60., 70., 90., 110., 130., 150., 200., 250., 300.]))
            self.h_eff_Lxy_resptcut[collection]= r.TEfficiency("h_eff_Lxy_resptcut_{0}".format(collection),"Efficiency;|L_{xy}| (cm);Efficiency", 16, 
                                                               np.array([0., 2., 5., 10., 20., 30., 40., 50., 60., 70., 90., 110., 130., 150., 200., 250., 300.]))
            self.h_eff_Lxy_cutdz[collection]   = r.TEfficiency("h_eff_Lxy_cutdz_{0}".format(collection),"Efficiency;|L_{xy}| (cm);Efficiency", 9, 
                                                               np.array([0., 2., 5., 10., 20., 30., 40., 50., 60., 70.]))
            self.h_eff_dz[collection]          = r.TEfficiency("h_eff_dz_{0}".format(collection), "Efficiency;|d_{z}| (cm);Efficiency", 6, 
                                                               np.array([0., 8., 20., 40., 60., 90., 140.]))
            self.h_eff_dz_cutdxy[collection]   = r.TEfficiency("h_eff_dz_cutdxy_{0}".format(collection),"Efficiency;|d_{z}| (cm);Efficiency", 6, 
                                                               np.array([0., 8., 20., 40., 60., 90., 140.]))
            self.h_eff_2D[collection]          = r.TEfficiency("h_eff_2D_{0}".format(collection), "Efficiency;|d_{0}| (cm);|d_{z}| (cm);Efficiency",6,
                                                               np.array([0., 2., 5., 10., 30., 50., 70.]), 6,np.array([0., 8., 20., 40., 60., 90., 140.]))
            self.h_dxy_dz_2D[collection]       = r.TH2F("h_dxy_dz_2D_{0}".format(collection), "Displacement;|d_{0}| (cm);|d_{z}| (cm);N events",100,0,500,100,0,700)
        
        self.h_matched_IDS_2D['0']             = r.TH2F("h_matched_IDS_2D", ";DSA ID;DGL ID;N events",4,-1,3,4,-1,3)
        self.h_check_if_tracks_and_muons_are_identical['0'] = r.TH1F("h_check", ";passTrack + passMuon;N events", 2,0,2)        

        ### Parse config file
        self.readCuts()


    def readCuts(self):
        super().readCuts()


    '''
    Perform an OR of the triggers
    '''
    def evalTriggers(self, ev):
        # True if there are no triggers in the list
        if not self.triggers:
            return True
        for t in self.triggers:
            if eval(t): return True
        return False


    '''
    Check if a muon passes the defined cuts
    '''
    def evalCuts(self, ev, n, collection):
        for c in self.cuts[collection]:
            if 'ID' in c:
                if not super().passDSAID(ev, n, collection): return False
            else:
                if not eval(c): return False
        return True


    def fillVariableHistograms(self, ev, n, collection):
        self.h_pt[collection].Fill(eval('ev.{0}_pt[n]'.format(collection)))
        self.h_pt_100[collection].Fill(eval('ev.{0}_pt[n]'.format(collection)))
        self.h_eta[collection].Fill(eval('ev.{0}_eta[n]'.format(collection)))
        self.h_phi[collection].Fill(eval('ev.{0}_phi[n]'.format(collection)))
        self.h_dxy[collection].Fill(eval('abs(ev.{0}_dxy[n])'.format(collection)))
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
        if True:
        #if ev.HardProcessParticle_pt[n] >= 3.5:
           self.h_eff_eta[collection].Fill(hasProbe, ev.HardProcessParticle_eta[n])
           self.h_eff_Lxy[collection].Fill(hasProbe, abs(self.Lxy_value(ev,n)))
           self.h_eff_Lxy_300[collection].Fill(hasProbe, abs(self.Lxy_value(ev,n)))
        

    def fillPtResidual(self, collection, ev, i, n):
        pt_gen = ev.HardProcessParticle_pt[i]
        pt_reco = eval('ev.{0}_pt[n]'.format(collection))
        res_pt = (pt_reco-pt_gen)/pt_gen
        self.h_pt_residual[collection].Fill(res_pt) # we know pt_gen is not zero
        if abs(res_pt) < 0.3: passed = True
        else: passed = False
        self.h_eff_pt_resptcut[collection].Fill(passed, ev.HardProcessParticle_pt[i])
        self.h_eff_eta_resptcut[collection].Fill(passed, ev.HardProcessParticle_eta[i])
        self.h_eff_Lxy_resptcut[collection].Fill(passed, abs(self.Lxy_value(ev,i)))


    def processEvent(self, ev):
        ## Check if events pass the trigger
        if not self.evalTriggers(ev): return
        if ev.ndsa < 1 and ev.ndmu < 1: return
        passTrack = []
        passMuon = []

        # -------------------------------------------------------------------------------
        ## First, process DSA tracks
        for n in range(ev.ndsa):
            ## Apply cuts
            if self.evalCuts(ev, n, 'dsa'):
                passTrack.append(1)
                ## Fill variable plots
                self.fillVariableHistograms(ev, n, 'dsa')
        ## Compute efficiencies wrt generation
        ##     Loop over hard process particles
        for i in range(ev.nHardProcessParticle):
            if abs(ev.HardProcessParticle_pdgId[i]) != 13: continue
            hasProbe, _ = self.findProbeTracks(ev, i)
            self.fillEfficiencyHistograms(ev, i, 'dsa', hasProbe)
        # -------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------
        ## Secondly, process displacedMuon DSA collection
        #print('>> Start pat::Muon')
        for n in range(ev.ndmu):
            #print('  >> ndmu = {0}'.format(n))
            ### Check if muon is DSA
            if not ev.dmu_isDSA[n]: 
                #print('  >> dmu_isDSA = False')
                continue
            #print('  >> dmu_isDSA = True')
            ### Apply cuts
            if self.evalCuts(ev, n, 'dmu_dsa'):
                passMuon.append(1)
                ## Fill variable plots
                #print('  >> Passed cuts. Filling hists...')
                self.fillVariableHistograms(ev, n, 'dmu_dsa')
        ## Compute efficiencies wrt generation
        ##     Loop over hard process particles
        #print('>> Loop over HardProcessParticles')
        for i in range(ev.nHardProcessParticle):
            if abs(ev.HardProcessParticle_pdgId[i]) != 13: continue
            hasProbe, _ = self.findProbeMuons(ev, i)
            #print('  >> hasProbe = {0}'.format(hasProbe))
            self.fillEfficiencyHistograms(ev, i, 'dmu_dsa', hasProbe)
        # -------------------------------------------------------------------------------
        self.h_check_if_tracks_and_muons_are_identical['0'].Fill((sum(passMuon)+sum(passTrack))%2)


    '''
    Given one hard process particle (tag), loop through the tracks in the event to find a matching probe.
    '''
    def findProbeTracks(self, ev, i):
        hasProbe = False
        n = -1
        dR = 1

        phi_tag = ev.HardProcessParticle_phi[i]
        eta_tag = ev.HardProcessParticle_eta[i]
        for n_temp in range(ev.ndsa):
            phi_temp   = ev.dsa_phi[n_temp]
            eta_temp   = ev.dsa_eta[n_temp]
            dR_temp = self.deltaR(phi_tag, eta_tag, phi_temp, eta_temp)
            ## Apply cuts
            if not self.evalCuts(ev, n_temp, 'dsa'): continue
            if dR_temp < 0.5:
                hasProbe = True
                if dR_temp < dR: 
                    dR = dR_temp
                    n = n_temp
        if n > -1: self.fillPtResidual('dsa', ev, i, n)
        return hasProbe, n


    '''
    Given one hard process particle (tag), loop through the muons in the event to find a matching probe.
    '''
    def findProbeMuons(self, ev, i):
        hasProbe = False
        n = -1
        dR = 1

        phi_tag = ev.HardProcessParticle_phi[i]
        eta_tag = ev.HardProcessParticle_eta[i]
        for n_temp in range(ev.ndmu):
            if ev.dmu_isDSA[n_temp]:
                phi_temp   = ev.dmu_dsa_phi[n_temp]
                eta_temp   = ev.dmu_dsa_eta[n_temp]
                dR_temp = self.deltaR(phi_tag, eta_tag, phi_temp, eta_temp)
                ## Apply cuts
                if not self.evalCuts(ev, n_temp, 'dmu_dsa'): continue
                if dR_temp < 0.5:
                    hasProbe = True
                    if dR_temp < dR: 
                        dR = dR_temp
                        n = n_temp
        if n > -1: self.fillPtResidual('dmu_dsa', ev, i, n)
        return hasProbe, n


    def count_muons(self, ev):
        return super().count_muons(ev)


    '''
    Function to apply DisplacedMuonFilter. It fills a histogram telling, in case of returning False,
    in which stage of the filter the muon was dropped.
    Args:
        - ev               : event
        - n                : id of muon in event
        - toApply = [x,x,x]: indicates with 1 and 0 if each stage of the filter is applied
    '''
    def passMuonFilter(self, ev, n, toApply=[1,1,1]):
        return super().passMuonFilter(ev, n, toApply)


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
        output.Close()
