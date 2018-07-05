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


###Programme###


#stiffness for real NAO Robot
def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def ymca():

    a = memoryProxy.getData("Device/SubDeviceList/LHipYawPitch/Position/Actuator/Value")
    b = memoryProxy.getData("Device/SubDeviceList/LHipRoll/Position/Actuator/Value")
    c = memoryProxy.getData("Device/SubDeviceList/LHipPitch/Position/Actuator/Value")
    d = memoryProxy.getData("Device/SubDeviceList/LKneePitch/Position/Actuator/Value")
    e = memoryProxy.getData("Device/SubDeviceList/LAnklePitch/Position/Actuator/Value")
    f = memoryProxy.getData("Device/SubDeviceList/LAnkleRoll/Position/Actuator/Value")
    g = -a
    h = memoryProxy.getData("Device/SubDeviceList/RHipRoll/Position/Actuator/Value")
    i = memoryProxy.getData("Device/SubDeviceList/RHipPitch/Position/Actuator/Value")
    j = memoryProxy.getData("Device/SubDeviceList/RKneePitch/Position/Actuator/Value")
    k = memoryProxy.getData("Device/SubDeviceList/RAnklePitch/Position/Actuator/Value")
    l = memoryProxy.getData("Device/SubDeviceList/RAnkleRoll/Position/Actuator/Value")

    pMaxSpeedFraction = 0.5
    tts = ALProxy("ALTextToSpeech", robotIP, port)
    tts.setLanguage('English')
    
    #Y
    motionProxy.angleInterpolationWithSpeed("Body",[0,0,-np.pi/2,0.7,0,0,0,0,a,b,c,d,e,f,-a,h,i,j,k,l,-np.pi/2,-0.7,0,0,0,0], pMaxSpeedFraction)
    tts.say("Y")
    time.sleep(0.5)

    #M
    motionProxy.angleInterpolationWithSpeed("Body",[0,0,-np.pi/2,0.7,0,-np.pi/2,-np.pi/2,0,a,b,c,d,e,f,g,h,i,j,k,l,-np.pi/2,-0.7,0,np.pi/2,np.pi/2,0], pMaxSpeedFraction)
    tts.say("M")
    time.sleep(0.2)

    #C   
    motionProxy.angleInterpolationWithSpeed("Body",[0,0,0,np.pi/2,0,0,-np.pi/2,0,a,b,c,d,e,f,g,h,i,j,k,l,-np.pi/2,0.2,0,np.pi/2,np.pi/2,0], pMaxSpeedFraction)
    tts.say("C")
    time.sleep(0.2)

    #A   
    motionProxy.angleInterpolationWithSpeed("Body",[0,0,-np.pi/2,0.4,0,-np.pi/4,-np.pi/2,0,a,b,c,d,e,f,g,h,i,j,k,l,-np.pi/2,-0.4,0,np.pi/4,np.pi/2,0], pMaxSpeedFraction)
    tts.say("A")
    time.sleep(0.7)


if __name__ == "__main__":
    StiffnessOn(motionProxy)
    # Send NAO to Pose Zero
    ymca()
    postureProxy.goToPosture("Crouch", 1.0)
    motionProxy.stiffnessInterpolation("Body", 0.0, 1.0)
