import ROOT as r
import os, json
from math import pi
import numpy as np
from argparse import ArgumentParser
import include.drawUtils as draw
from include.Launcher import Launcher
from include.DTree import DTree

#r.gStyle.SetLabelFont(42)
################################# GLOBAL VARIABLES DEFINITION ####################################

runningfile = os.path.abspath(__file__)
WORKPATH = ''
for level in runningfile.split('/')[:-1]:
    WORKPATH += level
    WORKPATH += '/'
EOSPATH = '/eos/user/r/rlopezru/DisplacedMuons-Analyzer_out/'

# Read dat file
datFile = WORKPATH + 'dat/Samples_Spring23.json'
dat = json.load(open(datFile,'r'))

def makeEfficiencyPlot(hfile, dtree, hname, tag, collection, names, color=r.kBlue+1, texts=[]):

    sample = dtree.name

    h_track = hfile.Get(hname+"_"+collection)
    h_muon = hfile.Get(hname+"_dmu_"+collection)

    c = r.TCanvas(sample+'_'+hname+'_'+collection, sample+'_'+hname+'_'+collection)
    c.cd()

    h_track.Draw("PA")
    h_muon.Draw("P,SAME")

    c.Update()
    #### Styling track plot
    h_track.SetLineWidth(1)
    h_track.SetLineColor(color[0])
    h_track.SetMarkerColor(color[0])
    h_track.SetMarkerStyle(20)
    _g = h_track.GetPaintedGraph()
    _g.SetMinimum(0)
    _g.SetMaximum(1.2)
    #_g.GetYaxis().SetTitle('Efficiency')
    #### Styling muon plot
    h_muon.SetLineWidth(1)
    h_muon.SetLineColor(color[1])
    h_muon.SetMarkerColor(color[1])
    h_muon.SetMarkerStyle(20)
    #_g = h_track.GetPaintedGraph()
    #_g.SetMinimum(0)
    #_g.SetMaximum(1.2)
    #_g.GetYaxis().SetTitle('Efficiency')

    l = r.TLegend(.60,.83,.85,.88)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.03)
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
    latex.DrawLatex(0.36, 0.93, "#bf{CMS} #it{Simulation}")

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.025);
    for n,t in enumerate(texts):
        latex.DrawLatex(0.17, 0.86-0.03*n, t)

    c.Print(EOSPATH+'Plots/{0}/{1}/{2}.png'.format(tag,dtree.name,c.GetName()))
    c.Print(EOSPATH+'Plots/{0}/{1}/{2}.pdf'.format(tag,dtree.name,c.GetName()))


def makeVarPlot(hfile, dtree, hname, tag, collection, names, color=r.kRed, texts=[], ylog=True):
    
    sample = dtree.name

    h_track = hfile.Get(hname+"_"+collection) # track hist
    h_muon = hfile.Get(hname+"_dmu_"+collection) # muon hist
    
    maxVal = max([h_track.GetMaximum(), h_muon.GetMaximum()])

    #### Styling track plot
    h_track.SetLineWidth(1)
    if ylog: 
        h_track.SetMaximum(100*maxVal)
        h_track.SetMinimum(1)
    else: h_track.SetMaximum(1.2*maxVal)
    h_track.SetLineColor(color)
    h_track.SetFillColorAlpha(color, 0.05)
    h_track.SetLineWidth(2)
    #### Styling muon plot
    h_muon.SetLineWidth(1)
    if ylog: h_muon.SetMaximum(10*maxVal)
    else: h_muon.SetMaximum(1.2*maxVal)
    h_muon.SetLineColor(color)
    h_muon.SetFillColorAlpha(color, 0.05)
    h_muon.SetLineWidth(2)
    h_muon.SetLineStyle(2)

    c = r.TCanvas(sample+'_'+hname+'_'+collection, sample+'_'+hname+'_'+collection)
    c.SetFillStyle(4000)
    c.cd()
    if ylog: c.GetPad(0).SetLogy(1)
    else: c.GetPad(0).SetLogy(0)
    
    h_track.Draw("HIST")    
    h_muon.Draw("HIST,SAME")
    
    l = r.TLegend(.60,.83,.85,.88)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.03)
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
    latex.SetTextAlign(11);
    latex.SetTextSize(0.025);
    for n,t in enumerate(texts):
        latex.DrawLatex(0.17, 0.86-0.03*n, t)
    
    c.Print(EOSPATH+'Plots/{0}/{1}/{2}.png'.format(tag,dtree.name,c.GetName()))
    c.Print(EOSPATH+'Plots/{0}/{1}/{2}.pdf'.format(tag,dtree.name,c.GetName()))

def make2DPlot(hfile, dtree, tag, hname, zlog=False, cut=True):

    sample = dtree.name
    label = dtree.label
    if 'nseg2' in sample: label += ' (nsegments #geq 2)'
    else: label += ' (numberOfMatches #geq 2)' 

    h = hfile.Get(hname)

    c = r.TCanvas(sample+'_'+hname,sample+'_'+hname,ww=620,wh=600)
    c.SetFillStyle(4000)
    c.cd()
    if zlog: c.SetLogz(1)
    else: c.SetLogz(0)

    h.GetXaxis().SetRange(1,10)
    h.GetYaxis().SetRange(1,10)
    h.Draw("COLZ,TEXT")

    if cut:
        line = r.TLine(2,0,2,10)
        line.SetLineColor(r.kRed)
        line.Draw()

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.36, 0.93, "#bf{CMS} #it{Internal}")

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.03);
    latex.DrawLatex(0.87, 0.93, label)

    c.Print(EOSPATH+'Plots/{0}/{1}/{2}.png'.format(tag,dtree.name,c.GetName()))
    c.Print(EOSPATH+'Plots/{0}/{1}/{2}.pdf'.format(tag,dtree.name,c.GetName()))


def makePlot(hfile, dtree, hname, tag, collection, name, color=r.kBlue, texts=[], ylog=True):
    
    sample = dtree.name

    h_muon = hfile.Get(hname+"_dmu_"+collection) # muon hist
    
    #### Styling muon plot
    h_muon.SetLineWidth(1)
    if ylog: h_muon.SetMaximum(10*h_muon.GetMaximum())
    else: h_muon.SetMaximum(1.2*h_muon.GetMaximum())
    h_muon.SetLineColor(color)
    h_muon.SetFillColorAlpha(color, 0.)
    h_muon.SetLineWidth(2)

    c = r.TCanvas(sample+'_'+hname+'_'+collection, sample+'_'+hname+'_'+collection)
    c.SetFillStyle(4000)
    c.cd()
    if ylog: c.GetPad(0).SetLogy(1)
    else: c.GetPad(0).SetLogy(0)
    
    h_muon.Draw("HIST")    
    
    l = r.TLegend(.60,.83,.85,.88)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.03)
    l.AddEntry(h_muon, name, "L")
    l.SetBorderSize(0)
    l.Draw()
    
    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.15, 0.93, "#bf{CMS} #it{Simulation}")
   
    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.03);
    for n,t in enumerate(texts):
        latex.DrawLatex(0.17, 0.86-0.03*n, t)
    
    c.Print(EOSPATH+'Plots/{0}/{1}/{2}.png'.format(tag,dtree.name,c.GetName()))
    c.Print(EOSPATH+'Plots/{0}/{1}/{2}.pdf'.format(tag,dtree.name,c.GetName()))


if __name__ == '__main__':

    r.gROOT.ProcessLine('.L ./include/tdrstyle.C')
    r.gROOT.SetBatch(1)
    print('WORKPATH: ' + WORKPATH)

    r.gStyle.SetPaintTextFormat("3.2f")
    parser = ArgumentParser()
    parser.add_argument('-t', '--tag',   dest='tag')
    parser.add_argument('-a', '--aod',   dest='aod',      action='store_true')
    parser.add_argument('-f', '--force', dest='force_rm', action='store_true')
    args = parser.parse_args()
    gTag = args.tag   
 
    data = 'MiniAOD'
    if args.aod: data = 'AOD'
    
    r.setTDRStyle()    
    collections = ['dsa', 'dgl']

    # Trees
    trees_originalFilter = []
    #trees_originalFilter.append(DTree('Cosmics_2022C_MiniAOD',              'Cosmics Run2022C MiniAOD',            dat['Cosmics_2022C']['MiniAOD-Ntuples'],              gTag, isData = False))
    trees_originalFilter.append(DTree('Cosmics_2022C_AOD',                 'Cosmics Run2022C AOD',                dat['Cosmics_2022C']['AOD-Ntuples'],                  gTag, isData = False))

    trees_nsegmentsFilter = []

    if not os.path.exists(EOSPATH+'Plots/'+args.tag):
        os.makedirs(EOSPATH+'Plots/'+args.tag)

    for dtree in trees_originalFilter + trees_nsegmentsFilter:
        dtree.merge(args.force_rm)

        if not os.path.exists(EOSPATH+'Plots/'+args.tag+'/'+dtree.name):
            os.makedirs(EOSPATH+'Plots/'+args.tag+'/'+dtree.name)

        hfile = r.TFile(dtree.targetFile)

        hists =     ["h_pt", "h_eta", "h_phi", "h_normalizedChi2", "h_dxy", "h_dz"]
        hists_log = []
        hists_eff = ["h_eff_pt", "h_eff_eta"]
        colors_1 = [[r.kMagenta+1, r.kCyan-3], [r.kAzure, r.kOrange+10]]
        colors = [r.kRed+1, r.kBlue+1]
        
        print('>> Plotting {0}'.format(dtree.name))
       
        #####           Elaborate texts that will go in Var and Eff plots          ##### 
        #------------------------------------------------------------------------------#
        texts = []
        texts.append(dtree.label)
        texts.append("Emulated DisplacedMuonFilter")
        texts.append("(minMatches=2,minPtSTA=3.5,minPtTK=3.5)")
        texts.append("NoBPTX3BX trigger, Tag ID muons")
        #------------------------------------------------------------------------------#
        
        for n,collection in enumerate(collections):
            for h in hists:
                makeVarPlot(hfile, dtree, h, args.tag, collection, names=['reco::Track({0})'.format(collection),'pat::Muon({0})'.format(collection)], color=colors[n], texts=texts, ylog=False) 
            for h in hists_log:
                makeVarPlot(hfile, dtree, h, args.tag, collection, names=['reco::Track({0})'.format(collection),'pat::Muon({0})'.format(collection)], color=colors[n], texts=texts, ylog=True)
            for h in hists_eff:
                makeEfficiencyPlot(hfile, dtree, h, args.tag, collection, names=['reco::Track({0})'.format(collection),'pat::Muon({0})'.format(collection)], color=colors_1[n], texts=texts)
            #makePlot(hfile, dtree, "h_pt_residual", args.tag, collection, name='pat::Muon({0})'.format(collection), color=r.kAzure, texts=texts, ylog=False)
        #make2DPlot(hfile, dtree, args.tag, "h_matched_IDS_2D", zlog=False, cut=False)
        print('>> DONE') 
