import ROOT as r
import os
from argparse import ArgumentParser

'''
Script that loops over the events of a given ntuple
'''
if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-i', '--filename', dest='fname') # name of file containing the Ntuple
    parser.add_argument('-o', '--histfilename', dest='hfname') # name of the output file with the hists
    parser.add_argument('-n', '--name', dest='name')
    args = parser.parse_args()
    ### Read args
    inputFileName = args.fname
    outHistsFileName = args.hfname
    sampleName = args.name

    ### Open data file
    _file = r.TFile(inputFileName)
    _tree = _file.Get("Events")

    ### Define histograms
    h_nsegments_nhits_2D = r.TH2F("h_nsegments_nhits_2D", ";nsegments;nDThits + nCSChits;N events",10,0,10,50,0,50)
    h_pt                 = r.TH1F("h_pt", ";p_{T};N events",20,0,70)
    h_normChi2           = r.TH1F("h_normChi2", ";#chi^{2}_{norm};N events",20,0,10)
    h_ptError            = r.TH1F("h_ptError", ";#Delta p_{T}/p_{T};N events",20,0,2)

    ### Process events
    for i,ev in enumerate(_tree):
        if i%1000==0: 
            print("    - Events processed: {0}".format(str(i)))
        for n in range(ev.ndmu):
            if not ev.dmu_isDSA[n]: continue
            #if i%50==0: print("      nsegments = {0}, nDThits = {1}, nCSChits = {2}".format(ev.dmu_dsa_nsegments[n], ev.dmu_dsa_nValidMuonDTHits[n], ev.dmu_dsa_nValidMuonCSCHits[n]))
            nseg = ev.dmu_dsa_nsegments[n]
            nhits = ev.dmu_dsa_nValidMuonDTHits[n]+ev.dmu_dsa_nValidMuonCSCHits[n]
            #if i%50==0: print("      (nsegments, nhits) = ({0},{1})".format(nseg,nhits))
            h_nsegments_nhits_2D.Fill(nseg,nhits)
            # Apply DisplacedMuonFilter
            if nseg < 2 or ev.dmu_dsa_pt[n] < 3.5: continue
            h_pt.Fill(ev.dmu_dsa_pt[n])
            if nhits <= 12: continue
            if ev.dmu_dsa_nValidMuonCSCHits[n] == 0 and ev.dmu_dsa_nValidMuonDTHits[n] <= 18: continue
            h_normChi2.Fill(ev.dmu_dsa_normalizedChi2[n])
            if ev.dmu_dsa_normalizedChi2[n] >= 2.5: continue
            h_ptError.Fill(ev.dmu_dsa_ptError[n]/ev.dmu_dsa_pt[n])

    ### Write out to file
    if os.path.exists(outHistsFileName): os.system('rm {0}'.format(outHistsFileName))
    output = r.TFile(outHistsFileName, "RECREATE")
    h_nsegments_nhits_2D.Write()
    h_pt.Write()
    h_normChi2.Write()
    h_ptError.Write()
    output.Close()
