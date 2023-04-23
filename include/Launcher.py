import ROOT as r
import os


class Launcher:


    def __init__(self, filedir, tag, cut_file):
        WORKDIR = "/afs/cern.ch/user/r/rlopezru/private/ntuplizer_test/CMSSW_13_0_0_pre4/src/Analysis/DisplacedMuons-Analyzer_Mar14/DisplacedMuons-Analyzer/"
        # Read input args
        if filedir: self.filedir = filedir
        self.tag = tag
        if cut_file: self.cut_file = WORKDIR+cut_file
        
        # Condor templates
        self.condorSh_template = open(WORKDIR+"templates/condor_template.sh","r").read()
        self.condorSub_template = open(WORKDIR+"templates/condor_template.sub","r").read()
        # Script for looping events
        self.scriptLoc = WORKDIR+"loopEvents.py"
        # Condor logs location
        self.condor_dir = WORKDIR+"condor/"+self.tag+"/"
        if not os.path.exists(self.condor_dir): os.makedirs(self.condor_dir)
        
        # Declare histograms dir and list
        self.hists_dir = "/eos/user/r/rlopezru/Cosmics-Analyzer_out/Analyzer/temp_hists/"+self.tag+"/"
        if not os.path.exists(self.hists_dir): os.makedirs(self.hists_dir)
        self.joint_hists_name = {}
        self.joint_hists_name = self.hists_dir+'full/hists_'+self.tag+'.root'
        if not os.path.exists(self.hists_dir+'/full/'): os.makedirs(self.hists_dir+'/full/')


    def launchJobs(self):
        for fname in os.listdir(self.filedir):
            if '.root' not in fname: continue
            if '.sys' in fname: continue
            hfname = "hists_"+fname[:-5]
            command = "python3 {0} -o {1} -i {2} -c {3} -t {4}".format(self.scriptLoc,
                                                               self.hists_dir+hfname,
                                                               self.filedir+fname,
                                                               self.cut_file,
                                                               self.tag)
            sh_filename = self.condor_dir+"bash_"+fname[:-5]+".sh"
            with open(sh_filename,"w") as f_sh:
                f_sh.write(self.condorSh_template.format(command))
        sub_filename = self.condor_dir+"condor_"+self.tag+".sub"
        with open(sub_filename,"w") as f_sub:
            f_sub.write(self.condorSub_template.format(self.condor_dir, self.tag))
        os.system("condor_submit "+sub_filename+" --batch-name "+self.tag)


    def loop(self):
        for fname in os.listdir(self.filedir)[0:1]:
            print(' -> Processing file {0}'.format(fname))
            if '.root' not in fname: continue
            if '.sys' in fname: continue
            hfname = "hists_"+fname[:-5]
            command = "python3 {0} -o {1} -i {2} -c {3} -t {4}".format(self.scriptLoc,
                                                               self.hists_dir+hfname,
                                                               self.filedir+fname,
                                                               self.cut_file,
                                                               self.tag)
            os.system(command)


    def mergeHists(self):
        print('---- merge {0} hist file ---')
        command = 'hadd {0} {1}*.root'.format(self.joint_hists_name, self.hists_dir)
        if os.path.isfile(self.joint_hists_name): os.system('rm '+self.joint_hists_name)
        print('  - executing... '+command)
        os.system(command)
        print('----   merging done  ---')
        return self.joint_hists_name
