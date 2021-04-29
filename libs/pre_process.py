import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import sys


class Process_Image():
    def __init__(self, img, img2, area,mask):
        self.mask = mask
        self.img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.img = cv2.resize(self.img[area[0]:area[1],area[2]:area[3]], (1080,1920), interpolation=cv2.INTER_CUBIC)
        self.img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        self.img2 = cv2.resize(self.img2[area[0]:area[1],area[2]:area[3]], (1080,1920),interpolation=cv2.INTER_CUBIC)
        self.FDI(15)
        self.Close3()
        #self.FC()
        #self.Mask()
        #self.GB()
        self.HC()
        #self.out = self.img3

    def FDI(self, T):
        self.img3 = cv2.absdiff(self.img, self.img2)
        self.img3 = np.where(self.img3 > T, 255, 0).astype('uint8')

    def Close(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        self.img3 = cv2.morphologyEx(self.img3, cv2.MORPH_OPEN, kernel, iterations=1)
        self.img3 = cv2.dilate(self.img3, kernel, iterations=1)
        del kernel

    def Close2(self):
        kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        self.img3 = cv2.erode(self.img3, kernel3, iterations=1)
        self.img3 = cv2.dilate(self.img3, kernel, iterations=1)
        #self.img3 = cv2.erode(self.img3, kernel,iterations=2)
        #self.img3 = cv2.dilate(self.img3, kernel,iterations=1)
        #self.img3 = cv2.morphologyEx(self.img3, cv2.MORPH_OPEN, kernel,iterations = 2)
        #self.img3 = cv2.dilate(self.img3, kernel,iterations=1)
        del kernel

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

    def Mask(self):
        mask1 = np.zeros(self.img.shape[0:2], dtype="uint8")
        cv2.rectangle(mask1, self.mask[0:2], self.mask[2:4], 255, -1)
        self.img3 = cv2.add(self.img3, self.img3, mask=mask1)
        del mask1

    def GB(self):
        self.img3 = cv2.GaussianBlur(self.img3, (5, 5), 0)
        self.img3 = np.where(self.img3 > 1, 255, 0).astype('uint8')

    def HC(self):
        #self.point = cv2.HoughCircles(self.img3,cv2.HOUGH_GRADIENT,1, 150,param1=70,param2=10,minRadius=8,maxRadius=70)
        self.point = cv2.HoughCircles(self.img3, cv2.HOUGH_GRADIENT, 1, 150, param1=70, param2=10, minRadius=8, maxRadius=70)      
        self.out = cv2.cvtColor(self.img3, cv2.COLOR_GRAY2BGR)
        if self.point is None:
            print('none')
            pass
        else:
            #print(self.point)
            for i in self.point[0]:
                leftup = [int(i[0]-i[2]),int(i[1]-i[2])]
                tmp = self.img3[leftup[1]:leftup[1]+int(2*i[2]),leftup[0]:leftup[0]+int(2*i[2])]
                #tmp = self.out[leftup[0]:leftup[0]+int(2*i[2]),leftup[1]:leftup[1]+int(2*i[2])]
                #print(leftup[0],leftup[0]+int(2*i[2]),leftup[1],leftup[1]+int(2*i[2]))
                #print(int(2*i[2])*int(2*i[2]))
                if cv2.countNonZero(tmp) >= int(2*i[2]*2*i[2]*0.55):
                    #text = str(int(2*i[2]*2*i[2]*0.65)) + ' ' + str(cv2.countNonZero(tmp))
                    #cv2.putText(self.out, text, (leftup[0],leftup[1]), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.circle(self.out, (i[0], i[1]), int(i[2]), (0, 0, 255), 3)

    def FC(self):
        ret, thresh = cv2.threshold(self.img3, 125, 255, 1)
        cnts, hierarchy = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.out = cv2.cvtColor(self.img3, cv2.COLOR_GRAY2BGR)
        for c in cnts:
            if cv2.contourArea(c) < 80:
                continue
            if cv2.contourArea(c) > 3000:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(self.out, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.drawContours(self.out, cnts, -1, (0, 255, 255), 2)



'''
listA = [['606','607'],['878','879'],["894","895"],["3878","3879"],["4196","4197"]]
for i in listA:
    pa = "/Users/teddy/Desktop/project/src/0311/"+i[0]+".jpg"
    pb = "/Users/teddy/Desktop/project/src/0311/"+i[1]+".jpg"
    print(pa,pb)
    i1 = cv2.imread(pa)
    i2 = cv2.imread(pb)
    A = Process_Image(i1,i2,[0,1920,0,1080],(0,400,1080,1300))
    cv2.imwrite(i[0]+'+'+i[1]+'_2.jpg',A.out)



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