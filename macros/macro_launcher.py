import ROOT as r
import os, json
from math import pi
import numpy as np
from argparse import ArgumentParser
from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
#print(sys.path)
from include.DTree import DTree

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

########################################## FUNCTIONS #############################################
def printConfig(args):
    print(bcolors.WARNING + 20*'#' + ' DISPLACED MUON ANALYZER ' + 20*'#')
    print(' >> -t / --tag:    {0}'.format(args.tag))
    print(' >> --no-run:      {0}'.format(not args.run))
    print(' >> -q / --condor: {0}'.format(args.condor))
    print(65*'#' + bcolors.ENDC)


def launchMacro(dtree, macroFileName, args = {}):
    if args['condor']:
        for i,path in enumerate(dtree.dtpaths):
            # aqui hay que llamar a la macro que toca
            command = "python3 {0} -o {1} -i {2} --name {3}".format(WORKPATH + '/macros/' + macroFileName + '.py',
                                                                           dtree.outHistFiles[i],
                                                                           path,
                                                                           dtree.name)
            sh_filename = dtree.condorDir+"bash_{0}_{1}.sh".format(dtree.name, i)
            with open(sh_filename,"w") as f_sh:
                f_sh.write(dtree.condorSh_template.format(command))

        sub_filename = dtree.condorDir+"condor_{0}.sub".format(dtree.name)
        with open(sub_filename,"w") as f_sub:
            f_sub.write(dtree.condorSub_template.format(dtree.condorDir, dtree.name))
        os.system("condor_submit "+sub_filename+" --batch-name "+dtree.name)
    else:
        for i,path in enumerate(dtree.dtpaths):
            print(' -> Processing file {0}'.format(path))
            command = "python3 {0} -o {1} -i {2} --name {3}".format(WORKPATH + '/macros/' + macroFileName + '.py',
                                                                           dtree.outHistFiles[i],
                                                                           path,
                                                                           dtree.name)
            os.system(command)


################################# GLOBAL VARIABLES DEFINITION ####################################

runningfile = os.path.abspath(__file__)
WORKPATH = ''
for level in runningfile.split('/')[:-2]:
    WORKPATH += level
    WORKPATH += '/'
EOSPATH = '/eos/user/r/rlopezru/DisplacedMuons-Analyzer_out/Analyzer/'

# Read dat file
datFile = WORKPATH + 'dat/Samples_Spring23.json'
dat = json.load(open(datFile,'r'))

if __name__ == '__main__':

    r.gROOT.ProcessLine('.L ./include/tdrstyle.C')
    r.gROOT.SetBatch(1)
    print('WORKPATH: ' + WORKPATH)
    print('EOSPATH: ' + EOSPATH)

    r.gStyle.SetPaintTextFormat("3.2f")
    parser = ArgumentParser()
    parser.add_argument('-t', '--tag',   dest='tag')
    parser.add_argument('-m', '--macro', dest='macro')
    parser.add_argument('-d', '--debug', dest='debug',  action='store_true')
    parser.add_argument('-q', '--queue', dest='condor', action= 'store_true')
    parser.add_argument('--no-run',      dest='run',    action= 'store_false')
    args = parser.parse_args()

    printConfig(args)
   
    run = args.run
    gTag = 'AOD_hitsVSsegments_' + args.tag
    macroFileName = args.macro
 
    # Set debugging mode
    with open(WORKPATH+'include/cfg.py','w') as f:
        f.write('DEBUG = {0}'.format(args.debug))

    # Trees
    trees_originalFilter = []
    #trees_originalFilter.append(DTree('Cosmics_2022C',             'Cosmics Run2022C',                dat['Cosmics_2022C']['MiniAOD-Ntuples'],              gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_400_150_4000','H #rightarrow SS (400,150,4000)', dat['HTo2LongLived_400_150_4000']['AOD-Ntuples'], gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_1300', 'H #rightarrow SS (125,20,1300)',  dat['HTo2LongLived_125_20_1300']['AOD-Ntuples'],  gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_130',  'H #rightarrow SS (125,20,130)',   dat['HTo2LongLived_125_20_130']['AOD-Ntuples'],   gTag, isData = False))
    trees_originalFilter.append(DTree('HTo2LongLived_125_20_13',   'H #rightarrow SS (125,20,13)',    dat['HTo2LongLived_125_20_13']['AOD-Ntuples'],    gTag, isData = False))

    trees_nsegmentsFilter = []
    #trees_nsegmentsFilter.append(DTree('HTo2LongLived_400_150_4000_nseg2','H #rightarrow SS (400,150,4000)', dat['HTo2LongLived_400_150_4000']['AOD-Ntuples_nsegments2'], gTag, isData = False))
    #trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_1300_nseg2', 'H #rightarrow SS (125,20,1300)',  dat['HTo2LongLived_125_20_1300']['MiniAOD-Ntuples_nsegments2'],  gTag, isData = False))
    #trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_130_nseg2',  'H #rightarrow SS (125,20,130)',   dat['HTo2LongLived_125_20_130']['MiniAOD-Ntuples_nsegments2'],   gTag, isData = False))
    #trees_nsegmentsFilter.append(DTree('HTo2LongLived_125_20_13_nseg2',   'H #rightarrow SS (125,20,13)',    dat['HTo2LongLived_125_20_13']['MiniAOD-Ntuples_nsegments2'],    gTag, isData = False))
    

    if run:
        # Empty condor folder
        if args.condor:
            os.system('rm {0}/condor/{1}/*'.format(WORKPATH, args.tag))

        # Launch jobs
        for dtree in trees_originalFilter + trees_nsegmentsFilter:
            largs = {}
            largs['condor'] = args.condor
            launchMacro(dtree, macroFileName, args = largs)
