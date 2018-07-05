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

try:
    memoryProxy = ALProxy("ALMemory",robotIP, port)
except Exception, e:
    print "Could not create proxy to ALMemory"
    print "Error was: ", e


def init(proxy):
    #We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def getData():

    liste = []

    #position tête
    liste.append(memoryProxy.getData("Device/SubDeviceList/HeadYaw/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/HeadPitch/Position/Actuator/Value"))

    #position bras gauche
    liste.append(memoryProxy.getData("Device/SubDeviceList/LShoulderPitch/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/LShoulderRoll/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/LElbowYaw/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/LElbowRoll/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/LWristYaw/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/LHand/Position/Actuator/Value"))

    #position jambe Gauche
    liste.append(memoryProxy.getData("Device/SubDeviceList/LHipYawPitch/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/LHipRoll/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/LHipPitch/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/LKneePitch/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/LAnklePitch/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/LAnkleRoll/Position/Actuator/Value"))

    #position jambe droite
    liste.append(-memoryProxy.getData("Device/SubDeviceList/LHipYawPitch/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/RHipRoll/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/RHipPitch/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/RKneePitch/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/RAnklePitch/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/RAnkleRoll/Position/Actuator/Value"))

    #position bras Droit
    liste.append(memoryProxy.getData("Device/SubDeviceList/RShoulderPitch/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/RShoulderRoll/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/RElbowYaw/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/RElbowRoll/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/RWristYaw/Position/Actuator/Value"))
    liste.append(memoryProxy.getData("Device/SubDeviceList/RHand/Position/Actuator/Value"))

    print(liste)


if __name__ == "__main__":
    init(motionProxy)
    getData()
    motionProxy.stiffnessInterpolation("Body", 0.0, 1.0)
