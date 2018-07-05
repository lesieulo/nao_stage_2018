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
    #position tête
    print("headYawAngle : ",memoryProxy.getData("Device/SubDeviceList/HeadYaw/Position/Actuator/Value"))
    print("HeadPitch : ", memoryProxy.getData("Device/SubDeviceList/HeadPitch/Position/Actuator/Value"))

    #position bras gauche
    print("LShoulderPitch : ", memoryProxy.getData("Device/SubDeviceList/LShoulderPitch/Position/Actuator/Value"))
    print("LShoulderRoll : ", memoryProxy.getData("Device/SubDeviceList/LShoulderRoll/Position/Actuator/Value"))
    print("LElbowYaw : ", memoryProxy.getData("Device/SubDeviceList/LElbowYaw/Position/Actuator/Value"))
    print("LElbowRoll : ", memoryProxy.getData("Device/SubDeviceList/LElbowRoll/Position/Actuator/Value"))
    print("LWristYaw : ", memoryProxy.getData("Device/SubDeviceList/LWristYaw/Position/Actuator/Value"))
    print("LHand : ", memoryProxy.getData("Device/SubDeviceList/LHand/Position/Actuator/Value"))

    #position jambe Gauche
    print("LHipYawPitche : ", memoryProxy.getData("Device/SubDeviceList/LHipYawPitch/Position/Actuator/Value"))
    print("LHipRoll : ", memoryProxy.getData("Device/SubDeviceList/LHipRoll/Position/Actuator/Value"))
    print("LHipPitch : ", memoryProxy.getData("Device/SubDeviceList/LHipPitch/Position/Actuator/Value"))
    print("LKneePitch : ", memoryProxy.getData("Device/SubDeviceList/LKneePitch/Position/Actuator/Value"))
    print("LAnklePitch : ", memoryProxy.getData("Device/SubDeviceList/LAnklePitch/Position/Actuator/Value"))
    print("LAnkleRoll : ", memoryProxy.getData("Device/SubDeviceList/LAnkleRoll/Position/Actuator/Value"))

    

    #position jambe droite
    print("RHipYawPitche : ", -memoryProxy.getData("Device/SubDeviceList/LHipYawPitch/Position/Actuator/Value"))
    print("RHipRoll : ", memoryProxy.getData("Device/SubDeviceList/RHipRoll/Position/Actuator/Value"))
    print("RHipPitch : ", memoryProxy.getData("Device/SubDeviceList/RHipPitch/Position/Actuator/Value"))
    print("RKneePitch : ", memoryProxy.getData("Device/SubDeviceList/RKneePitch/Position/Actuator/Value"))
    print("RAnklePitch : ", memoryProxy.getData("Device/SubDeviceList/RAnklePitch/Position/Actuator/Value"))
    print("RAnkleRoll : ", memoryProxy.getData("Device/SubDeviceList/RAnkleRoll/Position/Actuator/Value"))



    #position bras Droit
    print("RShoulderPitch : ", memoryProxy.getData("Device/SubDeviceList/RShoulderPitch/Position/Actuator/Value"))
    print("RShoulderRoll : ", memoryProxy.getData("Device/SubDeviceList/RShoulderRoll/Position/Actuator/Value"))
    print("RElbowYaw: ", memoryProxy.getData("Device/SubDeviceList/RElbowYaw/Position/Actuator/Value"))
    print("RElbowRoll : ", memoryProxy.getData("Device/SubDeviceList/RElbowRoll/Position/Actuator/Value"))
    print("RWristYaw : ", memoryProxy.getData("Device/SubDeviceList/RWristYaw/Position/Actuator/Value"))
    print("RHand : ", memoryProxy.getData("Device/SubDeviceList/RHand/Position/Actuator/Value"))


def aka():
    init(motionProxy)
    vitesse = 0.6
    postureProxy.goToPosture("StandInit",1.0)
    #position haka départ
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,0.49,-0.179,0.0645,-1.269,0.207,0.0,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.012,0.221,0.167,1.290,-0.085,0.0],0.2)
    time.sleep(0.5)
    #position haka, bras haut
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,0.957,1.117,-2.079,-1.529,-0.132,0.148,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.39427995681762695, -0.925044059753418, 1.823884129524231, 1.362234115600586, -0.015382050536572933, 0.009600043296813965],vitesse)
    #position haka, bras bas
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.480,0.073,-1.264,-0.880,1.097,0.205,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,1.360,-0.015,1.143,0.677,-1.009,0.009],vitesse)
    
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,0.957,1.117,-2.079,-1.529,-0.132,0.148,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.39427995681762695, -0.925044059753418, 1.823884129524231, 1.362234115600586, -0.015382050536572933, 0.009600043296813965],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.480,0.073,-1.264,-0.880,1.097,0.205,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,1.360,-0.015,1.143,0.677,-1.009,0.009],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,0.957,1.117,-2.079,-1.529,-0.132,0.148,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.39427995681762695, -0.925044059753418, 1.823884129524231, 1.362234115600586, -0.015382050536572933, 0.009600043296813965],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.480,0.073,-1.264,-0.880,1.097,0.205,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,1.360,-0.015,1.143,0.677,-1.009,0.009],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,0.957,1.117,-2.079,-1.529,-0.132,0.148,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.39427995681762695, -0.925044059753418, 1.823884129524231, 1.362234115600586, -0.015382050536572933, 0.009600043296813965],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.480,0.073,-1.264,-0.880,1.097,0.205,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,1.360,-0.015,1.143,0.677,-1.009,0.009],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.480,0.073,-1.264,-0.880,1.097,0.205,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,1.360,-0.015,1.143,0.677,-1.009,0.009],vitesse)
    # position haka bras milieu
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.2501680850982666, 1.274712085723877, -1.5202360153198242, -1.4695301055908203, 0.3389720916748047, 0.1624000072479248,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173, 1.2257080078125, -1.1198620796203613, 1.52168607711792, 1.5141000747680664, -0.42342591285705566, 0.009600043296813965],vitesse)
    #time.sleep(0.2)
    # idem avec coudes dépliés
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.2501680850982666, 1.274712085723877, -1.5202360153198242, 0.0, 0.3389720916748047, 0.1624000072479248,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173, 1.2257080078125, -1.1198620796203613, 1.52168607711792, 0.0, -0.42342591285705566, 0.009600043296813965],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.2501680850982666, 1.274712085723877, -1.5202360153198242, -1.4695301055908203, 0.3389720916748047, 0.1624000072479248,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173, 1.2257080078125, -1.1198620796203613, 1.52168607711792, 1.5141000747680664, -0.42342591285705566, 0.009600043296813965],vitesse)
    #bras haut, tête haute
    motionProxy.angleInterpolationWithSpeed("Body",[-0.0015759468078613281, -0.5890979766845703,0.957,1.117,-2.079,-1.529,-0.132,0.148,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.39427995681762695, -0.925044059753418, 1.823884129524231, 1.362234115600586, -0.015382050536572933, 0.009600043296813965],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.480,0.073,-1.264,-0.880,1.097,0.205,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,1.360,-0.015,1.143,0.677,-1.009,0.009],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,0.957,1.117,-2.079,-1.529,-0.132,0.148,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.39427995681762695, -0.925044059753418, 1.823884129524231, 1.362234115600586, -0.015382050536572933, 0.009600043296813965],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.480,0.073,-1.264,-0.880,1.097,0.205,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,1.360,-0.015,1.143,0.677,-1.009,0.009],vitesse)
    time.sleep(0.2)
    #position 2 bras avancés
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.142788052558899, 0.230057954788208, -1.4174580574035645, -0.6580440998077393, -1.7518701553344727, 0.6387999653816223,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173, 1.0907158851623535, -0.16878199577331543, 1.6597460508346558,0.7026140689849854, 1.3621500730514526, 0.4976000189781189],vitesse)
    time.sleep(0.2)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.480,0.073,-1.264,-0.880,1.097,0.205,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,1.360,-0.015,1.143,0.677,-1.009,0.009],vitesse)
    #bras droit avancé (ext -> int ), tête un peu baissé vers la droite
    motionProxy.angleInterpolationWithSpeed("Body",[-0.5691559314727783, 0.31442809104919434,1.480,0.073,-1.264,-0.880,1.097,0.205,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173, 1.0907158851623535, -0.16878199577331543, 1.6597460508346558,0.7026140689849854, 1.3621500730514526, 0.4976000189781189],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.480,0.073,-1.264,-0.880,1.097,0.205,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173, 1.0201520919799805, 0.27454400062561035, 1.6566780805587769, 0.7563040256500244, 1.3606160879135132, 0.49720001220703125],0.3)
    time.sleep(0.2)
    #bras gauche avancé (ext -> int ), tête un peu baissé vers la gauche
    motionProxy.angleInterpolationWithSpeed("Body",[0.4662940502166748, 0.31442809104919434, 1.142788052558899, 0.230057954788208, -1.4174580574035645, -0.6580440998077393, -1.7518701553344727, 0.6387999653816223,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,1.360,-0.015,1.143,0.677,-1.009,0.009],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170, 1.084496021270752, -0.2224719524383545, -1.415924072265625, -0.6810541152954102, -1.6951122283935547, 0.6387999653816223,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,1.360,-0.015,1.143,0.677,-1.009,0.009],0.3)
    time.sleep(0.2)

    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.480,0.073,-1.264,-0.880,1.097,0.205,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,1.360,-0.015,1.143,0.677,-1.009,0.009],vitesse)
    #retour en position initiale
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,0.49,-0.179,0.0645,-1.269,0.207,0.0,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.012,0.221,0.167,1.290,-0.085,0.0],0.2)
    time.sleep(0.2)

    #partie2
    #position bras droit levé
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.480,0.073,-1.264,-0.880,1.097,0.205,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173, 0.5384759902954102, -1.132133960723877, 1.9404680728912354, 1.529439926147461, 1.5891821384429932, 0.012799978256225586],vitesse)
    #position frappe coude droit
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,0.5874800682067871, -0.297637939453125, -0.2715599536895752, -1.0722241401672363, -0.8943638801574707, 0.5600000023841858,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.12276195734739304, 0.16409611701965332, 1.533958077430725, 1.5325078964233398, 1.6766201257705688, 0.3203999996185303],vitesse)
    # position précédent avec les bras plus écartés
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170, 0.6580440998077393, 0.36658406257629395, -0.6504578590393066, -1.1642640829086304, -0.7762460708618164, 0.5812000036239624,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.1825878620147705, -0.32524991035461426, 1.579978108406067, 1.5325078964233398, 1.383626103401184, 0.011600017547607422],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,0.5874800682067871, -0.297637939453125, -0.2715599536895752, -1.0722241401672363, -0.8943638801574707, 0.5600000023841858,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.12276195734739304, 0.16409611701965332, 1.533958077430725, 1.5325078964233398, 1.6766201257705688, 0.3203999996185303],vitesse)

    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.142788052558899, 0.230057954788208, -1.4174580574035645, -0.6580440998077393, -1.7518701553344727, 0.6387999653816223,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173, 1.0907158851623535, -0.16878199577331543, 1.6597460508346558,0.7026140689849854, 1.3621500730514526, 0.4976000189781189],vitesse)

    # position frappe coude gauche
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170, 0.3021559715270996, -0.19792795181274414, -1.6843738555908203, -1.5621000528335571, -1.3975157737731934, 0.013200044631958008,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173, 0.3467259407043457, 0.3251659870147705, 0.3128941059112549, 0.9910058975219727, 1.2102841138839722, 0.5320000052452087],vitesse)
    # idem avec bras plus écartés
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170, 0.23926210403442383, 0.15335798263549805, -1.563188076019287, -1.537026047706604, -1.3714380264282227, 0.013200044631958008,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.4249598979949951, -0.26389002799987793, 0.34357404708862305, 1.2778639793395996, 1.1274480819702148, 0.5320000052452087],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170, 0.3021559715270996, -0.19792795181274414, -1.6843738555908203, -1.5621000528335571, -1.3975157737731934, 0.013200044631958008,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173, 0.3467259407043457, 0.3251659870147705, 0.3128941059112549, 0.9910058975219727, 1.2102841138839722, 0.5320000052452087],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170, 0.23926210403442383, 0.15335798263549805, -1.563188076019287, -1.537026047706604, -1.3714380264282227, 0.013200044631958008,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.4249598979949951, -0.26389002799987793, 0.34357404708862305, 1.2778639793395996, 1.1274480819702148, 0.5320000052452087],vitesse)

    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,0.5874800682067871, -0.297637939453125, -0.2715599536895752, -1.0722241401672363, -0.8943638801574707, 0.5600000023841858,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.12276195734739304, 0.16409611701965332, 1.533958077430725, 1.5325078964233398, 1.6766201257705688, 0.3203999996185303],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170, 0.6580440998077393, 0.36658406257629395, -0.6504578590393066, -1.1642640829086304, -0.7762460708618164, 0.5812000036239624,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.1825878620147705, -0.32524991035461426, 1.579978108406067, 1.5325078964233398, 1.383626103401184, 0.011600017547607422],vitesse)

    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170, 0.3021559715270996, -0.19792795181274414, -1.6843738555908203, -1.5621000528335571, -1.3975157737731934, 0.013200044631958008,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173, 0.3467259407043457, 0.3251659870147705, 0.3128941059112549, 0.9910058975219727, 1.2102841138839722, 0.5320000052452087],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170, 0.23926210403442383, 0.15335798263549805, -1.563188076019287, -1.537026047706604, -1.3714380264282227, 0.013200044631958008,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,0.4249598979949951, -0.26389002799987793, 0.34357404708862305, 1.2778639793395996, 1.1274480819702148, 0.5320000052452087],vitesse)

    # position bras gauche devant la tête, bras droit dessous le coude gauche
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170, 0.3282339572906494, -0.34035733342170715, -0.7455658912658691, -1.5508320331573486, -1.089181900024414, 0.011600017547607422,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173, 0.9724169969558716, 0.255886435508728, 0.38133978843688965, 1.0374573469161987, 0.5123140811920166, 0.010800004005432129],vitesse)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.480,0.073,-1.264,-0.880,1.097,0.205,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173, 0.5384759902954102, -1.132133960723877, 1.9404680728912354, 1.529439926147461, 1.5891821384429932, 0.012799978256225586],vitesse)
    time.sleep(0.5)
    motionProxy.angleInterpolationWithSpeed("Body",[0.00,-0.170,1.480,0.073,-1.264,-0.880,1.097,0.205,-0.690,0.0844,-0.061,1.303,-0.759,-0.003,0.690,-0.339,-0.167,1.311,-0.661,0.173,1.360,-0.015,1.143,0.677,-1.009,0.009],vitesse)



    
if __name__ == "__main__":
    init(motionProxy)
    aka()
    #motionProxy.stiffnessInterpolation("Body", 0.0, 1.0)
