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


###Programme###


#def image():
#    cameraProxy = ALProxy("ALVideoDevice", robotIP, port)
#    myCamera = cameraProxy.subscribe("myCamera", resolution, colorSpace, fps)
#    for i in range(20):
#        cameraProxy.getImageLocal(myCamera)
#        cameraProxy.releaseImage(myCamera)
#    cameraProxy.unsubscribe(myCamera)

def showNaoImage():
    """
    Enregistre une vidéo de 10 secondes de qualité 640x480 et 30 fps
    """
    videoRecorderProxy = ALProxy("ALVideoRecorder", robotIP, port)
    
    # This records a 320*240 MJPG video at 50 fps.
    # Note MJPG can't be recorded with a framerate lower than 3 fps.
    videoRecorderProxy.setResolution(resolution) 
    videoRecorderProxy.setFrameRate(fps)
    videoRecorderProxy.setVideoFormat("MJPG")
    videoRecorderProxy.startRecording("/home/nao/records/", "test_vid")
    
    print("On enregistre la video")
    time.sleep(10)
    # Video file is saved on the robot in the
    # /home/nao/recordings/cameras/ folder.
    videoInfo = videoRecorderProxy.stopRecording()
    #print type video
    print "Video was saved on the robot: ", videoInfo[1]
    print "Num frames: ", videoInfo[0]
    #video = memoryProxy.getData("/home/nao/records/test.avi")

def micro():
    """
    Enregistre le son ambiant pendant 10 secondes
    """
    audioRecorderProxy = ALProxy("ALAudioDevice", robotIP, port)
    audioRecorderProxy.openAudioInputs()
    audioRecorderProxy.startMicrophonesRecording("/home/nao/records/test_aud.wav")
    
    print("On enregistre le son")
    time.sleep(10)
    audioRecorderProxy.stopMicrophonesRecording()


###Execution###


if __name__ == "__main__" :
    showNaoImage()
    micro()

