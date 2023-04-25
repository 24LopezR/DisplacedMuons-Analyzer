import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-r', '--run', dest='run', action='store_true')
parser.add_argument('-t', '--tag', dest='tag')
args = parser.parse_args()

tag = args.tag
njobs_AOD = 270
njobs_MiniAOD = 116

WORKDIR = os.getcwd() + '/'
print(' Workdir (from include/Launcher.py) {0}'.format(WORKDIR))
histdir = '/eos/user/r/rlopezru/DisplacedMuons-Analyzer_out/Analyzer/temp_hists/{0}/'.format(tag)
condor_dir = WORKDIR + 'condor/{0}/'.format(tag)

condorSub_template = '''
universe        = vanilla
executable      = {0}
arguments       = $(ProcID)
output          = {1}.out
error           = {1}.err
log             = {1}.log
Notify_user     = rlopezru@cern.ch
+JobFlavour     = "longlunch"
queue 1
'''

failed_AOD = 0
for i in range(njobs_AOD):
    if os.path.exists(histdir + 'hists_Cosmics_2022C_AOD_{0}.root'.format(i)): continue
    bash_file = 'bash_Cosmics_2022C_AOD_{0}.sh'.format(i)
    sub_filename = condor_dir + 'submit_failed_AOD_{0}.sub'.format(i+1)
    with open(sub_filename,"w") as f_sub:
        f_sub.write(condorSub_template.format(condor_dir + bash_file, condor_dir + 'log_failed_AOD_'+bash_file[:-3]))
    if args.run: os.system("condor_submit "+sub_filename+" --batch-name job_AOD_"+str(i))
    print('Failed job AOD: {0}'.format(i))
    #os.system('cat '+sub_filename)
    print("condor_submit "+sub_filename+" --batch-name job_AOD_"+str(i))
    failed_AOD += 1

failed_MiniAOD = 0
for i in range(njobs_MiniAOD):
    if os.path.exists(histdir + 'hists_Cosmics_2022C_MiniAOD_{0}.root'.format(i)): continue
    bash_file = 'bash_Cosmics_2022C_MiniAOD_{0}.sh'.format(i)
    sub_filename = condor_dir + 'submit_failed_MiniAOD_{0}.sub'.format(i+1)
    with open(sub_filename,"w") as f_sub:
        f_sub.write(condorSub_template.format(condor_dir + bash_file, condor_dir + 'log_failed_MiniAOD_'+bash_file[:-3]))
    if args.run: os.system("condor_submit "+sub_filename+" --batch-name job_MiniAOD_"+str(i))
    print('Failed job MiniAOD: {0}'.format(i))
    #os.system('cat '+sub_filename)
    print("condor_submit "+sub_filename+" --batch-name job_MiniAOD_"+str(i))
    failed_MiniAOD += 1

print('>>> Failed jobs AOD     = {0}'.format(failed_AOD))
print('>>> Failed jobs MiniAOD = {0}'.format(failed_MiniAOD))
