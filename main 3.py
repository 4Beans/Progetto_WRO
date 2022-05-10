#Imports
import cv2
import numpy as np
import imutils

#Def Functions
def Stop():
    print("Stop")

def trova_colore(immagine,col):
#colori: 1 arancione 2 blu 3 nero 4 rosso 5 verde
    hsv = cv2.cvtColor(immagine, cv2.COLOR_BGR2HSV)
    if col==1:
        low = np.array([(0, 145, 130)])
        high = np.array([(50, 255, 255)])
    if col==2:
        low = np.array([(105, 190, 0)])
        high = np.array([(115, 255, 255)])
    if col==3:
        low = np.array([(0, 145, 130)]) #momentaneamente uguali all'arancione per testarlo, non riesco a trovare i valori del nero
        high = np.array([(50, 255, 255)])
    mask = cv2.inRange(hsv, low, high)
    cnts = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)#problemi di compatibilità
    if len(cnts)!=0:
        for c in (cnts):
            #calcolo l'area della zona colorata
            if cv2.contourArea(c)>200:
                return 1
    return 0
    
def linea(immagine):
    sx=immagine[360:480,140:180]
    dx=immagine[360:480,460:500]
    cv2.rectangle(immagine,(140,360),(180,480),(255,0,0),1)#sx
    cv2.rectangle(immagine,(460,360),(500,480),(255,0,0),1)#dx
    return (sx,dx)
    
def trova_linea(col,immagine):
    (sx,dx)=linea(immagine)
    if trova_colore(sx,col)==1 and trova_colore(dx,col)==1:
        if col==1:
            return (2,1)
        else:
            return (1,2)         
    return (col,0)

def barreNere(immagine):
    sx=immagine[360:480,140:180]
    dx=immagine[360:480,460:500]
    cv2.rectangle(immagine,(0,180),(50,300),(255,0,0),1)#sx
    cv2.rectangle(immagine,(720,180),(590,300),(255,0,0),1)#dx Forse destra e sinistra non sono simmetricamente perfetti ma non riuscivo a trovare i valori giusti 
    return (sx,dx) 

#Initalizations
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
countOrange=0
countBlue=0
stato=1 #Stato 1=Cerca arancio 2=Cerca blu
trovato=0
giro=0

#Main
print("vai")
while True:
    print("Sto andando")
    if countOrange==3 and countBlue==3:#Ho messo 3 per testarlo velocemente, poi ovviamente si rimette 12
        Stop()
        break   
    #Prende immagini dalla cam e le mostra ad ogni iterazione del ciclo
    ret,img=cap.read()  
    if giro!=0:
        (stato,trovato)=trova_linea(stato,img)
        print(stato)
        if trovato==0:
            print("colore non trovato")
        if trovato==1:
            countOrange+=1
            print(countOrange)
        if trovato==2:
            countBlue+=1
            print(countBlue)
    else:
        (stato,trovato)=trova_linea(1,img)
        if trovato!=0:
            giro=trovato
            print("Prima riga trovata arancione, quindi stai andando in senso orario")
        else:    
            (stato,trovato)=trova_linea(2,img)
            if trovato!=0:
                giro=trovato
                print("Prima riga trovata blu, quindi stai andando in senso anti orario")
    (barraSx,barraDx)=barreNere(img)
    if trova_colore(barraSx,3)==1:
        print("Sei molto vicino al bordo nero a sinistra")
    if trova_colore(barraDx,3)==1:
        print("Sei molto vicino al bordo nero a destra")
    cv2.imshow("cam",img)
    k=cv2.waitKey(100)
    #Incrementi per testare
    #countOrange+=1
    #countBlue+=1
