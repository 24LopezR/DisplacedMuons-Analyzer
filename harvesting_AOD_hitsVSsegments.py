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

def makeEfficiencyPlot(hfile_of, hfile_nf, dtree, hname, tag, names, color=r.kBlue+1, texts=[]):

    sample = dtree.name

    h_track = hfile_nf.Get(hname+"_dsa")
    h_muon_of = hfile_of.Get(hname+"_dmu_dsa")
    h_muon_nf = hfile_nf.Get(hname+"_dmu_dsa")

    c = r.TCanvas(sample+'_'+hname, sample+'_'+hname)
    c.cd()

    h_track.Draw("PA")
    h_muon_of.Draw("P,SAME")
    h_muon_nf.Draw("P,SAME")

    c.Update()
    #### Styling track plot
    h_track.SetLineWidth(1)
    h_track.SetLineColor(color[0])
    h_track.SetMarkerColor(color[0])
    h_track.SetMarkerStyle(20)
    _g = h_track.GetPaintedGraph()
    _g.SetMinimum(0)
    _g.SetMaximum(1.2)
    #### Styling muon plot
    h_muon_of.SetLineWidth(1)
    h_muon_of.SetLineColor(color[1])
    h_muon_of.SetMarkerColor(color[1])
    h_muon_of.SetMarkerStyle(20)
    #### Styling muon plot
    h_muon_nf.SetLineWidth(1)
    h_muon_nf.SetLineColor(color[2])
    h_muon_nf.SetMarkerColor(color[2])
    h_muon_nf.SetMarkerStyle(20)

    l = r.TLegend(.46,.80,.82,.88)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.03)
    l.AddEntry(h_track, names[0], "P")
    l.AddEntry(h_muon_of, names[1], "P")
    l.AddEntry(h_muon_nf, names[2], "P")
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
    latex.SetTextAlign(11);
    latex.SetTextSize(0.03);
    for n,t in enumerate(texts):
        latex.DrawLatex(0.17, 0.86-0.03*n, t)

    c.Print(EOSPATH+'Plots/{0}/{1}/{2}.png'.format(tag,dtree.name,c.GetName()))
    c.Print(EOSPATH+'Plots/{0}/{1}/{2}.pdf'.format(tag,dtree.name,c.GetName()))


def makeVarPlot(hfile, dtree, hname, tag, names, color=r.kBlue, texts=[], ylog=True, cut=False):
    
    h = hfile.Get(hname)
    
    maxVal = h.GetMaximum()

    #### Styling plot
    h.SetLineWidth(1)
    if ylog: 
        h.SetMaximum(100*maxVal)
        h.SetMinimum(1)
    else: 
        h.SetMaximum(1.2*maxVal)
        h.SetMinimum(0)
    h.SetLineColor(color)
    h.SetFillColorAlpha(color, 0.)
    h.SetLineWidth(2)

    c = r.TCanvas(hname,hname)
    c.SetFillStyle(4000)
    c.cd()
    if ylog: c.GetPad(0).SetLogy(1)
    else: c.GetPad(0).SetLogy(0)
    
    h.Draw("HIST")    
    
    l = r.TLegend(.46,.80,.82,.88)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.03)
    l.AddEntry(h, names[0], "L")
    l.SetBorderSize(0)
    l.Draw()
    
    if cut:
        line = r.TLine(cut,0,cut,h.GetMaximum())
        line.SetLineColor(r.kRed)
        line.Draw()

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


def make2DPlot(hfile, dtree, tag, hname, zlog=False, cut=True):

    sample = dtree.name
    label = dtree.label + ' (AOD)'

    h = hfile.Get(hname)

    c = r.TCanvas(sample+'_'+hname,sample+'_'+hname,ww=620,wh=600)
    c.SetFillStyle(4000)
    c.cd()
    if zlog: c.SetLogz(1)
    else: c.SetLogz(0)

    h.GetXaxis().SetRange(1,10)
    h.GetYaxis().SetRange(1,50)
    h.Draw("COLZ,TEXT")

    if cut:
        liney = r.TLine(2,0,2,50)
        liney.SetLineColor(r.kRed)
        liney.Draw()
        linex = r.TLine(0,13,10,13)
        linex.SetLineColor(r.kRed)
        linex.Draw()

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.14, 0.93, "#bf{CMS} #it{Simulation}")

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.03);
    latex.DrawLatex(0.88, 0.93, label)

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

    # Trees
    trees_originalFilter = []
    trees_originalFilter.append(DTree('HTo2LongLived_400_150_4000','H #rightarrow SS (400,150,4000)', dat['HTo2LongLived_400_150_4000']['AOD-Ntuples'], gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_1300', 'H #rightarrow SS (125,20,1300)',  dat['HTo2LongLived_125_20_1300']['AOD-Ntuples'],  gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_130',  'H #rightarrow SS (125,20,130)',   dat['HTo2LongLived_125_20_130']['AOD-Ntuples'],   gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_13',   'H #rightarrow SS (125,20,13)',    dat['HTo2LongLived_125_20_13']['AOD-Ntuples'],    gTag, isData = False))

    trees_nsegmentsFilter = []
    #trees_nsegmentsFilter.append(DTree('HTo2LongLived_400_150_4000_nseg2','H #rightarrow SS (400,150,4000)', dat['HTo2LongLived_400_150_4000']['MiniAOD-Ntuples_nsegments2'], gTag, isData = False))
    #trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_1300_nseg2', 'H #rightarrow SS (125,20,1300)',  dat['HTo2LongLived_125_20_1300']['MiniAOD-Ntuples_nsegments2'],  gTag, isData = False))
    #trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_130_nseg2',  'H #rightarrow SS (125,20,130)',   dat['HTo2LongLived_125_20_130']['MiniAOD-Ntuples_nsegments2'],   gTag, isData = False))
    #trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_13_nseg2',   'H #rightarrow SS (125,20,13)',    dat['HTo2LongLived_125_20_13']['MiniAOD-Ntuples_nsegments2'],    gTag, isData = False))

    if not os.path.exists(EOSPATH+'Plots/'+args.tag):
        os.makedirs(EOSPATH+'Plots/'+args.tag)

    for i,dtree in enumerate(trees_originalFilter):
        dtree.merge(args.force_rm)

        if not os.path.exists(EOSPATH+'Plots/'+args.tag+'/'+dtree.name):
            os.makedirs(EOSPATH+'Plots/'+args.tag+'/'+dtree.name)

        hfile = r.TFile(dtree.targetFile)
 
        print('>> Plotting {0}'.format(dtree.name))
         
        make2DPlot(hfile, dtree, gTag, "h_nsegments_nhits_2D", zlog=False, cut=True)
        makeVarPlot(hfile, dtree, "h_pt", gTag, [dtree.name], color=r.kBlue, texts=["AOD"], cut=3.5)
        makeVarPlot(hfile, dtree, "h_normChi2", gTag, [dtree.name], color=r.kBlue, texts=["AOD"], cut=2.5)
        makeVarPlot(hfile, dtree, "h_ptError", gTag, [dtree.name], color=r.kBlue, texts=["AOD"], cut=1.)
        print('>> DONE') 
