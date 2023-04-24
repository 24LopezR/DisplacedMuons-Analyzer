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

def makeEfficiencyPlot(hfile, hname, title, tag, collection, names, color=r.kBlue+1):
    
    h_track = hfile.Get(hname+"_"+collection)
    h_muon = hfile.Get(hname+"_dmu_"+collection)

    c = r.TCanvas(hname+collection,hname+collection)
    #c.SetFillStyle(4000)
    c.cd()
    
    h_track.Draw("PA")
    h_muon.Draw("P,SAME")
   
    c.Update() 
    #### Styling track plot
    h_track.SetLineWidth(1)
    h_track.SetLineColor(color) 
    h_track.SetMarkerColor(color)
    h_track.SetMarkerStyle(20)
    #h_track.SetTitle(title)
    _g = h_track.GetPaintedGraph()
    _g.SetMinimum(0)
    _g.SetMaximum(1.2)
    _g.GetYaxis().SetTitle('Efficiency')
    #### Styling muon plot
    h_muon.SetLineWidth(1)
    h_muon.SetLineColor(color) 
    h_muon.SetMarkerColor(color)
    h_muon.SetMarkerStyle(r.kCircle)
    #h_muon.SetTitle(title)
    #_g = h_track.GetPaintedGraph()
    #_g.SetMinimum(0)
    #_g.SetMaximum(1.2)
    #_g.GetYaxis().SetTitle('Efficiency')
        
    l = r.TLegend(.60,.32,.85,.40)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.025)
    l.AddEntry(h_track, names[0], "P")
    l.AddEntry(h_muon, names[1], "P")
    l.SetBorderSize(0)
    l.Draw()

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.34, 0.93, "#bf{CMS} #it{Internal}")

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.03);
    latex.DrawLatex(0.92, 0.93, "Run3 2022C cosmics data ({0})".format(data))
    
    if not os.path.exists(EOSPATH+'Plots/'+tag):
        os.makedirs(EOSPATH+'Plots/'+tag)
    c.Print(EOSPATH+'Plots/'+tag+'/'+hname+collection+".png")
    c.Print(EOSPATH+'Plots/'+tag+'/'+hname+collection+".pdf")



def make2DEfficiencyPlot(hfile, hname, title, tag, collection, zlog=False):
    
    h = hfile.Get(hname+'_'+collection)

    c = r.TCanvas(hname+collection,hname+collection,ww=610,wh=600)
    c.SetFillStyle(4000)
    c.cd()
    if zlog: c.SetLogy(1)
    else: c.SetLogy(0)
    
    h.Draw("COLZ,TEXT")    
   
    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.33, 0.93, "#bf{CMS} #it{Internal}")

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.03);
    latex.DrawLatex(0.90, 0.93, "Run3 2022C cosmics data ({0})".format(data))
    
    if not os.path.exists(EOSPATH+'Plots/'+tag):
        os.makedirs(EOSPATH+'Plots/'+tag)
    c.Print(EOSPATH+'Plots/'+tag+'/'+hname+collection+".png")
    c.Print(EOSPATH+'Plots/'+tag+'/'+hname+collection+".pdf")


def makeVarPlot(hfile, hname, tag, title, collection, names, color=r.kBlue, ylog=True):
    
    h_track = hfile.Get(hname+"_"+collection) # track hist
    h_muon = hfile.Get(hname+"_dmu_"+collection) # muon hist
    
    maxVal = max([h_track.GetMaximum(), h_muon.GetMaximum()])

    #### Styling
    h_track.SetLineWidth(1)
    h_track.SetTitle(title)
    if ylog: h_track.SetMaximum(100*maxVal)
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
    
    l = r.TLegend(.65,.80,.90,.87)
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
    latex.DrawLatex(0.20, 0.93, "#bf{CMS} #it{Internal}")

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.03);
    latex.DrawLatex(0.88, 0.93, "Run3 2022C cosmics data ({0})".format(data))
   
    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.025);
    #latex.DrawLatex(0.17, 0.86, "Emulated DisplacedMuonFilter".format(data))
    #latex.DrawLatex(0.17, 0.83, "(minMatches=2, minPtSTA=3.5, minPtTK=3.5)".format(data))
    latex.DrawLatex(0.17, 0.80, "NoBPTX3BX trigger, no ID cuts".format(data))
    
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
    latex.DrawLatex(0.34, 0.93, "#bf{CMS} #it{Internal}")

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.03);
    latex.DrawLatex(0.90, 0.93, "Run3 2022C cosmics data ({0})".format(data))

 
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
    hists =     ["h_pt",       "h_eta",     "h_phi",
                 "h_dxy",      "h_dz",      "h_normalizedChi2"]
    hists_eff = ["h_eff_pt",   "h_eff_eta", 
                 "h_eff_dxy",  "h_eff_dxy_cutdz", 
                 "h_eff_dz",   "h_eff_dz_cutdxy"]
    hists_log = ["h_cosalpha", "h_dPhi", "h_dEta"]
    colors = [r.kRed+1, r.kBlue+1]
    
    for n,collection in enumerate(collections):
        for h in hists_eff:
            makeEfficiencyPlot(hfile, h, title, args.tag, collection, names=['track({0})'.format(collection),'muon({0})'.format(collection)], color=colors[n])
        for h in hists:
            makeVarPlot(hfile, h, args.tag, title, collection, names=['track({0})'.format(collection),'muon({0})'.format(collection)], color=colors[n], ylog=False)
        for h in hists_log:
            makeVarPlot(hfile, h, args.tag, title, collection, names=['track({0})'.format(collection),'muon({0})'.format(collection)], color=colors[n], ylog=True)
        make2DEfficiencyPlot(hfile, "h_eff_2D", title, args.tag, collection, zlog=False) 
        make2DEfficiencyPlot(hfile, "h_eff_2D_dmu", title, args.tag, collection, zlog=False) 
    
    makeFilterPlot(hfile, 'h_muons_filter', args.tag, title, color=r.kRed+1, ylog=True)
