import ROOT as r
import os
from PIL import Image
from math import pi
import numpy as np
from argparse import ArgumentParser
from include.PlotHandler import PlotHandler


def makeVarPlot(hifiles, hname, tag, title, collections, names=['DSA muons (NhitsDT>30)', 'DSA muons (NhitsDT<30)'], ylog=True):
    
    hists = []
    for f in hifiles:
        hists.append(f.Get(hname+"_dsa"))

    #### Styling
    colors = [r.kBlue-3, r.kRed-3]
    for n,h in enumerate(hists):
        h.Scale(1/h.Integral())
        h.SetLineWidth(1)
        h.SetLineColor(colors[n])
        h.GetXaxis().SetTitleSize(0.045)
        h.GetXaxis().SetLabelSize(0.03)
        h.GetYaxis().SetTitleSize(0.045)
        h.GetYaxis().SetTitleOffset(1.25)
        h.GetYaxis().SetTitle('N muons (normalized)')
        h.GetYaxis().SetLabelSize(0.03)
        #h.SetFillColorAlpha(colors[n], 0.5)
        h.SetTitle(title)

    c = r.TCanvas(hname, hname)
    c.cd()
    if ylog: c.GetPad(0).SetLogy(1)
    else: c.GetPad(0).SetLogy(0)
    
    hists[0].Draw("HIST")    
    for h in hists[1:]: h.Draw("HIST,SAME")
    
    l = r.TLegend(.60,.80,.80,.87)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.03)
    for n,h in enumerate(hists):
        l.AddEntry(h, names[n], "L")
    l.SetBorderSize(0)
    l.Draw()
    
    if not os.path.exists('output/'+tag):
        os.makedirs('output/'+tag)
    c.Print('output/'+tag+'/'+hname+".png")
    print('File '+hname+'.png created')


if __name__ == '__main__':

    r.gROOT.SetBatch(1)
    r.gStyle.SetOptStat(0)
   
    parser = ArgumentParser()
    parser.add_argument('-m', '--mode', dest='mode')
    parser.add_argument('-c', '--cuts', dest='cuts_filename')
    parser.add_argument('-t', '--tag', dest='tag')
    args = parser.parse_args()
    MODE = args.mode
    
    ############## PLOT TITLE #########################################
    title = ""#'Cuts: #phi #in (-2.1,-0.8), pT > 12.5'
    ###################################################################

    collections = ['dsa']
    histfilename = ['hists/hists_one_down_muon_pt_nhits.root', 'hists/hists_one_down_muon_pt_nhits_inv.root']
    with open(args.cuts_filename, 'r') as f:
        cuts_selection = ''.join(f.readlines())

    if MODE == "plot":
        hfiles = [r.TFile(h) for h in histfilename]
        hists = ["h_muons", "h_muons_down", "h_muons_up", "h_pt", "h_eta", "h_phi", "h_dxy", "h_dz", "h_Nhits", "h_NDThits", "h_normalizedChi2"]
        hists_eff = ["h_eff_pt", "h_eff_eta", "h_eff_dxy", "h_eff_dz", "h_dEta"]
        hists_log = ["h_cosalpha", "h_dPhi"]
        for h in hists:
            makeVarPlot(hfiles, h, args.tag, title, collections, ylog=False)
