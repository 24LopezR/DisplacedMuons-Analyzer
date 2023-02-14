import ROOT as r
import os
from math import pi
import numpy as np
from argparse import ArgumentParser
from include.PlotHandler import PlotHandler
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

def makeVarPlot(hifile, hname1, hname2, tag, title, collection, names, ylog=True):
    
    hists = []
    hists.append(hfile.Get(hname1+"_"+collection))
    hists.append(hfile.Get(hname2+"_"+collection))
    
    for h in hists: h.Scale(1/h.Integral())
    maxVal = max([h.GetMaximum() for h in hists])

    #### Styling
    if collection=='dsa': colors = [r.kRed+1, r.kRed+4]
    if collection=='dgl': colors = [r.kBlue+1, r.kBlue+4]
    for n,h in enumerate(hists):
        h.SetLineWidth(1)
        h.SetLineColor(colors[n])
        h.SetFillColorAlpha(colors[n], 0.1)
        h.GetYaxis().SetTitle('Fraction of events')
        h.SetTitle(title)
        h.SetMaximum(100*maxVal)

    c = r.TCanvas(hname1, hname1)
    c.cd()
    if ylog: c.SetLogy(1)
    else: c.SetLogy(0)
    
    hists[0].Draw("HIST")    
    for h in hists[1:]: h.Draw("HIST,SAME")
    
    l = r.TLegend(.50,.80,.90,.87)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.03)
    for n,h in enumerate(hists):
        l.AddEntry(h, names[n], "L")
    l.SetBorderSize(0)
    l.Draw()

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.32, 0.93, "#bf{CMS} #it{Internal}")    

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.88, 0.93, "Run3 2022C Cosmics Data") 
    
    if not os.path.exists(EOSPATH+'Plots/'+tag):
        os.makedirs(EOSPATH+'Plots/'+tag)
    c.Print(EOSPATH+'Plots/'+tag+'/h_eta_split_'+collection+'.png')
    c.Print(EOSPATH+'Plots/'+tag+'/h_eta_split_'+collection+'.pdf')


def makeQpTPlot(hifile, hname1, tag, title, collection, names, ylog=True):
    
    hists = []
    hists.append(hfile.Get(hname1+"_"+collection))
    
    for h in hists: h.Scale(1/h.Integral())
    maxVal = max([h.GetMaximum() for h in hists])

    #### Styling
    if collection=='dsa': color = [r.kRed+1]
    if collection=='dgl': color = [r.kBlue+1]
    for n,h in enumerate(hists):
        h.SetLineWidth(1)
        h.SetLineColor(color[n])
        h.SetFillColorAlpha(color[n], 0.1)
        h.GetYaxis().SetTitle('Fraction of events')
        h.SetTitle(title)
        h.SetMaximum(100*maxVal)

    c = r.TCanvas(hname1, hname1)
    c.cd()
    if ylog: c.SetLogy(1)
    else: c.SetLogy(0)
    
    hists[0].Draw("HIST")    
    for h in hists[1:]: h.Draw("HIST,SAME")
    
    l = r.TLegend(.50,.80,.90,.87)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.03)
    for n,h in enumerate(hists):
        l.AddEntry(h, names[n], "L")
    l.SetBorderSize(0)
    l.Draw()

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.32, 0.93, "#bf{CMS} #it{Internal}")    

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.88, 0.93, "Run3 2022C Cosmics Data") 

    if not os.path.exists(EOSPATH+'Plots/'+tag):
        os.makedirs(EOSPATH+'Plots/'+tag)
    c.Print(EOSPATH+'Plots/'+tag+'/h_qpt_'+collection+'.png')
    c.Print(EOSPATH+'Plots/'+tag+'/h_qpt_'+collection+'.pdf')


if __name__ == '__main__':

    r.gROOT.ProcessLine('.L ./include/tdrstyle.C')
    r.gROOT.SetBatch(1)
    print('WORKPATH: ' + WORKPATH)

    r.gStyle.SetPaintTextFormat("3.2f")
    parser = ArgumentParser()
    parser.add_argument('-t', '--tag', dest='tag')
    args = parser.parse_args()
    
    r.setTDRStyle()    
    collections = ['dsa', 'dgl']
    
    launch = Launcher(None, args.tag, collections, None)
    hfilename = launch.mergeHists()
    colors = [r.kRed+1, r.kBlue+1]
    hfile = r.TFile(hfilename)
    for collection in collections:
        makeVarPlot(hfile, 'h_eta_down', 'h_eta_up', args.tag, '', collection, names=[collection.upper()+' muons (#phi<0)', collection.upper()+' muons (#phi>0)'], ylog=True)
        makeQpTPlot(hfile, 'h_charge_pt', args.tag, '', collection, names=[collection.upper()+' muons'], ylog=True)
