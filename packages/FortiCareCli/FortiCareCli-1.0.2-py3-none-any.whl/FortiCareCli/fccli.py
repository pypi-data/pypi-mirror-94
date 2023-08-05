#!/usr/bin/env python3
# vim: tabstop=8 softtabstop=0 expandtab shiftwidth=4 smarttab

#
# The only purpose of this file is to have fccli.py calling fccli on Windows.
# (becase we need to use the suffix there)
#

import sys
import os

if __file__[-3:] != ".py":
    print("The current file does not have \".py\" extension.")
    sys.exit(1)

sys.argv[0] = __file__[:-3]

os.spawnve(os.P_WAIT, sys.executable, [sys.executable] + sys.argv, os.environ)


