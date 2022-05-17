import cv2
import imutils
import numpy as np


#pre elaborazione e filtro di soglia per identificare il nero
def filtra(frame):
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15,15), 0)
    (T, thresh) = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("fin",thresh)
    return thresh
 
  

    
    
def bordi(mask):    
    #trovare i contorni
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)#problemi di compatibilità
    
    if len(cnts)!=0:
        c = max(cnts, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        cx=(x+w)
        if cx>90:
            return 1
        if cx<70:
            return -1
    return 0
           
#************************MAIN***************************************
MAXX=160
MAXY=120

cap = cv2.VideoCapture(0)
cap.set(3, MAXX)
cap.set(4, MAXY)
if not cap.isOpened():
   cap.open(0)
while 1:   
    ret, frame = cap.read()
    cv2.imshow("finestra",frame)
    mask=filtra(frame)
    print(bordi(mask))
    if bordi(mask)==1: #Quindi trova bordo a destra
        print("Trovato bordo a destra, raddrizzati a sinistra")
        #p.correggiSinistra()
    else:
        if bordi(mask)==-1: #Quindi trova bordo a sinistra
            print("Trovato bordo a sinistra, raddrizzati a sinistra")
            #p.correggiDestra()
    if cv2.waitKey(1)==ord('q'):
        break