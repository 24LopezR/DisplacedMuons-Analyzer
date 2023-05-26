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


def makeVarPlot(hfile_of, hfile_nf, dtree, hname, tag, names, color=r.kBlue, texts=[], ylog=True):
    
    sample = dtree.name

    h_track = hfile_nf.Get(hname+"_dsa") # track hist
    h_muon_of = hfile_of.Get(hname+"_dmu_dsa")
    h_muon_nf = hfile_nf.Get(hname+"_dmu_dsa")
    
    maxVal = max([h_track.GetMaximum(), h_muon_of.GetMaximum(), h_muon_nf.GetMaximum()])

    #### Styling track plot
    h_track.SetLineWidth(1)
    if ylog: 
        h_track.SetMaximum(100*maxVal)
        h_track.SetMinimum(1)
    else: 
        h_track.SetMaximum(1.2*maxVal)
        h_track.SetMinimum(0)
    h_track.SetLineColor(color[0])
    h_track.SetFillColorAlpha(color[0], 0.)
    h_track.SetLineWidth(2)
    #### Styling muon plot
    h_muon_of.SetLineWidth(1)
    if ylog: h_muon_of.SetMaximum(10*maxVal)
    else: h_muon_of.SetMaximum(1.2*maxVal)
    h_muon_of.SetLineColor(color[1])
    h_muon_of.SetLineWidth(2)
    #### Styling muon plot
    h_muon_nf.SetLineWidth(1)
    if ylog: h_muon_nf.SetMaximum(10*maxVal)
    else: h_muon_nf.SetMaximum(1.2*maxVal)
    h_muon_nf.SetLineColor(color[2])
    h_muon_nf.SetLineWidth(2)

    c = r.TCanvas(sample+'_'+hname, sample+'_'+hname)
    c.SetFillStyle(4000)
    c.cd()
    if ylog: c.GetPad(0).SetLogy(1)
    else: c.GetPad(0).SetLogy(0)
    
    h_track.Draw("HIST")    
    h_muon_of.Draw("HIST,SAME")
    h_muon_nf.Draw("HIST,SAME")
    
    l = r.TLegend(.46,.80,.82,.88)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.03)
    l.AddEntry(h_track, names[0], "L")
    l.AddEntry(h_muon_of, names[1], "L")
    l.AddEntry(h_muon_nf, names[2], "L")
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


def makeRatioPlot(hfile_of, hfile_nf, dtree, hname, tag, names, color=r.kBlue, texts=[], ylog=True):
    
    sample = dtree.name
    c = r.TCanvas(sample+'_'+hname, sample+'_'+hname)
    c.SetFillStyle(4000)
    c.cd()
    ## Create tha pads
    pad1 = r.TPad("pad1", "pad1", 0, 0.3, 1, 1.0) # for the plot
    pad1.SetBottomMargin(0.015)
    pad1.SetTopMargin(0.13)
    pad1.Draw()                                     
    pad2 = r.TPad("pad2", "pad2", 0, 0.01, 1, 0.3) # for the ratio
    pad2.SetTopMargin(0.05);
    pad2.SetBottomMargin(0.4);
    #pad2.SetGridy(1);
    pad2.Draw();
 
    if ylog: pad1.SetLogy(1)
    else: pad1.SetLogy(0)

    ### Draw hists ---------------------------------------------------------------------------
    pad1.cd()

    h_track = hfile_nf.Get(hname+"_dsa") # track hist
    h_muon_of = hfile_of.Get(hname+"_dmu_dsa")
    h_muon_nf = hfile_nf.Get(hname+"_dmu_dsa")
    
    maxVal = max([h_track.GetMaximum(), h_muon_of.GetMaximum(), h_muon_nf.GetMaximum()])

    #### Styling track plot
    h_track.SetLineWidth(1)
    if ylog: 
        h_track.SetMaximum(100*maxVal)
        h_track.SetMinimum(1)
    else: 
        h_track.SetMaximum(1.2*maxVal)
        h_track.SetMinimum(0)
    h_track.SetLineColor(color[0])
    h_track.SetFillColorAlpha(color[0], 0.)
    h_track.SetLineWidth(2)
    #### Styling muon plot
    h_muon_of.SetLineWidth(1)
    if ylog: h_muon_of.SetMaximum(10*maxVal)
    else: h_muon_of.SetMaximum(1.2*maxVal)
    h_muon_of.SetLineColor(color[1])
    h_muon_of.SetLineWidth(2)
    #### Styling muon plot
    h_muon_nf.SetLineWidth(1)
    if ylog: h_muon_nf.SetMaximum(10*maxVal)
    else: h_muon_nf.SetMaximum(1.2*maxVal)
    h_muon_nf.SetLineColor(color[2])
    h_muon_nf.SetLineWidth(2)

    ## General style
    hists = [h_track,h_muon_of,h_muon_nf]
    for h in hists:
        h.GetYaxis().SetTitleSize(0.045)
        h.GetYaxis().SetTitleOffset(1.25);
        h.GetXaxis().SetLabelSize(0)
        h.GetYaxis().SetLabelSize(0.04)

    h_track.Draw("HIST")    
    h_muon_of.Draw("HIST,SAME")
    h_muon_nf.Draw("HIST,SAME")
    
    l = r.TLegend(.48,.70,.82,.80)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.03)
    l.AddEntry(h_track, names[0], "L")
    l.AddEntry(h_muon_of, names[1], "L")
    l.AddEntry(h_muon_nf, names[2], "L")
    l.SetBorderSize(0)
    l.Draw()
     
    latex = r.TLatex()
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(r.kBlack);
    latex.SetTextFont(42);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.045);
    latex.DrawLatex(0.17, 0.80, "#bf{CMS} #it{Simulation}")
    latex.SetTextSize(0.03);
    for n,t in enumerate(texts):
        latex.DrawLatex(0.17, 0.75-0.03*n, t)
    
    pad1.Update()
    pad1.RedrawAxis()
    #aux_frame = TLine()
    #aux_frame.SetLineWidth(2) 
    #aux_frame.DrawLine(pad1.GetUxmax(), pad1.GetUymin(), pad1.GetUxmax(), maxYAxisValue);

    ### Draw ratios ----------------------------------------------------------------------------
    pad2.cd()

    ratio_of = h_muon_of.Clone(h_muon_of.GetName()+'_ratio')
    ratio_nf = h_muon_nf.Clone(h_muon_nf.GetName()+'_ratio')
    ratios = [ratio_of, ratio_nf]
    for i,rat in enumerate(ratios):
        rat.Divide(h_track)
        rat.GetYaxis().SetRangeUser(0.9*rat.GetMinimum(), 1.2);
        rat.GetYaxis().SetTitle('Muon/Track');
        rat.GetYaxis().CenterTitle()
        rat.GetYaxis().SetLabelSize(0.10);
        rat.GetYaxis().SetNdivisions(4);
        rat.GetYaxis().SetTitleOffset(0.5);
        rat.GetXaxis().SetLabelSize(0.10);
        rat.GetYaxis().SetTitleSize(0.11);
        rat.GetXaxis().SetTitleSize(0.12);
        rat.GetXaxis().SetLabelOffset(0.02);
        rat.SetMarkerStyle(20);
        rat.SetMarkerSize(0.8);
        rat.SetMarkerColor(color[i+1]);
        rat.SetLineColor(color[i+1]);
        rat.SetLineWidth(2);
    ratio_of.Draw("AXIS")
    xmin = ratio_of.GetBinLowEdge(1)
    xmax = ratio_of.GetBinLowEdge(ratio_of.GetNbinsX()+1)
    line = r.TLine(xmin,1,xmax,1)
    line.SetLineColor(r.kGray+2);
    line.SetLineWidth(2);
    line.Draw(' ')
    ratio_of.Draw("P,SAME")
    ratio_nf.Draw("P,SAME")

    pad2.Update()
    pad2.RedrawAxis()

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
    trees_originalFilter.append(DTree('HTo2LongLived_400_150_4000','H #rightarrow SS (400,150,4000)', dat['HTo2LongLived_400_150_4000']['MiniAOD-Ntuples'], gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_1300', 'H #rightarrow SS (125,20,1300)',  dat['HTo2LongLived_125_20_1300']['MiniAOD-Ntuples'],  gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_130',  'H #rightarrow SS (125,20,130)',   dat['HTo2LongLived_125_20_130']['MiniAOD-Ntuples'],   gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_13',   'H #rightarrow SS (125,20,13)',    dat['HTo2LongLived_125_20_13']['MiniAOD-Ntuples'],    gTag, isData = False))

    trees_nsegmentsFilter = []
    trees_nsegmentsFilter.append(DTree('HTo2LongLived_400_150_4000_nseg2','H #rightarrow SS (400,150,4000)', dat['HTo2LongLived_400_150_4000']['MiniAOD-Ntuples_nsegments2'], gTag, isData = False))
    trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_1300_nseg2', 'H #rightarrow SS (125,20,1300)',  dat['HTo2LongLived_125_20_1300']['MiniAOD-Ntuples_nsegments2'],  gTag, isData = False))
    trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_130_nseg2',  'H #rightarrow SS (125,20,130)',   dat['HTo2LongLived_125_20_130']['MiniAOD-Ntuples_nsegments2'],   gTag, isData = False))
    trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_13_nseg2',   'H #rightarrow SS (125,20,13)',    dat['HTo2LongLived_125_20_13']['MiniAOD-Ntuples_nsegments2'],    gTag, isData = False))

    if not os.path.exists(EOSPATH+'Plots/'+args.tag):
        os.makedirs(EOSPATH+'Plots/'+args.tag)

    for i,dtree in enumerate(trees_originalFilter):
        dtree.merge(args.force_rm)
        trees_nsegmentsFilter[i].merge(args.force_rm)

        if not os.path.exists(EOSPATH+'Plots/'+args.tag+'/'+dtree.name):
            os.makedirs(EOSPATH+'Plots/'+args.tag+'/'+dtree.name)

        hfile_oldFilter = r.TFile(dtree.targetFile)
        hfile_newFilter = r.TFile(trees_nsegmentsFilter[i].targetFile)
      
        hists =     ["h_pt", "h_eta", "h_phi", "h_normalizedChi2"]
        hists_log = ["h_pt_100", "h_dxy", "h_dz"]
        hists_eff = ["h_eff_pt", "h_eff_eta", "h_eff_Lxy_300", "h_eff_pt_resptcut", "h_eff_eta_resptcut", "h_eff_Lxy_resptcut"]
        colors = [r.kBlack, r.kOrange+10, r.kBlue-3]
        names = ['reco::Track (DSA)','pat::Muon (DSA) (orig. filter)','pat::Muon (DSA) (new filter)']       
 
        print('>> Plotting {0}'.format(dtree.name))
       
        #####           Elaborate texts that will go in Var and Eff plots          ##### 
        #------------------------------------------------------------------------------#
        texts = []
        texts.append(dtree.label)
        #if 'nseg2' in dtree.name: texts.append(r'(nsegments #geq 2)')
        #else: texts.append(r'(numberOfMatches #geq 2)')
        #texts.append("DSA ID")
        #texts.append("p_{t} > 3.5 GeV")
        texts.append("No cuts applied")
        #------------------------------------------------------------------------------#
        
        for h in hists:
            makeVarPlot(hfile_oldFilter, hfile_newFilter, dtree, h, args.tag, names=names, color=colors, texts=texts, ylog=False) 
        for h in hists_log:
            makeVarPlot(hfile_oldFilter, hfile_newFilter, dtree, h, args.tag, names=names, color=colors, texts=texts, ylog=True)
        for h in hists_eff:
            makeEfficiencyPlot(hfile_oldFilter, hfile_newFilter, dtree, h, args.tag, names=names, color=colors, texts=texts)
        makeRatioPlot(hfile_oldFilter, hfile_newFilter, dtree, "h_pt_residual", args.tag, names=names, color=colors, texts=texts, ylog=False)
        print('>> DONE') 
