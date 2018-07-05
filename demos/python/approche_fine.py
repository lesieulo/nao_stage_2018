# -*- encoding: UTF-8 -*-
#auteur: gomisjo

"""
Programme qui récupère l'image de la vidéo et renvoie
les coordonnées du centre de la balle en pixels.

Images de taille 120x160.
"""

from naoqi import ALProxy
import vision_definitions
import time
import Image, cv2
import numpy as np
import sys

IP = "172.20.25.152"  # NAOqi's IP address.
PORT = 9559

if (len(sys.argv) >= 2):
    print("On prend l'IP entree")
    IP = sys.argv[1]

# Create proxy on ALVideoDevice
print("Creating ALVideoDevice proxy to ", IP)
camProxy = ALProxy("ALVideoDevice", IP, PORT)


# Register a Generic Video Module
camProxy = ALProxy("ALVideoDevice", IP, PORT)
camProxy.setParam(18, 0)	# "kCameraSelectID", 0 : camera top, 1 : camera bottom
resolution = 0			# 0 : QQVGA, 1 : QVGA, 2 : VGA
colorSpace = 11			# RGB
mini = 25
maxi = 33
seuil = 4

try :
    videoClient = camProxy.subscribeCamera("python_client",1, resolution, colorSpace, 5)
    print(videoClient)
except RuntimeError:
    camRepair.rep()
    videoClient = camProxy.subscribeCamera("python_client",1, resolution, colorSpace, 5)
    
    

def verif_bas(a):
    for i in range(1,120):
        for j in range(160):
            if a[-i][j] > 10:
                return((-i%120,j))

def centre_balle(a,b,liste):
    for k in range(4):
        for l in range(3):
            if a-k<120 and b-l<160:
                if liste[a-k][b-l] != 0:
                    #print("cas 1")
                    return [a-k, b-l]
            if a-k>0 and b+l>0:
                if liste[a-k][b+l] != 0:
                    #print("cas 2")
                    return [a-k, b+l]
    print("pas trouvé")

def contamine(x, y, seuil, convo, img_balle_seule):
    lst = []
    if 1<x<118 and 1<y<158:
            if convo[x-1][y] > seuil and img_balle_seule[x-1][y] == 0:
                img_balle_seule[x-1][y] = 1
                lst.append((x-1, y))
            if convo[x+1][y] > seuil and img_balle_seule[x+1][y] == 0:
                img_balle_seule[x+1][y] = 1
                lst.append((x+1, y))
            if convo[x][y-1] > seuil and img_balle_seule[x][y-1] == 0:
                img_balle_seule[x][y-1] = 1
                lst.append((x, y-1))
            if convo[x][y+1] > seuil and img_balle_seule[x][y+1] == 0:
                img_balle_seule[x][y+1] = 1
                lst.append((x, y+1))
    return lst,img_balle_seule

def nbr_pxl(seuil,a,b,convo,img_balle_seule):
    open = [(a, b)]
    while open != []:
        open += contamine(open[0][0], open[0][1], seuil,convo,img_balle_seule)[0]
        img_balle_seule = contamine(open[0][0], open[0][1], seuil,convo,img_balle_seule)[1]
        del(open[0])
    return np.count_nonzero(img_balle_seule), img_balle_seule

def trouve_balle(videoClient):
    from_video = camProxy.getImageRemote(videoClient)
    imageWidth, imageHeight = from_video[0], from_video[1]
    middle_x, middle_y = float(imageWidth / 2), float(imageHeight / 2)
    img_nao = from_video[6]
    img_PIL = Image.fromstring("RGB", (imageWidth, imageHeight), img_nao)
    img_brute = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
    cvImg = cv2.cvtColor(img_brute, cv2.COLOR_BGR2HSV)
    cvImg = cvImg[:,:,0]
    cvfiltre1 = mini < cvImg
    cvfiltre2 = (cvImg < maxi)
    cvfiltre = (cvfiltre1 * cvfiltre2)
    cvfiltre2 = np.zeros((120,160))
    for i in range(120):
        for j in range(160):
            if cvfiltre[i][j]:
                cvfiltre2[i][j] = 1
            else:
                cvfiltre2[i][j] = 0
    kernel = np.ones((4,4),np.float32)
    convo = cv2.filter2D(cvfiltre2,-1,kernel)
    print("convo",np.shape(convo),np.max(convo))
    if np.max(convo) < 4:
        return(False)
    else:
        x_b,y_b = verif_bas(convo)[0], verif_bas(convo)[1]
        img_bas = np.zeros((120,160))
        img_bas[x_b][y_b] = 1
        if x_b!=0 and x_b!=119 and y_b!=0 and y_b!=159:
            img_bas[x_b+1][y_b] = 1
            img_bas[x_b-1][y_b] = 1
            img_bas[x_b][y_b+1] = 1
            img_bas[x_b][y_b-1] = 1
        x_centre, y_centre = centre_balle(x_b,y_b,convo)
        img_balle_seule = np.zeros((120,160))
        img_balle_seule[x_centre][y_centre] = 1
        n,img_balle_seule = nbr_pxl(seuil,x_centre,y_centre,convo,img_balle_seule)
        x1 = max(0, x_centre-20)
        x2 = min(x_centre+5, 119)
        y1 = max(0, y_centre-7)
        y2 = min(y_centre+7, 159)
        for i in range(img_balle_seule.shape[0]):
            if np.max(img_balle_seule[i,:]) > 0:
                xmin = i
                break
        for i in range(img_balle_seule.shape[0]-1, 0, -1):
            if np.max(img_balle_seule[i,:]) > 0:
                xmax = i
                break	
        for i in range(img_balle_seule.shape[1]):
            if np.max(img_balle_seule[:,i]) > 0:
                ymin = i
                break
        for i in range(img_balle_seule.shape[1]-1, 0, -1):
            if np.max(img_balle_seule[:,i]) > 0:
                ymax = i
                break
        largeur, hauteur = ymax-ymin, xmax-xmin
        diametre = max(largeur, hauteur)
        return((xmax+xmin)//2, (ymax+ymin)//2)



if __name__ == "__main__":
    
    print(trouve_balle(videoClient))
    camProxy.unsubscribe(videoClient)















