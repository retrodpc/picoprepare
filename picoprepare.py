#!/usr/bin/env python3

import sys
assert sys.version_info[0] >= 3, "Python 3 required."

import os
import shutil
import random

# directories for input/output files:
#
# src = put your source NSFs here
# cut = random-ordered stripped entries here
# fin = random-ordered final entries here
#
# note: cut/fin directories will be obliterated and recreated
#
# seed = random seed used for shuffling

src_dir = "src"
cut_dir = "cut_"
fin_dir = "fin"
cut_txt = "FAMICOMPO PICO"
seed = 37

print("pico_prepare.py")
print("")

shutil.rmtree(cut_dir,ignore_errors=True)
shutil.rmtree(fin_dir,ignore_errors=True)
os.mkdir(cut_dir)
os.mkdir(fin_dir)

print("Gathering source files...")
src_list = []
for f in os.listdir(src_dir):
    (root,ext) = os.path.splitext(f)
    if ext.lower() == ".nsf":
        src_list.append(f)
        print("> " + f)
print("")

print("Shuffling and preparing final/cut files...")
random.seed(seed)
random.shuffle(src_list)
fin_list = []
count = 1
for f in src_list:
    (root, ext) = os.path.splitext(f)
    ff = "Entry%03d_%s.nsf" % (count,root)
    fc = "Entry%03d.nsf" % (count)
    fb = "Entry%03d" % (count)
    fin_list.append(ff)
    count = count + 1
    # copy final file
    b = open(os.path.join(src_dir,f),"rb").read()
    fin_out = open(os.path.join(fin_dir,ff),"wb")
    fin_out.write(b)
    fin_out.close()
    # generate stripped file
    b = bytearray(b)
    for i in range(0,32):
        c = 0
        if i < len(cut_txt):
            c = ord(cut_txt[i])
        b[i+0x2E] = c # strip artist
        b[i+0x4E] = c # strip copyright
        c = 0
        if i < len(fb):
            c = ord(fb[i])
        b[i+0x0E] = c # replace title
    cut_out = open(os.path.join(cut_dir,fc),"wb")
    cut_out.write(b)
    cut_out.close()
    # list final name    
    print("> " + ff)
print("")

print("I'm finished!")
