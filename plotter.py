import ROOT as r
from PIL import Image
from math import pi
from numpy import prod

r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)

_file = r.TFile('output.root')
_tree = _file.Get("Events")

# Print counts
hcounts = _file.Get("counts")
counts = hcounts.GetBinContent(0)
print("Events read: {counts}")

# Declare hists
h_pT = r.TH1F("h_pT", "; pT; N events", 100, 0, 200)
h_eta = r.TH1F("h_eta", "; eta, N events", 100, 0, 2.4)
h_phi = r.TH1F("h_phi", "; phi; N events", 100, -3.2, 3.2)

if False:
    for n,ev in enumerate(_tree):
        for n in range(ev.ndsa):
        
            h_pT.Fill(ev.dsa_pt[n])
            h_eta.Fill(ev.dsa_eta[n])
            h_phi.Fill(ev.dsa_phi[n])

    outfile = r.TFile("hists_dsa.root","RECREATE")
    for h in [h_pT, h_eta, h_phi]:
        h.Write()
    outfile.Close()

hist_file = r.TFile("hists_dsa.root","READ")
h_pT = hist_file.Get("h_pT")
h_eta = hist_file.Get("h_eta")
h_phi = hist_file.Get("h_phi")

h_pT.SetLineColor(r.kBlack)
l = r.TLegend(.83,.85,.97,.98)
l.AddEntry(h_pT, "DSA", "L")
c = r.TCanvas("c","",600,600)
c.cd()
c.SetLogy(1)
h_pT.Draw()
l.Draw()
c.Print("hist_pT.png")


h_eta.SetLineColor(r.kBlack)
l = r.TLegend(.83,.85,.97,.98)
l.AddEntry(h_pT, "DSA", "L")
c = r.TCanvas("c","",600,600)
c.cd()
c.SetLogy(1)
h_eta.Draw()
l.Draw()
c.Print("hist_eta.png")


h_phi.SetLineColor(r.kBlack)
l = r.TLegend(.80,.80,.87,.85)
l.AddEntry(h_pT, "DSA", "L")
c = r.TCanvas("c","",900,900)
c.cd()
c.SetLogy(0)
h_phi.Draw()
l.Draw()
c.Print("hist_phi.png")
