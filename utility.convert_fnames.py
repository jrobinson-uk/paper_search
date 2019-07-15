import os
import sys
import subprocess

f = open('theories-terms.csv')
for line in f:
    fields = line.strip().split(',')
    newname = '{}.bib'.format(line.strip())
    oldname = '{}.bib'.format(fields[1].strip('"'))

    subprocess.call(['git', 'mv', os.sep.join(['ALL', oldname]), os.sep.join(['ALL', newname])])
    subprocess.call(['git', 'mv', os.sep.join(['CSE', oldname]), os.sep.join(['CSE', newname])])
