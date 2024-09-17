import os
from cvzone.HandTrackingModule import HandDetector
import cv2
from select import select

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgBackground = cv2.imread("ARKAPLAN.png") # Bu fonksiyon, belirtilen dosya yolundan bir görüntü dosyasını okur. Eğer dosya başarıyla okunursa, görüntüyü bir NumPy dizisi olarak döndürür

# Modes resimlerini liste haline getirme
folderPathModes =  "Modes"
listImgModesPath =os.listdir(folderPathModes)
listImgModes = []
for imgModePath in listImgModesPath:
    listImgModes.append(cv2.imread(os.path.join(folderPathModes,imgModePath)))

# Icon resimlerini liste haline getirme
folderPathIcon =  "Icon"
listImgIconPath =os.listdir(folderPathIcon)
listImgIcon = []
for imgIconPath in listImgIconPath:
    listImgIcon.append(cv2.imread(os.path.join(folderPathIcon,imgIconPath)))

selection =-1
ModesType =0
counter = 0 # sayaç
selectionSpeed = 7
modelPositions = [(1136,196),(1000,384),(1136,581)]
counterPause = 0
selectionList = [-1,-1,-1]

detector = HandDetector(detectionCon=0.8,maxHands=1)

while True:
    success , img = cap.read()
    hands , img = detector.findHands(img)
    imgBackground[142:142+480,43:43+640] = img # , ün sol kısmı yüksekliğin nerde başlayıp nerde bittiğini gösterir , sağ tarafı ise genişliğin nerde başlayıp nerde bittiğini gösterir
    imgBackground[0:705, 847:1270] = listImgModes[ModesType]

    if hands and counterPause == 0 and ModesType<3:
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        print(fingers1)

        if fingers1 == [0,1,0,0,0]:
            if selection != 1:
                counter = 1
            selection=1

        elif fingers1 == [0,1,1,0,0]:
            if selection != 2:
                counter = 1
            selection=2

        elif fingers1 == [0,1,1,1,0]:
            if selection != 3:
                counter = 1
            selection=3

        else:
            selection = -1
            counter = 0

        if counter > 0 :
            counter+=1
            print(counter)

            cv2.ellipse(imgBackground,modelPositions[selection-1],(103,103),0,0,counter*selectionSpeed,(0,255,0),20)
            # cv2.ellipse fonksiyonu, belirtilen parametrelerle bir görüntü üzerine elips çizmemizi sağlar
            # modelPositions[selection-1]: Elipsin merkezi olan noktanın koordinatları. Bu, çizilecek elipsin merkezinin görüntüdeki konumunu belirtir
            # (103, 103): Elipsin büyüklüğünü belirten yarı eksen uzunlukları (genişlik, yükseklik). Her iki değer de 103 olduğu için bu, aslında çizilen şeklin bir daire olduğunu görürüz
            # 0: Elipsin dönme açısı
            # 0: Başlangıç açısı
            # counter*selectionSpeed: Bitiş açısı. Bu değer, elipsin kaç derecelik bir yay çizeceğini belirler. counter ve selectionSpeed değişkenlerinin çarpımı ile hesaplanır, bu da dinamik bir bitiş açısı sağlar. Kullanıcı etkileşimine göre bu açı değişebilir, böylece elipsin doluluk oranı değişir
            # (0, 255, 0): Elipsin rengi. Bu durumda yeşil renk
            # 20: Elipsin çizgi kalınlığı
            if counter*selectionSpeed>360:
                selectionList[ModesType]=selection
                ModesType +=1
                counter = 0
                selection = -1
                counterPause = 1
    if counterPause>0:
        counterPause+=1
        if counterPause > 60:
            counterPause = 0

    if selectionList[0] != -1:
        imgBackground[640:640+65,125:125+65] = listImgIcon[selectionList[0]-1]
    if selectionList[1] != -1:
        imgBackground[640:640+65,332:332+65] = listImgIcon[2+selectionList[1]]
    if selectionList[2] != -1:
        imgBackground[640:640+65,534:534+65] = listImgIcon[5+selectionList[2]]


    cv2.imshow("Background",imgBackground)
    cv2.waitKey(1)