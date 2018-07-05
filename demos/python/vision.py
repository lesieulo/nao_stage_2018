# -*- encoding: UTF-8 -*-

from naoqi import ALProxy, ALModule, ALBroker
import time
import sys
import motion
import select
import numpy as np
import signal
from optparse import OptionParser

robotIP = "192.168.0.103" #Gamma
port = 9559
CameraID = 0
resolution = 2
colorSpace = 0
fps = 30


###Definition de l'IP du robot###


if (len(sys.argv) >= 2):
    print("On prend l'IP entree")
    robotIP = sys.argv[1] 


###Tests###


try:
    memoryProxy = ALProxy("ALMemory",robotIP, port)
except Exception, e:
    print "Could not create proxy to ALMemory"
    print "Error was: ", e

