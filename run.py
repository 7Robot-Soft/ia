#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys
from time import sleep
import settings
from ia import IA
from argparse import ArgumentParser
from ipython import IPython

parser = ArgumentParser(description='Eurobot IA')
parser.add_argument("name")
parser.add_argument("-k", "--kernel", action="store_true", help="launch ipython kernel")
parser.add_argument("-s", "--shell", action="store_true", help="launch ipython shell")

args = parser.parse_args()

if args.name not in settings.robots:
    print("Error: unknow robot '%s', available robots are: %s"
            %(args.name, ','.join(settings.robots)), file=sys.stderr)
    sys.exit(1)

ia = IA(args.name)

#from IPython.parallel import bind_kernel

#bind_kernel()

#ipython = IPython()

#if args.shell:
#    ipython.start(True)
#elif args.kernel:
#    ipython.start()
