'''
Class that emulates the different stages of cmssw/PhysicsTools/PatAlgos/plugins/DisplacedMuonFilterProducer.cc
'''
class DisplacedMuonFilter:

    def __init__(self, minPtTK, minPtSTA, minMatches):
        self.minPtTK    = minPtTK
        self.minPtSTA   = minPtSTA
        self.minMatches = minMatches


    def layerOneFilter(self, ev, n):
        if ev.dmu_dtk_pt[n] < self.minPtTK and ev.dmu_dsa_pt[n] < self.minPtSTA: return False
        return True


    def layerTwoFilter(self, ev, n):
        #if not ev.dmu_isMatchesValid[n] or ev.dmu_numberOfMatches[n] < self.minMatches or ev.dmu_dsa_pt[n] < self.minPtSTA: return False
        if ev.dmu_dsa_nsegments[n] < 2 or ev.dmu_dsa_pt[n] < self.minPtSTA: return False
        return True


    def layerThreeFilter(self, ev, n):
        if ev.dmu_dtk_pt[n] < self.minPtTK or not ev.dmu_isDTK[n]: return False
        return True
