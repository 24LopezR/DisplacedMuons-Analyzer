import ROOT as r
from math import pi
import numpy as np

'''
Given one muon, checks if it passes the ID selection for tag and probe method.
'''
def passIDSelection(ev, i, col='dsa'):
    passID = False

    if col == 'dsa':
        if ev.dsa_phi[i] >= -0.8: return
        if ev.dsa_phi[i] <= -2.1: return
        if abs(ev.dsa_eta[i]) >= 0.7: return
        if ev.dsa_pt[i] <= 12.5: return
        if ev.dsa_ptError[i]/ev.dsa_pt[i] >= 0.2: return
        if ev.dsa_nValidMuonDTHits[i] <= 30: return
        if ev.dsa_normalizedChi2[i] >= 2: return
        passID = True
    
    if col == 'dgl':        
        if ev.dgl_phi[i] >= -0.6: return
        if ev.dgl_phi[i] <= -2.6: return
        if abs(ev.dgl_eta[i]) >= 0.9: return
        if ev.dgl_pt[i] <= 20: return
        if ev.dgl_ptError[i]/ev.dgl_pt[i] >= 0.3: return
        if ev.dgl_nMuonHits[i] <= 12: return
        #if ev.dgl_normalizedChi2[i] >= 2: return
        if ev.dgl_nValidStripHits[i] <= 5: return
        passID = True
    
    return passID


def angle(v1, v2):
    # assuming unit vectors
    cos_angle = np.dot(v1, v2)
    return cos_angle


'''
Given one muon (tag), loop through the other muons in the event to find a matching probe.
'''
def findProbe(ev, n, print_out=False, col='dsa'):
    existsProbe = False
    cos_alpha = None

    if col == 'dsa':
        phi_tag = ev.dsa_phi[n]
        eta_tag = ev.dsa_eta[n]
        theta_tag = 2 * np.arctan(np.exp(-eta_tag)) - np.pi/2

        for i in range(ev.ndsa):
            if i == n: continue
            if ev.dsa_nValidMuonDTHits[i]+ev.dsa_nValidMuonDTHits[i] <= 0: continue
            phi_temp = ev.dsa_phi[i]
            eta_temp = ev.dsa_eta[i]
            theta_temp = 2 * np.arctan(np.exp(-eta_temp)) - np.pi/2
            v_tag = [np.cos(theta_tag)*np.cos(phi_tag), np.cos(theta_tag)*np.sin(phi_tag), np.sin(theta_tag)]
            v_temp = [np.cos(theta_temp)*np.cos(phi_temp), np.cos(theta_temp)*np.sin(phi_temp), np.sin(theta_temp)]
            cos_alpha_temp = angle(v_tag, v_temp)
            cos_alpha = cos_alpha_temp
            if cos_alpha_temp < np.cos(2.1) :
                existsProbe = True
                break
    
    if col == 'dgl':
        phi_tag = ev.dgl_phi[n]
        eta_tag = ev.dgl_eta[n]
        theta_tag = 2 * np.arctan(np.exp(-eta_tag)) - np.pi/2

        for i in range(ev.ndgl):
            if i == n: continue
            if ev.dgl_pt[i] <= 20: continue
            #if ev.dgl_nValidMuonDTHits[i]+ev.dgl_nValidMuonDTHits[i] <= 0: continue
            phi_temp = ev.dgl_phi[i]
            eta_temp = ev.dgl_eta[i]
            theta_temp = 2 * np.arctan(np.exp(-eta_temp)) - np.pi/2
            v_tag = [np.cos(theta_tag)*np.cos(phi_tag), np.cos(theta_tag)*np.sin(phi_tag), np.sin(theta_tag)]
            v_temp = [np.cos(theta_temp)*np.cos(phi_temp), np.cos(theta_temp)*np.sin(phi_temp), np.sin(theta_temp)]
            cos_alpha_temp = angle(v_tag, v_temp)
            cos_alpha = cos_alpha_temp
            if cos_alpha < np.cos(2.8):
                existsProbe = True
                break
    
    return existsProbe, cos_alpha, i

def printOut(ev, n):
    print('     - phi = {phi}'.format(phi = ev.dsa_phi[n]))
    print('     - eta = {eta}'.format(eta = ev.dsa_eta[n]))
    print('     - theta = {theta}'.format(theta = 2 * np.arctan(np.exp(ev.dsa_eta[n]))))
    print('________________________________')
