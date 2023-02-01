import ROOT as r
import os
from math import pi
import numpy as np
from argparse import ArgumentParser
from include.PlotHandler import PlotHandler

#r.gStyle.SetLabelFont(42)
################################# GLOBAL VARIABLES DEFINITION ####################################

runningfile = os.path.abspath(__file__)
WORKPATH = ''
for level in runningfile.split('/')[:-1]:
    WORKPATH += level
    WORKPATH += '/'

def makeDSANmuonsPlot(hfile, tag, title):

    hists = []
    hists.append(hfile.Get('h_muons_dsa'))
    hists.append(hfile.Get('h_muons_up_dsa'))
    hists.append(hfile.Get('h_muons_down_dsa'))

    #### Styling
    colors = [r.kBlue-3, r.kRed-3, r.kGreen-3]
    maxVal = max([h.GetMaximum() for h in hists])
    for n,h in enumerate(hists):
        h.SetMaximum(1.2*maxVal)
        h.SetLineWidth(1)
        h.SetLineColor(colors[n])
        #h.GetXaxis().SetTitleSize(0.045)
        #h.GetXaxis().SetLabelSize(0.03)
        #h.GetYaxis().SetTitleSize(0.045)
        #h.GetYaxis().SetTitleOffset(1.25)
        #h.GetYaxis().SetLabelSize(0.03)
        h.SetFillColorAlpha(colors[n], 0.25)
        h.SetTitle(title)   
 
    c = r.TCanvas('c','c')
    c.cd()
    c.SetLogy(0)

    hists[0].Draw()
    for h in hists[1:]: h.Draw("SAME")

    l = r.TLegend(.65,.75,.90,.87)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.03)
    names = ['DSA muons','DSA muons (#phi>0)','DSA muons (#phi<0)']
    for n,h in enumerate(hists):
        l.AddEntry(h, names[n], "L")
    l.SetBorderSize(0)
    l.Draw()

    if not os.path.exists('output/'+tag):
        os.makedirs('output/'+tag)
    c.Print('output/'+tag+'/h_nmuons.png')
    print('File h_nmuons.png created')



def makeEfficiencyPlot(hifile, hname, title, tag, collection, color=r.kBlue+1, ylog=False):
    
    h = hfile.Get(hname+"_"+collection)

    c = r.TCanvas("c","c")
    c.cd()
    if ylog: c.SetLogy(1)
    else: c.SetLogy(0)
    
    h.Draw()    
   
    c.Update() 
    #### Styling
    h.SetLineWidth(1)
    h.SetLineColor(color) 
    h.SetMarkerColor(color)
    h.SetMarkerStyle(20)
    h.SetTitle(title)
    _g = h.GetPaintedGraph()
    _g.SetMinimum(0)
    _g.SetMaximum(1.2)
    _g.GetYaxis().SetTitle('Efficiency')
        
    '''
    l = r.TLegend(.60,.32,.85,.40)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.025)
    l.AddEntry(h, name, "P")
    l.SetBorderSize(0)
    l.Draw()
    '''

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.35, 0.93, "#bf{CMS} #it{Internal}")

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.90, 0.93, "Run3 2022C cosmics data")
    
    if not os.path.exists('output/'+tag):
        os.makedirs('output/'+tag)
    c.Print('output/'+tag+'/'+hname+collection+".png")
    print('File '+hname+'.png created')



def make2DEfficiencyPlot(hifile, hname, title, tag, collection, ylog=False):
    
    h = hfile.Get(hname+'_'+collection)

    c = r.TCanvas("c","c")
    c.cd()
    if ylog: c.SetLogy(1)
    else: c.SetLogy(0)
    
    h.Draw("COLZ,TEXT")    
   
    c.Update() 
    #### Styling
    #colors = [r.kRed+1, r.kBlue+1]
    #h.SetLineWidth(1)
    #h.SetLineColor(colors[n]) 
    #h.SetMarkerColor(colors[n])
    #h.SetMarkerStyle(20)
    #h.SetTitle(title)
    #_g = h.GetPaintedGraph()
    #_g.SetMinimum(0)
    #_g.SetMaximum(1.2)
    #_g.GetYaxis().SetTitle('Efficiency')
        
    '''
    l = r.TLegend(.60,.32,.85,.40)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.025)
    for n,h in enumerate(hists):
        l.AddEntry(h, n, "P")
    l.SetBorderSize(0)
    l.Draw()
    '''

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.35, 0.93, "#bf{CMS} #it{Internal}")

    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(0.04);
    latex.DrawLatex(0.90, 0.93, "Run3 2022C cosmics data")
    
    if not os.path.exists('output/'+tag):
        os.makedirs('output/'+tag)
    c.Print('output/'+tag+'/'+hname+".png")
    print('File '+hname+'.png created')


def makeVarPlot(hifile, hname, tag, title, collections, names=['DSA'], ylog=True):
    
    hists = []
    for c in collections:
        hists.append(hfile.Get(hname+"_"+c))
    
    for h in hists: h.Scale(1/h.Integral())
    maxVal = max([h.GetMaximum() for h in hists])

    #### Styling
    colors = [r.kRed+1, r.kBlue+1]
    for n,h in enumerate(hists):
        h.SetLineWidth(1)
        h.SetLineColor(colors[n])
        #h.GetXaxis().SetTitleSize(0.045)
        #h.GetXaxis().SetLabelSize(0.03)
        #h.GetYaxis().SetTitleSize(0.045)
        #h.GetYaxis().SetTitleOffset(1.25)
        #h.GetYaxis().SetLabelSize(0.03)
        h.SetFillColorAlpha(colors[n], 0.5)
        h.SetTitle(title)
        h.SetMaximum(1.2*maxVal)

    c = r.TCanvas(hname, hname)
    c.cd()
    if ylog: c.GetPad(0).SetLogy(1)
    else: c.GetPad(0).SetLogy(0)
    
    hists[0].Draw("HIST")    
    for h in hists[1:]: h.Draw("HIST,SAME")
    
    l = r.TLegend(.70,.80,.90,.87)
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

    r.gROOT.ProcessLine('.L ./include/tdrstyle.C')
    r.gROOT.SetBatch(1)
    print('WORKPATH: ' + WORKPATH)
    #r.setTDRStyle()    


    parser = ArgumentParser()
    parser.add_argument('-m', '--mode', dest='mode')
    parser.add_argument('-c', '--cuts', dest='cuts_filename')
    parser.add_argument('-t', '--tag', dest='tag')
    args = parser.parse_args()
    MODE = args.mode
    
    ############## PLOT TITLE #########################################
    title = ''
    ###################################################################

    collections = ['dsa', 'dgl']
    histfilename = '/afs/cern.ch/user/r/rlopezru/private/ntuplizer_test/CMSSW_12_4_0/src/Analysis/Analyzer/hists/hists_'+args.tag+'.root'
    with open(args.cuts_filename, 'r') as f:
        cuts_selection = ''.join(f.readlines())

    if MODE == "fill":
        
        _filedir = '/eos/user/r/rlopezru/Cosmics/NoBPTX/CosmicsAnalysis_Run2022C/230131_152319/0000/'
        _files = []
        for name in os.listdir(_filedir):
            if '.root' in name: _files.append(r.TFile(_filedir+name))
        _trees = [_f.Get("Events") for _f in _files]
        '''
        ### Interactive mode
        _files = [r.TFile('../first-Ntuplizer/Cosmics_Run2022C.root')]
        _trees = [_f.Get("Events") for _f in _files]
        '''
        # Print counts
        hcounts = _files[0].Get("counts")
        counts = hcounts.GetBinContent(0)
        print('Events in Ttree: {counts}'.format(counts=counts))
        
        outdir = './'
  
        pltHandle = PlotHandler(outdir, histfilename, collections, cuts_selection)
        for n,_tree in enumerate(_trees):
            print('Processing tree '+str(_files[n]))
            for i,ev in enumerate(_tree):
                #if i>=300000: continue
                if i%10000==0: print('>> {0} events processed'.format(i)) 
                pltHandle.processEvent(ev)
        pltHandle.write()

    if MODE == "plot":
        colors = [r.kRed+1, r.kBlue+1]
        hfile = r.TFile(histfilename)
        hists = ["h_muons", "h_muons_down", "h_muons_up", "h_pt", "h_eta", "h_phi", "h_dxy", "h_dz", "h_Nhits", "h_NDThits", "h_normalizedChi2"]
        hists_eff = ["h_eff_pt", "h_eff_eta", "h_eff_dxy", "h_eff_dz"]
        hists_log = ["h_cosalpha", "h_dPhi", "h_dEta"]
        for h in hists:
            makeVarPlot(hfile, h, args.tag, title, collections, names=[c.upper() for c in collections], ylog=False)
        for h in hists_log:
            makeVarPlot(hfile, h, args.tag, title, collections, names=[c.upper() for c in collections], ylog=True)
        for n,collection in enumerate(collections):
            for h in hists_eff:
                makeEfficiencyPlot(hfile, h, title, args.tag, collection, color=colors[n], ylog=False)
            make2DEfficiencyPlot(hfile, "h_eff_2D", title, args.tag, collection, ylog=False)
        makeDSANmuonsPlot(hfile, args.tag, title)
