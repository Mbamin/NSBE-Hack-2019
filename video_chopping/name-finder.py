import beta_snippets
import os
import sys
import argparse
import io
import time
import subprocess

from google.cloud import videointelligence
from google.cloud.videointelligence import enums

f=open("cuts.txt","r")
lines=f.readlines()
names=[]
for x in lines:
    names.append(x.split()[0])
for name in names:
    os.system('python beta_snippets.py transcription name')
