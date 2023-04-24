import os

tag = 'redo_MiniAOD_IDcuts'
njobs = 116

WORKDIR = os.getcwd() + '/'
print(' Workdir (from include/Launcher.py) {0}'.format(WORKDIR))
histdir = '/eos/user/r/rlopezru/Cosmics-Analyzer_out/Analyzer/temp_hists/{0}/'.format(tag)
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

for i in range(njobs):
    if os.path.exists(histdir + 'hists_Cosmics_Run2022C_{0}_tracks.root'.format(i+1)): continue
    bash_file = 'bash_Cosmics_Run2022C_{0}.sh'.format(i+1)
    sub_filename = condor_dir + 'submit_failed_{0}.sub'.format(i+1)
    with open(sub_filename,"w") as f_sub:
        f_sub.write(condorSub_template.format(condor_dir + bash_file, condor_dir + 'log_failed_'+bash_file[:-3]))
    os.system("condor_submit "+sub_filename+" --batch-name job_"+str(i+1))
    print('Failed job: {0}'.format(i+1))
    #os.system('cat '+sub_filename)
    print("condor_submit "+sub_filename+" --batch-name job_"+str(i+1))
