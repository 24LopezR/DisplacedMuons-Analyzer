#!/bin/bash
pushd /afs/cern.ch/user/r/rlopezru/private/ntuplizer_test/CMSSW_12_4_0/src
eval `scramv1 runtime -sh`
pushd
python3 /afs/cern.ch/user/r/rlopezru/private/ntuplizer_test/CMSSW_12_4_0/src/Analysis/Cosmics-Analyzer/fill.py -t dgl_efficiencies -c /afs/cern.ch/user/r/rlopezru/private/ntuplizer_test/CMSSW_12_4_0/src/Analysis/Cosmics-Analyzer/config/trigger.txt -m fill
