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

def makeVarPlot(hfile, dtree, hname, tag, title, collection, names, color=r.kBlue, ylog=True):
    
    sample = dtree.name
    label = dtree.label
    if 'nseg2' in sample: label += ' (nsegments #geq 2)'
    else: label += ' (numberOfMatches #geq 2)'

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

    c = r.TCanvas(sample+'_'+hname+'_'+collection, sample+'_'+hname+'_'+collection)
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
    latex.DrawLatex(0.15, 0.93, "#bf{CMS} #it{Simulation}")
   
    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.025);
    latex.DrawLatex(0.17, 0.86, label)
    #latex.DrawLatex(0.17, 0.83, "DisplacedMuonFilter (numberOfMatches #geq 2)")
    latex.DrawLatex(0.17, 0.83, "No ID cuts")
    
    if not os.path.exists(EOSPATH+'Plots/'+tag):
        os.makedirs(EOSPATH+'Plots/'+tag)
    c.Print(EOSPATH+'Plots/'+tag+'/'+c.GetName()+".png")
    c.Print(EOSPATH+'Plots/'+tag+'/'+c.GetName()+".pdf")

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
    latex.DrawLatex(0.33, 0.93, "#bf{CMS} #it{Simulation}")

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.03);
    latex.DrawLatex(0.87, 0.93, label)

    if not os.path.exists(EOSPATH+'Plots/'+tag):
        os.makedirs(EOSPATH+'Plots/'+tag)
    c.Print(EOSPATH+'Plots/{0}/{1}.png'.format(tag,c.GetName()))
    c.Print(EOSPATH+'Plots/{0}/{1}.pdf'.format(tag,c.GetName()))


if __name__ == '__main__':

    r.gROOT.ProcessLine('.L ./include/tdrstyle.C')
    r.gROOT.SetBatch(1)
    print('WORKPATH: ' + WORKPATH)

    r.gStyle.SetPaintTextFormat("3.2f")
    parser = ArgumentParser()
    parser.add_argument('-t', '--tag', dest='tag')
    parser.add_argument('-a', '--aod', dest='aod', action='store_true')
    args = parser.parse_args()
    gTag = args.tag   
 
    data = 'MiniAOD'
    if args.aod: data = 'AOD'
    
    r.setTDRStyle()    
    collections = ['dsa', 'dgl']

    # Trees
    trees_originalFilter = []
    trees_originalFilter.append(DTree('HTo2LongLived_400_150_4000','H #rightarrow SS (400,150,4000)', dat['HTo2LongLived_400_150_4000']['MiniAOD-Ntuples'], gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_1300', 'H #rightarrow SS (125,20,1300)',  dat['HTo2LongLived_125_20_1300']['MiniAOD-Ntuples'],  gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_130',  'H #rightarrow SS (125,20,130)',   dat['HTo2LongLived_125_20_130']['MiniAOD-Ntuples'],   gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_13',   'H #rightarrow SS (125,20,13)',    dat['HTo2LongLived_125_20_13']['MiniAOD-Ntuples'],    gTag, isData = False))

    trees_nsegmentsFilter = []
    trees_nsegmentsFilter.append(DTree('HTo2LongLived_400_150_4000_nseg2','H #rightarrow SS (400,150,4000)', dat['HTo2LongLived_400_150_4000']['MiniAOD-Ntuples_nsegments2'], gTag, isData = False))
    trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_1300_nseg2', 'H #rightarrow SS (125,20,1300)',  dat['HTo2LongLived_125_20_1300']['MiniAOD-Ntuples_nsegments2'],  gTag, isData = False))
    trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_130_nseg2',  'H #rightarrow SS (125,20,130)',   dat['HTo2LongLived_125_20_130']['MiniAOD-Ntuples_nsegments2'],   gTag, isData = False))
    trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_13_nseg2',   'H #rightarrow SS (125,20,13)',    dat['HTo2LongLived_125_20_13']['MiniAOD-Ntuples_nsegments2'],    gTag, isData = False))

    for dtree in trees_originalFilter:
        dtree.merge()
        hfile = r.TFile(dtree.targetFile)

        title = ''
        hists =     ["h_pt", "h_eta", "h_phi", "h_normalizedChi2"]
        hists_log = ["h_pt_100", "h_dxy", "h_dz"]
        colors = [r.kMagenta+1, r.kCyan-4]
        
        print('>> Plotting {0}'.format(dtree.name))
        for n,collection in enumerate(collections):
            #for h in hists:
            #    makeVarPlot(hfile, dtree, h, args.tag, title, collection, names=['track({0})'.format(collection),'muon({0})'.format(collection)], color=colors[n], ylog=False) 
            for h in hists_log:
                makeVarPlot(hfile, dtree, h, args.tag, title, collection, names=['track({0})'.format(collection),'muon({0})'.format(collection)], color=colors[n], ylog=True)
            make2DPlot(hfile, dtree, args.tag, "h_nmatches_nsegments_2D_dmu_dsa", zlog=False)
            make2DPlot(hfile, dtree, args.tag, "h_nsegments_nstations_2D_dmu_dsa", zlog=False, cut=False)
        print('>> DONE')
    
    for dtree in trees_nsegmentsFilter:
        dtree.merge()
        hfile = r.TFile(dtree.targetFile)

        title = ''
        hists =     ["h_pt", "h_eta", "h_phi", "h_normalizedChi2"]
        hists_log = ["h_pt_100", "h_dxy", "h_dz"]
        colors = [r.kMagenta+1, r.kCyan-4]
        
        print('>> Plotting {0}'.format(dtree.name))
        for n,collection in enumerate(collections):
            #for h in hists:
            #    makeVarPlot(hfile, dtree, h, args.tag, title, collection, names=['track({0})'.format(collection),'muon({0})'.format(collection)], color=colors[n], ylog=False) 
            for h in hists_log:
                makeVarPlot(hfile, dtree, h, args.tag, title, collection, names=['track({0})'.format(collection),'muon({0})'.format(collection)], color=colors[n], ylog=True)
            make2DPlot(hfile, dtree, args.tag, "h_nmatches_nsegments_2D_dmu_dsa", zlog=False)
            make2DPlot(hfile, dtree, args.tag, "h_nsegments_nstations_2D_dmu_dsa", zlog=False, cut=False)
        print('>> DONE')
