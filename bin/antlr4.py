import subprocess
import sys
import os

my_dir = os.path.realpath(os.path.dirname(__file__))
antlr = 'antlr-4.7.2-complete.jar'
args = [
    'java', '-cp', my_dir + '/' + antlr, 'org.antlr.v4.Tool'
]
args.extend(sys.argv[1:])
subprocess.check_call(args)
