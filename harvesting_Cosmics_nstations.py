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
    latex.DrawLatex(0.88, 0.93, "Run3 2022C cosmics data ({0})".format(data))
   
    if data == 'AOD':
        latex = r.TLatex()
        latex.SetNDC();
        latex.SetTextAngle(0);
        latex.SetTextColor(r.kBlack);
        latex.SetTextFont(42);
        latex.SetTextAlign(11);
        latex.SetTextSize(0.025);
        latex.DrawLatex(0.17, 0.83, "Emulated DisplacedMuonFilter (nstations #geq 2)".format(data))
    
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


def makeStagedPlot(hfile, tag, color=r.kBlue, ylog=True):
    
    h_track = hfile.Get('h_dxy_dsa')
    #h_filter_1 = hfile.Get('h_dxy_dmu_dsa_1')
    h_filter_2 = hfile.Get('h_dxy_dmu_dsa_2')
    #h_filter_3 = hfile.Get('h_dxy_dmu_dsa_3')
    h_muon = hfile.Get('h_dxy_dmu_dsa') # muon hist
    #hists = [h_track,h_filter_1,h_filter_2,h_filter_3,h_muon]
    hists = [h_track,h_filter_2,h_muon]
    maxVal = max([h.GetMaximum() for h in hists])

    #### Styling
    color = [r.kBlack,r.kRed+1,r.kViolet+4,r.kGreen-4,r.kPink-9]
    for i,h in enumerate(hists):
        h.SetLineWidth(1)
        if ylog: h.SetMaximum(100*maxVal)
        else: h.SetMaximum(1.2*maxVal)
        h.SetLineColor(color[i])
        h.SetFillColorAlpha(color[i], 0)
        h.SetLineStyle(1)

    c = r.TCanvas('h_staged', 'h_staged')
    c.SetFillStyle(4000)
    c.cd()
    if ylog: c.GetPad(0).SetLogy(1)
    else: c.GetPad(0).SetLogy(0)
    
    hists[0].Draw("HIST")
    for h in hists[1:]:
        h.Draw("HIST,SAME")
    
    l = r.TLegend(.50,.72,.90,.87)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.025)
    l.AddEntry(h_track, "track(DSA)", "L")
    #l.AddEntry(h_filter_1, "muon(DSA) (no filter 1)", "L")
    l.AddEntry(h_filter_2, "muon(DSA) (no filter 2)", "L")
    #l.AddEntry(h_filter_3, "muon(DSA) (no filter 3)", "L")
    l.AddEntry(h_muon, "muon(DSA)", "L")
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
    latex.DrawLatex(0.88, 0.93, "Run3 2022C cosmics data ({0})".format(data))
   
    if data == 'AOD':
        latex = r.TLatex()
        latex.SetNDC();
        latex.SetTextAngle(0);
        latex.SetTextColor(r.kBlack);
        latex.SetTextFont(42);
        latex.SetTextAlign(11);
        latex.SetTextSize(0.025);
        latex.DrawLatex(0.15, 0.86, "Emulated DisplacedMuonFilter".format(data))
        latex.DrawLatex(0.15, 0.83, "NoBPTX3BX trigger, no ID".format(data))
    
    if not os.path.exists(EOSPATH+'Plots/'+tag):
        os.makedirs(EOSPATH+'Plots/'+tag)
    c.Print(EOSPATH+'Plots/'+tag+'/h_staged_dsa.png')
    c.Print(EOSPATH+'Plots/'+tag+'/h_staged_dsa.pdf')


def makeNMatchesPlot(hfile, tag, ylog=True):
    
    h_nmatch = hfile.Get('h_numberOfMatches_dmu_dsa') # track hist
    h_nseg = hfile.Get('h_nsegments_dmu_dsa') # muon hist
    
    maxVal = max([h_nmatch.GetMaximum(), h_nseg.GetMaximum()])

    #### Styling
    h_nmatch.SetLineWidth(1)
    if ylog: h_nmatch.SetMaximum(100*maxVal)
    else: h_nmatch.SetMaximum(1.2*maxVal)
    h_nmatch.SetLineColor(r.kRed+1)
    h_nmatch.SetFillColorAlpha(r.kRed, 0)
    #### Styling muon plot
    h_nseg.SetLineWidth(1)
    if ylog: h_nseg.SetMaximum(10*maxVal)
    else: h_nseg.SetMaximum(1.2*maxVal)
    h_nseg.SetLineColor(r.kBlack)
    h_nseg.SetFillColorAlpha(r.kRed, 0)

    c = r.TCanvas('h_nmatches', 'h_nmatches')
    c.SetFillStyle(4000)
    c.cd()
    if ylog: c.GetPad(0).SetLogy(1)
    else: c.GetPad(0).SetLogy(0)
    
    h_nmatch.Draw("HIST")    
    h_nseg.Draw("HIST,SAME")
    
    l = r.TLegend(.45,.76,.90,.82)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.025)
    l.AddEntry(h_nmatch, 'numberOfMatches', "L")
    l.AddEntry(h_nseg, 'nsegments (EXO-21-006)', "L")
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
    latex.DrawLatex(0.88, 0.93, "Run3 2022C cosmics data ({0})".format(data))
   
    if data == 'AOD':
        latex = r.TLatex()
        latex.SetNDC();
        latex.SetTextAngle(0);
        latex.SetTextColor(r.kBlack);
        latex.SetTextFont(42);
        latex.SetTextAlign(11);
        latex.SetTextSize(0.025);
        latex.DrawLatex(0.17, 0.83, "muon(DSA-only)".format(data))
        latex.DrawLatex(0.17, 0.86, "No ID cuts".format(data))
    
    if not os.path.exists(EOSPATH+'Plots/'+tag):
        os.makedirs(EOSPATH+'Plots/'+tag)
    c.Print(EOSPATH+'Plots/'+tag+'/h_nmatches_dsa.png')
    c.Print(EOSPATH+'Plots/'+tag+'/h_nmatches_dsa.pdf')


def make2DPlot(hfile, title, tag, hname, zlog=False, cut=True):

    h = hfile.Get(hname)

    c = r.TCanvas(hname,hname,ww=620,wh=600)
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
    latex.DrawLatex(0.33, 0.93, "#bf{CMS} #it{Internal}")

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.03);
    latex.DrawLatex(0.87, 0.93, "Run3 2022C cosmics data ({0})".format(data))

    if not os.path.exists(EOSPATH+'Plots/'+tag):
        os.makedirs(EOSPATH+'Plots/'+tag)
    c.Print(EOSPATH+'Plots/{0}/{1}.png'.format(tag,hname))
    c.Print(EOSPATH+'Plots/{0}/{1}.pdf'.format(tag,hname))



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
    collection = 'dsa'
    makeVarPlot(hfile, 'h_dxy', args.tag, title, collection, names=['track({0})'.format(collection),'muon({0})'.format(collection)], color=r.kRed+1, ylog=True)
    makeVarPlot(hfile, 'h_pt_100', args.tag, title, collection, names=['track({0})'.format(collection),'muon({0})'.format(collection)], color=r.kRed+1, ylog=True)
    #makeFilterPlot(hfile, 'h_muons_filter', args.tag, title, color=r.kRed+1, ylog=True)
    #makeStagedPlot(hfile, args.tag, color=r.kRed+1, ylog=False)
    #makeNMatchesPlot(hfile, args.tag, ylog=True)
    make2DPlot(hfile, title, args.tag, "h_nmatches_nsegments_2D_dmu_dsa", zlog=False)
    make2DPlot(hfile, title, args.tag, "h_nsegments_nstations_2D_dmu_dsa", zlog=False, cut=False)
