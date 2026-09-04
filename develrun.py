#!/usr/bin/python
# This is for development only
import sys, re
from khidl.app import CLI
if __name__=="__main__":
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(CLI())
