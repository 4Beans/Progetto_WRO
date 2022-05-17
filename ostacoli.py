#Imports
import cv2
import numpy as np
import imutils

#Def Functions
def Stop():
    print("Stop")
    
def trova_colore(immagine,col):
    global cx
# colori: 1 - arancione 2 blu da modificare
    hsv = cv2.cvtColor(immagine, cv2.COLOR_BGR2HSV)
    if col==1:
        low = np.array([(0,126,45)])
        high =np.array([(9, 255, 255)])
    if col==2:
        low = np.array([36,50,50])
        high =np.array([85,255,255])
    mask = cv2.inRange(hsv, low, high)
    cv2.imshow("maschera",mask)
    cnts = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)#problemi di compatibilità
    if len(cnts)!=0:
        c = max(cnts, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        area=w*h
        if area>500:
            return area
    return 0

        
#Initalizations
cap=cv2.VideoCapture(0)
cap.set(3,160)
cap.set(4,120)
cx=0
print("vai")
#Main
while True:

    #Prende immagini dalla cam e le mostra ad ogni iterazione del ciclo
    ret,img=cap.read()
    cv2.imshow("cam",img)
    k=cv2.waitKey(1)
    centro=trova_colore(img,1)
    cxr=cx
    centro2=trova_colore(img,2)
    print(centro,centro2)
    if centro>centro2:
            print("destra-raddrizza")
    elif centro2>centro:
            print("sinistra-raddrizza")
  