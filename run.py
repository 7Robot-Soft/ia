#!/usr/bin/env python3

import sys
from time import sleep
import settings
from ia import IA
from argparse import ArgumentParser
from logging.config import fileConfig

parser = ArgumentParser(description='Eurobot IA')
parser.add_argument("name")
parser.add_argument("-s", "--shell", action="store_true", help="Launch IPython shell.")

args = parser.parse_args()

if args.name not in settings.robots:
    print("Error: unknow robot '%s', available robots are: %s"
            %(args.name, ','.join(settings.robots)), file=sys.stderr)
    sys.exit(1)

f = open('robots/'+args.name+'.ini')
fileConfig(f)
f.close()

ia = IA(args.name)

if args.shell:
    try:
        from IPython import embed
    except ImportError:
        print("Error: you need IPython to launch IPython shell.", file=sys.stderr)
    else:
        embed()
