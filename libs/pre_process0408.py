import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import sys

CNTS_MAX = 30000
CNTS_MIN = 70

class Process_Image():
    def __init__(self, img, img2, area, mask):
        self.mask = mask
        self.CenterPoint = []
        self.CenterPointX = []
        self.CenterPointY = []
        self.img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.img = cv2.resize(self.img[area[0]:area[1],area[2]:area[3]], (1080,1920), interpolation=cv2.INTER_CUBIC)
        self.img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        self.img2 = cv2.resize(self.img2[area[0]:area[1],area[2]:area[3]], (1080,1920),interpolation=cv2.INTER_CUBIC)
        self.FDI(15)
        self.Close3()
        self.findCenter()

    def FDI(self, T):
        self.img3 = cv2.absdiff(self.img, self.img2)
        self.img3 = np.where(self.img3 > T, 255, 0).astype('uint8')

    def Close3(self):
        kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        kernel5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        kernel7 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
        self.img3 = cv2.dilate(self.img3, kernel5, iterations=1)
        self.img3 = cv2.erode(self.img3, kernel7, iterations=1)
        self.img3 = cv2.dilate(self.img3, kernel5, iterations=1)
        self.img3 = cv2.erode(self.img3, kernel3, iterations=1)
        del kernel3
        del kernel5
        del kernel7

    def findCenter(self):
        self.out = cv2.cvtColor(self.img3,cv2.COLOR_GRAY2BGR)
        ret, thresh = cv2.threshold(self.img3, 25, 255, cv2.THRESH_BINARY)
        cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #txt = open(r"/Users/teddy/Desktop/Project/PRINT.txt","w+", encoding="utf-8")
        
        for c in cnts:
            #print(c)
            area = int(cv2.contourArea(c))
            if area > CNTS_MAX:
                continue
            if area < CNTS_MIN:
                continue
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            circle = int(radius*radius*3.14)
            #txt.write(str(x)+' '+str(y)+' ' + str(circle)+ " ===> "+str(area))
            if area >= circle*0.45: 
                #txt.write(" OK!")
                #cv2.circle(self.out, (int(x), int(y)), 10, (0, 0, 255), -1)
                cv2.circle(self.out, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                self.CenterPoint.append([int(x), int(y)])
                self.CenterPointX.append(int(x))
                self.CenterPointY.append(int(y))

            #txt.write("\n")
        #txt.close()
            




'''
#listA = [['606','607'],['878','879'],["894","895"],["3878","3879"],["4196","4197"]]
listA = [['606','607']]
for i in listA:
    pa = "/Users/teddy/Desktop/project/src/0311/"+i[0]+".jpg"
    pb = "/Users/teddy/Desktop/project/src/0311/"+i[1]+".jpg"
    print(pa,pb)
    i1 = cv2.imread(pa)
    i2 = cv2.imread(pb)
    A = Process_Image(i1,i2,[0,1920,0,1080],(0,400,1080,1300))
    print(A.CenterPoint)
'''
'''
listA = [['0320_1_2124','0320_1_2125'],['0320_1_2125','0320_1_2126'],["0320_1_2147","0320_1_2148"],["0320_1_2148","0320_1_2149"]]
#listA = [['0320_1_2124','0320_1_2125']]
for i in listA:
    pa = "/Users/teddy/Desktop/project/src/0323/"+i[0]+".jpg"
    pb = "/Users/teddy/Desktop/project/src/0323/"+i[1]+".jpg"
    print(pa,pb)
    i1 = cv2.imread(pa)
    i2 = cv2.imread(pb)
    t0 = time.time()
    A = Process_Image(i1,i2,[640,1920,100,820],(0,400,1080,1300))
    t1 = time.time()
    print(t1-t0)
    cv2.imwrite(i[0]+'+'+i[1]+'_2.jpg',A.out)'''