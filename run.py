#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys
from time import sleep
import settings
from ia import IA

if len(sys.argv) != 2:
    print("Usage: %s ROBOT" %sys.argv[0])
    print("where  ROBOT := { petit | gros }")
    exit(1)

robot_name = sys.argv[1]
if not robot_name in settings.robots:
    print("Robot '%s' unavailable" %robot_name)
    print("Available robots :")
    for robot in settings.robots:
        print("\t", robot)
    exit(1)

ia = IA(robot_name)
