import kulms
import communicate
import requests
import sys
import getopt
import getpass

def main():
    uid = ''
    upw = ''
    opts, args = getopt.getopt(sys.argv[1:],"ipa:",["interactive","pass","auth="])

    for opt,arg in opts:
        if opt in ("-i","--interactive"):
            interactive=1
        if opt in ("-a","--auth"):
            uid = arg
        if opt in ("-p","--pass"):
            upw = getpass.getpass()
        
    if interactive == 1:
        communicate.commLoop(uid,upw)

    
if __name__ == '__main__':
    main()
