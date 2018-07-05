# -*- encoding: UTF-8 -*-

from naoqi import ALProxy, ALModule, ALBroker
import time
import sys
import motion
import select
import numpy as np
import signal
from optparse import OptionParser

robotIP = "192.168.0.103" # Gamma
port = 9559
Frequency = 0.0 #low speed
t=1.0


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
    print"Could not create proxy to ALMotion"
    print"Error was: ", e


###Execution###

def crouch():
    postureProxy.goToPosture("Crouch", 0.5) # Send NAO to Pose Crouch

    pNames = "Body"
    pStiffnessLists = 0.0
    pTimeLists = 1.0
    motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

if __name__ == "__main__":
    crouch()

