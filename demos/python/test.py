# -*- encoding: UTF-8 -*-

from naoqi import ALProxy, ALModule, ALBroker
import time
import sys
import motion
import select
import numpy as np
import signal
from optparse import OptionParser
import math
import Image, cv2
import vision_definitions

robotIP = "192.168.0.103" # Gamma
port = 9559


###Definition de l'IP du robot###


if (len(sys.argv) >= 2):
    print("On prend l'IP entree")
    robotIP = sys.argv[1]


###Tests###


try:
    motionProxy = ALProxy("ALMotion", robotIP, port)
except Exception, e:
    print"Could not create proxy to ALMotion"
    print"Error was: ", e
try:
    postureProxy = ALProxy("ALRobotPosture", robotIP, port)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e


postureProxy.goToPosture("StandInit", 0.5)
motionProxy.setAngles("HeadPitch",5,0.2)

moveConfig = [["Frequency", 0.5]]
motionProxy.moveToward(0,0.5,0,moveConfig)
time.sleep(5)
motionProxy.moveToward(0,0,0,moveConfig)


