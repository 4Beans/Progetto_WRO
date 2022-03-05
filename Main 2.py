#Imports
import cv2

#Def Functions
def Stop():
    print("Stop")

#Initalizations
cap=cv2.VideoCapture(0)
countOrange=0
countBlue=0

#Main
while True:
    if countOrange==12 and countBlue==12:
        Stop()
        break
    print("Vai") 
    #Prende immagini dalla cam e le mostra ad ogni iterazione del ciclo
    ret,img=cap.read()
    cv2.imshow("cam",img)
    k=cv2.waitKey(1000)
    #Incrementi per testare
    countOrange+=1
    countBlue+=1
input("Premi un tasto per continuare")