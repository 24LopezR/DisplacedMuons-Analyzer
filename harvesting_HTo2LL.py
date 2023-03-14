import ROOT as r
import os
from math import pi
import numpy as np
from argparse import ArgumentParser
import include.drawUtils as draw
from include.Launcher import Launcher

#r.gStyle.SetLabelFont(42)
################################# GLOBAL VARIABLES DEFINITION ####################################

runningfile = os.path.abspath(__file__)
WORKPATH = ''
for level in runningfile.split('/')[:-1]:
    WORKPATH += level
    WORKPATH += '/'
EOSPATH = '/eos/user/r/rlopezru/Cosmics-Analyzer_out/'


def makeVarPlot(hfile, hname, tag, title, collection, names, color=r.kBlue, ylog=True):
    
    h_track = hfile.Get(hname+"_"+collection) # track hist
    h_muon = hfile.Get(hname+"_dmu_"+collection) # muon hist
    
    maxVal = max([h_track.GetMaximum(), h_muon.GetMaximum()])

    #### Styling
    h_track.SetLineWidth(1)
    h_track.SetTitle(title)
    if ylog: 
        h_track.SetMaximum(100*maxVal)
        h_track.SetMinimum(1)
    else: h_track.SetMaximum(1.2*maxVal)
    h_track.SetLineColor(color)
    h_track.SetFillColorAlpha(color, 0.05)
    #### Styling muon plot
    h_muon.SetLineWidth(1)
    h_muon.SetTitle(title)
    if ylog: h_muon.SetMaximum(10*maxVal)
    else: h_muon.SetMaximum(1.2*maxVal)
    h_muon.SetLineColor(color)
    h_muon.SetFillColorAlpha(color, 0.05)
    h_muon.SetLineStyle(2)

    c = r.TCanvas(hname+collection, hname+collection)
    c.SetFillStyle(4000)
    c.cd()
    if ylog: c.GetPad(0).SetLogy(1)
    else: c.GetPad(0).SetLogy(0)
    
    h_track.Draw("HIST")    
    h_muon.Draw("HIST,SAME")
    
    l = r.TLegend(.65,.80,.90,.86)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.025)
    l.AddEntry(h_track, names[0], "L")
    l.AddEntry(h_muon, names[1], "L")
    l.SetBorderSize(0)
    l.Draw()
    
    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.20, 0.93, "#bf{CMS} #it{Simulation}")
   
    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.025);
    latex.DrawLatex(0.17, 0.86, "HTo2LongLivedTo2mu2jets")
    latex.DrawLatex(0.17, 0.83, "DisplacedMuonFilter (numberOfMatches #geq 2)")
    latex.DrawLatex(0.17, 0.80, "No trigger, no ID cuts")
    
    if not os.path.exists(EOSPATH+'Plots/'+tag):
        os.makedirs(EOSPATH+'Plots/'+tag)
    c.Print(EOSPATH+'Plots/'+tag+'/'+hname+collection+".png")
    c.Print(EOSPATH+'Plots/'+tag+'/'+hname+collection+".pdf")


def makeFilterPlot(hfile, hname, tag, title, color=r.kBlue, ylog=True):
    
    h_muon = hfile.Get(hname) # muon hist
    
    maxVal = h_muon.GetMaximum()

    c = r.TCanvas(hname, hname)
    c.SetFillStyle(4000)
    c.cd()
    if ylog: c.GetPad(0).SetLogy(1)
    else: c.GetPad(0).SetLogy(0)

    #### Styling muon plot
    h_muon.SetLineWidth(1)
    h_muon.SetTitle(title)
    if ylog: h_muon.SetMaximum(2*maxVal)
    else: h_muon.SetMaximum(1.2*maxVal)
    h_muon.SetLineColor(color)
    h_muon.SetFillColorAlpha(color, 0.05)
    h_muon.SetLineStyle(1)

    ### Bin labels
    labels = ['stage 1','stage 2','stage 3']
    for i in range(3): h_muon.GetXaxis().SetBinLabel(i+1,labels[i])
    h_muon.SetMinimum(1)
    h_muon.Draw("HIST")    
     
    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.34, 0.93, "#bf{CMS} #it{Simulation}")

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.025);
    latex.DrawLatex(0.17, 0.86, "HTo2LongLivedTo2mu2jets")
    latex.DrawLatex(0.17, 0.83, "DisplacedMuonFilter (numberOfMatches #geq 2)")
    latex.DrawLatex(0.17, 0.80, "No trigger, no ID cuts")
 
    if not os.path.exists(EOSPATH+'Plots/'+tag):
        os.makedirs(EOSPATH+'Plots/'+tag)
    c.Print(EOSPATH+'Plots/'+tag+'/'+hname+".png")
    c.Print(EOSPATH+'Plots/'+tag+'/'+hname+".pdf")


if __name__ == '__main__':

    r.gROOT.ProcessLine('.L ./include/tdrstyle.C')
    r.gROOT.SetBatch(1)
    print('WORKPATH: ' + WORKPATH)

    r.gStyle.SetPaintTextFormat("3.2f")
    parser = ArgumentParser()
    parser.add_argument('-t', '--tag', dest='tag')
    parser.add_argument('-a', '--aod', dest='aod', action='store_true')
    args = parser.parse_args()
    
    data = 'MiniAOD'
    if args.aod: data = 'AOD'

    r.setTDRStyle()    
    collections = ['dsa', 'dgl']
    
    launch = Launcher(None, args.tag, None)
    title = ''
    hfilename = launch.mergeHists()
    hfile = r.TFile(hfilename)
    hists =     ["h_pt", "h_eta", "h_phi", "h_normalizedChi2"]
    hists_log = ["h_pt_100", "h_dxy", "h_dz"]
    colors = [r.kViolet+4, r.kTeal+3]
    
    for n,collection in enumerate(collections):
        for h in hists:
            makeVarPlot(hfile, h, args.tag, title, collection, names=['track({0})'.format(collection),'muon({0})'.format(collection)], color=colors[n], ylog=False) 
        for h in hists_log:
            makeVarPlot(hfile, h, args.tag, title, collection, names=['track({0})'.format(collection),'muon({0})'.format(collection)], color=colors[n], ylog=True) 
    #makeFilterPlot(hfile, 'h_muons_filter', args.tag, title, color=r.kRed+1, ylog=True)
