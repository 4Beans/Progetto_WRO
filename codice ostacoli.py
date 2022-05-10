#Imports
import cv2
import numpy as np
import imutils

#Def Functions
def Stop():
    print("Stop")
    
def trova_colore(immagine,col):
    global cx,cy
# colori: 1 - arancione 2 blu da modificare
    hsv = cv2.cvtColor(immagine, cv2.COLOR_BGR2HSV)
    if col==1:
        low = np.array([(0, 145, 130)])
        high =np.array([(50, 255, 255)])
    if col==2:
        low = np.array([(99, 192, 105)])
        high =np.array([(120, 255, 255)])
    mask = cv2.inRange(hsv, low, high)
    cv2.imshow("arancione",mask)
    cnts = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)#problemi di compatibilità
    if len(cnts)!=0:
        c = max(cnts, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        cx=(x+w)
        
        return 1
    return 0

        
#Initalizations
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cx=0
cy=0
print("vai")
#Main
while True:

    #Prende immagini dalla cam e le mostra ad ogni iterazione del ciclo
    ret,img=cap.read()
    cv2.imshow("cam",img)
    k=cv2.waitKey(1)
    centro=trova_colore(img,1)
    if centro!=0:
        print(cx,cy)
        rcx=cx
        rcy=cy
        
        if (cx-100)>50:
            print("destra-raddrizza")
        
   # legge ultrasuono    
   # se è minore di tot
   #    legge destro se è > di tot1 curva a dx e raddrizza
   