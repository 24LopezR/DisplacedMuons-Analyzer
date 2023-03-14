import ROOT as r
from math import pi
import numpy as np

'''
Given one muon, checks if it passes the ID selection for tag and probe method.
'''
def passIDSelection(ev, i, col):
    passID = False

    if 'dsa' in col:
        if eval('ev.{0}_phi[i]'.format(col)) >= -0.8: return
        if eval('ev.{0}_phi[i]'.format(col)) <= -2.1: return
        if eval('abs(ev.{0}_eta[i])'.format(col)) >= 0.7: return
        if eval('ev.{0}_pt[i]'.format(col)) <= 12.5: return
        if eval('ev.{0}_ptError[i]/ev.{0}_pt[i]'.format(col)) >= 0.2: return
        if eval('ev.{0}_nValidMuonDTHits[i]'.format(col)) <= 30: return
        if eval('ev.{0}_normalizedChi2[i]'.format(col)) >= 2: return
        passID = True
    
    if 'dgl' in col:        
        if eval('ev.{0}_phi[i]'.format(col)) >= -0.6: return
        if eval('ev.{0}_phi[i]'.format(col)) <= -2.6: return
        if eval('abs(ev.{0}_eta[i])'.format(col)) >= 0.9: return
        if eval('ev.{0}_pt[i]'.format(col)) <= 20: return
        if eval('ev.{0}_ptError[i]/ev.{0}_pt[i]'.format(col)) >= 0.3: return
        if eval('ev.{0}_nMuonHits[i]'.format(col)) <= 12: return
        if eval('ev.{0}_nValidStripHits[i]'.format(col)) <= 5: return
        passID = True
    
    return passID


def angle(v1, v2):
    # assuming unit vectors
    cos_angle = np.dot(v1, v2)
    return cos_angle
