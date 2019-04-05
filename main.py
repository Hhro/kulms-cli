import kulms
import requests
import sys
import getopt

def main():
    opts,args = getopt.getopt(sys.argv[1:],"i",["interactive"])

    for opt,arg in opts:
        if opt=='i':
            interactive=1
        
    
if __name__ == '__main__':
    main()
