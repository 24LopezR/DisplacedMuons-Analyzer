import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Debugger:

    def __init__(self, debug=False):
        self.debug = debug
        #if debug:
            #print(bcolors.BOLD+'Running in debug mode'+bcolors.ENDC)
            #print('Output to log.out')
        self.color_map = {}
        self.color_map["INFO"] = bcolors.OKCYAN
        self.color_map["ERROR"] = bcolors.FAIL
        self.color_map["SUCCESS"] = bcolors.OKGREEN
        self.outfile = 'out.log'
        if os.path.exists(self.outfile): os.system('rm {0}'.format(self.outfile))

    def print(self, message, status):
        if self.debug:
            head = self.color_map[status]+'['+status+'] '+bcolors.ENDC
            print(head+message, file=open(self.outfile,'a'))
