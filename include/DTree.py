import ROOT as r
from array import array
from ROOT import TTree, TFile, TCut, TH1F, TH2F, TH3F, THStack, TCanvas, SetOwnership
import copy
import os
import __main__

'''
Class that contains everything to read and process a certain dataset
'''
class DTree:

    def __init__(self, name, label, location, tag, isData = False):
        self.name = name
        self.label = label
        self.location = location
        self.isData = isData
        self.tag = tag # esto se da por linea de comandos al correr fill.py

        self.dtpaths = []
        self.dtfiles = []
        self.dtrees  = []
        for _file in os.listdir(self.location):
            if '.root' not in _file: continue
            ftfile = TFile(location + _file)
            ttree = ftfile.Get('Events')
            self.dtpaths.append(location + _file)
            self.dtfiles.append(ftfile)
            self.dtrees.append(ttree)

        self.count = 0.
        if self.isData:
            print(self.dtrees[0].GetEntries())
            for dtree in self.dtrees:
                self.count += dtree.GetEntries()
        
        self.outHistFiles = []

        self.printSample() 
        
        # ---------------------------------------------------------------------------------------------------------
        # Get useful directories, paths and filenames
        self.WORKDIR = os.getcwd() + '/'
        # Condor templates
        self.condorSh_template =  open(self.WORKDIR+"templates/condor_template.sh","r").read()
        self.condorSub_template = open(self.WORKDIR+"templates/condor_template.sub","r").read()
        # Script for looping events
        self.scriptLoc = self.WORKDIR+"loopEvents.py"
        # Condor logs location
        self.condorDir = self.WORKDIR+"condor/"+self.tag+"/"
        if not os.path.exists(self.condorDir): os.makedirs(self.condorDir)
        # Declare histograms dir and list
        self.histsDir = "/eos/user/r/rlopezru/DisplacedMuons-Analyzer_out/Analyzer/temp_hists/"+self.tag+"/"
        if not os.path.exists(self.histsDir): os.makedirs(self.histsDir)
        # ----------------------------------------------------------------------------------------------------------

    def printSample(self):
        print("#################################")
        print("Sample Name: ", self.name)
        print("Sample Location: ", self.location)
        print("Sample IsData: ", self.isData)
        print("Event count: ", self.count)
        print("#################################")

    def closeFiles(self):
        for _file in self.ftfiles:
            _file.Close()

    def process(self, outHistFile):
        return 

    def launchJobs(self, cutsFilename):
        self.cutsFilename = cutsFilename

        for i,tree in enumerate(self.dtrees):
            outHistFilename = self.histsDir+'hists_{0}_{1}.root'.format(self.name, i)
            self.outHistFiles.append(outHistFilename) # have a register of the output files with the histograms
            # aqui hay que llamar a loopevents.py
            command = "python3 {0} -o {1} -i {2} -c {3} -t {4}".format(self.scriptLoc,
                                                                       outHistFilename,
                                                                       self.dtpaths[i],
                                                                       self.cutsFilename,
                                                                       self.tag)
            sh_filename = self.condor_dir+"bash_{0}_{1}.sh".format(self.name, i)
            with open(sh_filename,"w") as f_sh:
                f_sh.write(self.condorSh_template.format(command))

        sub_filename = self.condor_dir+"condor_{0}.sub".format(self.name)
        with open(sub_filename,"w") as f_sub:
            f_sub.write(self.condorSub_template.format(sh_filename, self.condor_dir, self.name))
        os.system("condor_submit "+sub_filename+" --batch-name "+self.name)

    def merge(self):
        return
