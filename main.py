#Imports
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import imutils
import time
import RPi.GPIO as GPIO
import pin as p
#Def Functionsq

def reset(s):
    global stato
    global conta
    stato=1
    conta=0
    p.reset()

def trova_colore(immagine,col):

    hsv = cv2.cvtColor(immagine, cv2.COLOR_BGR2HSV)
    if col==1:#arancio
        low = np.array([(10, 0, 0)])
        high = np.array([(20, 255, 255)])
        
    if col==2:#blu
        low = np.array([(99, 0, 0)])
        high = np.array([(105, 255, 255)])
        
    if col==3:#verde
        low = np.array([(46, 120, 0)])
        high = np.array([(49, 255, 255)])
        
    if col==4:#rosso
        low = np.array([(173, 0, 0)])
        high = np.array([(179, 255, 255)])
        
    mask = cv2.inRange(hsv, low, high)
    cnts = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)#problemi di compatibilità
    if len(cnts)!=0:
        for c in (cnts):
            #calcolo l'area della zona colorata
            if cv2.contourArea(c)>20:
                return 1
    return 0
    
def linea(immagine):
    l=immagine[60:120,0:120]
    cv2.rectangle(immagine,(160,60),(0,120),(255,0,0),1)
    return l
    
def trova_linea(col,immagine):
    l=linea(immagine)
    return trova_colore(l,col)

#pre elaborazione e filtro di soglia per identificare il nero
def tagli(immagine):
    sx=immagine[80:120,0:20]
    dx=immagine[80:120,140:160]
    return (sx,dx)
    
def filtra(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15,15), 0)
    (T, thresh) = cv2.threshold(blurred, 40, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("fin",thresh)
    return thresh    

def bordi(mask):    
    #trovare i contorni
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)#problemi di compatibilità
    
    if len(cnts)!=0:
        c = max(cnts, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        if (w*h)>200:
            return 1
    return 0

def controllaBordi():
    maschera=filtra(img)
    (sx,dx)=tagli(maschera)
    sx=bordi(sx)
    dx=bordi(dx)
    print("sx",sx)
    print("dx",dx)
    if dx==1:
        p.destra()
    elif sx==1:
        p.sinistra()
        
def controllaOstacoli():
    if trova_linea(3,img)==1:
        print("ostacolo verde")
        p.sinistra()
        time.sleep(0.5)
    elif trova_linea(4,img)==1:
        print("ostacolo rosso")
        p.destra()
        time.sleep(0.5)
    

#Initalizations
camera = PiCamera()
camera.resolution = (160, 120)
camera.shutter_speed=30000
camera.exposure_mode = 'off'
rawCapture = PiRGBArray(camera, size=(160, 120))
time.sleep(0.1)
stato=0
conta=0

#Main
GPIO.add_event_detect(p.tastoReset, GPIO.RISING,callback=reset, bouncetime=100)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #Prende immagini dalla cam e le mostra ad ogni iterazione del ciclo
    img = cv2.flip(frame.array, 0)
    rawCapture.truncate(0)         
    cv2.imshow("cam",img)
    
    k=cv2.waitKey(1)
    #print(stato)
    if conta>11 and stato!=0:
        p.stop()
        stato=0
        
    if stato==1:#non so ancora dove girare, guardo entrambe i colori
            
        if trova_linea(1,img)==1:
            print("Prima riga trovata arancione, quindi stai andando in senso orario")
            stato=2
            p.destra90()
            conta=conta+1
            time.sleep(0.5)
            
        elif trova_linea(2,img)==1:
                print("Prima riga trovata blu, quindi stai andando in senso anti orario")
                stato=3
                p.sinistra90()
                conta=conta+1
                time.sleep(0.5)
        elif controllaOstacoli()==0:
            controllaBordi()
                
    elif stato==2:
        trovato=trova_linea(1,img)
        if trovato==1:
            print("riga trovata arancione")
            p.destra90()
            time.sleep(0.5)
            conta=conta+1
        elif controllaOstacoli()==0:
            controllaBordi()
    
    elif stato==3:
        trovato=trova_linea(2,img)
        if trovato==1:
            print("riga trovata blu")
            p.sinistra90()
            time.sleep(0.5)
            conta=conta+1
        elif controllaOstacoli()==0:
            controllaBordi()