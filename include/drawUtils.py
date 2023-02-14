import ROOT as r
import os


class Canvas:

    def __init__(self, name):
        self.canvas = r.TCanvas(name, name)


    def drawHist(h, options=""):
        h.Draw(options)


    def addCMSLatex(text):
        latex = r.TLatex()
        latex.SetNDC();
        latex.SetTextAngle(0);
        latex.SetTextColor(r.kBlack);
        latex.SetTextFont(42);
        latex.SetTextAlign(31);
        latex.SetTextSize(0.04);
        latex.DrawLatex(0.35, 0.93, "#bf{CMS} #it{{0}}".format(text))
    
    
    def addDataLatex(text):
        latex = r.TLatex()
        latex.SetNDC();
        latex.SetTextAngle(0);
        latex.SetTextColor(r.kBlack);
        latex.SetTextFont(42);
        latex.SetTextAlign(31);
        latex.SetTextSize(0.04);
        latex.DrawLatex(0.90, 0.93, "{0}".format(text))
