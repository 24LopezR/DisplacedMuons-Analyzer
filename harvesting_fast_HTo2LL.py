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


def makeVarPlot(hfiles, hname, tag, color=r.kBlue, texts=[], ylog=True):
    

    h_pre = hfiles[0].Get(hname+"_dmu_dsa")
    h_post = hfiles[1].Get(hname+"_dmu_dsa")    
    maxVal = max([h_pre.GetMaximum(), h_post.GetMaximum()])

    #### Styling pre plot
    h_pre.SetLineWidth(1)
    if ylog: 
        h_pre.SetMaximum(100*maxVal)
        h_pre.SetMinimum(1)
    else: h_pre.SetMaximum(1.2*maxVal)
    h_pre.SetLineColor(color[0])
    h_pre.SetFillColorAlpha(color[0], 0.)
    h_pre.SetLineWidth(2)
    #### Styling post plot
    h_post.SetLineWidth(1)
    if ylog: h_post.SetMaximum(10*maxVal)
    else: h_post.SetMaximum(1.2*maxVal)
    h_post.SetLineColor(color[1])
    h_post.SetFillColorAlpha(color[1], 0.)
    h_post.SetLineWidth(2)

    c = r.TCanvas(hname,hname)
    c.SetFillStyle(4000)
    c.cd()
    if ylog: c.GetPad(0).SetLogy(1)
    else: c.GetPad(0).SetLogy(0)
    
    h_pre.Draw("HIST")    
    h_post.Draw("HIST,SAME")
    
    l = r.TLegend(.60,.83,.85,.88)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.03)
    l.AddEntry(h_pre, 'Pre', "L")
    l.AddEntry(h_post, 'Post', "L")
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
    
    c.Print('{0}.png'.format(c.GetName()))
    c.Print('{0}.pdf'.format(c.GetName()))


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



    hfiles = ['hists_pre.root', 'hists_post.root']

    hfile1 = r.TFile('hists_pre.root')
    hfile2 = r.TFile('hists_post.root')

    hists =     ["h_pt", "h_eta", "h_phi", "h_normalizedChi2", "h_pt_residual"]
    hists_log = ["h_pt_100", "h_dxy", "h_dz", "h_pt_residual"]
    colors = [[r.kMagenta+1, r.kCyan-3], [r.kAzure, r.kOrange+10]]
       
    #####           Elaborate texts that will go in Var and Eff plots          ##### 
    #------------------------------------------------------------------------------#
    texts = []
    texts.append('H #rightarrow SS (400,150,4000)')
    #texts.append("DSA ID")
    #texts.append("p_{t} > 3.5 GeV")
    texts.append("No cuts applied")
    #------------------------------------------------------------------------------#
        
    for h in hists:
        makeVarPlot([hfile1, hfile2], h, args.tag, color=colors[0], texts=texts, ylog=False) 
    for h in hists_log:
        makeVarPlot([hfile1, hfile2], h, args.tag, color=colors[0], texts=texts, ylog=True)
    print('>> DONE') 
