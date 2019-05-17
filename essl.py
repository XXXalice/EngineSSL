#!/usr/local/var/pyenv/versions/anaconda3-5.2.0/envs/ml/bin/python
import enginessl.etc.wordart as wa
import subprocess
import sys

VERSION = 1.00
font = 'big'
if len(sys.argv) <= 1:
    target = ''
else:
    target = sys.argv[1]
    if sys.argv[2:3]:
        font=sys.argv[2]
wa.print_logo(font=font)
print('(version:{})'.format(VERSION))

subprocess.run(['python enginessl/exe.py {}'.format(target)], shell=True)