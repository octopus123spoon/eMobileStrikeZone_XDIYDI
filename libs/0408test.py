import cv2
import numpy as np
import time

CNTS_MAX = 4000
CNTS_MIN = 50

'''
    a0 = r'/Users/teddy/Desktop/project/src/0323/0320_1_2124.jpg'
    a1 = r'/Users/teddy/Desktop/project/src/0323/0320_1_2125.jpg'
    a2 = r'/Users/teddy/Desktop/project/src/0323/0320_1_2126.jpg'

    a0 = r'/Users/teddy/Desktop/project/src/0323/0320_1_2147.jpg'
    a1 = r'/Users/teddy/Desktop/project/src/0323/0320_1_2148.jpg'
    a2 = r'/Users/teddy/Desktop/project/src/0323/0320_1_2149.jpg'
    '''
point = [[100,640],[820,640],[100,1920],[820,1920]]
def run(point):
    #a0 = r'/Users/teddy/Desktop/project/src/0323/0320_1_2124.jpg'
    a0 = r'/Users/asus/Desktop/New_eMobileStrikeZone_IP-main/src/0323/0320_1_2124.jpg'
    #a1 = r'/Users/teddy/Desktop/project/src/0323/0320_1_2125.jpg'
    a1 = r'/Users/asus/Desktop/New_eMobileStrikeZone_IP-main/src/0323/0320_1_2125.jpg'
    #a2 = r'/Users/teddy/Desktop/project/src/0323/0320_1_2126.jpg'
    a2 = r'/Users/asus/Desktop/New_eMobileStrikeZone_IP-main/src/0323/0320_1_2126.jpg'

    ia0 = cv2.imread(a0)
    ia0 = cv2.cvtColor(ia0, cv2.COLOR_BGR2GRAY)
    ia0 = cv2.resize(ia0[640:1920,100:820], (1080,1920), interpolation=cv2.INTER_CUBIC)
    ia1 = cv2.imread(a1)
    ia1 = cv2.cvtColor(ia1, cv2.COLOR_BGR2GRAY)
    ia1 = cv2.resize(ia1[640:1920,100:820], (1080,1920), interpolation=cv2.INTER_CUBIC)
    ia2 = cv2.imread(a2)
    ia2 = cv2.cvtColor(ia2, cv2.COLOR_BGR2GRAY)
    ia2 = cv2.resize(ia2[640:1920,100:820], (1080,1920), interpolation=cv2.INTER_CUBIC)

    a0a1 = cv2.absdiff(ia0,ia1)
    a1a2 = cv2.absdiff(ia1,ia2)
    a012 = cv2.bitwise_and(a0a1,a1a2)
    a012 = np.where(a012 >10 ,255,0).astype('uint8')

    kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    kernel5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    kernel7 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
    #a012 = cv2.erode(a012, kernel, iterations=1)
    a012 = cv2.dilate(a012, kernel5, iterations=1)
    a012 = cv2.erode(a012, kernel7, iterations=1)
    a012 = cv2.dilate(a012, kernel5, iterations=1)
    a012 = cv2.erode(a012, kernel3, iterations=1)
    
    aaaa = cv2.Canny(a012, 30, 150)
    #cv2.imshow('',aaaa)
    #cv2.waitKey(0)

    ret, thresh = cv2.threshold(a012, 25, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    out = cv2.cvtColor(a012, cv2.COLOR_GRAY2BGR)
    txt = open(r"/Users/asus/Desktop/New_eMobileStrikeZone_IP-main/rr.txt","w", encoding="utf-8")
    for c in cnts:
        #print(c)
        if cv2.contourArea(c) > CNTS_MAX:
            continue
        if cv2.contourArea(c) < CNTS_MIN:
            continue
        M = cv2.moments(c)
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])
        txt.write(str(cX) + ' ' + str(cY) + '\n')
        #print(cX,cY)
        cv2.circle(out, (cX, cY), 10, (255, 0, 0), -1)
        '''
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(out, (x, y), (x + w, y + h), (0, 255, 0), 2)'''

    txt.close()

    #cv2.drawContours(out, cnts, -1, (0, 255, 255), 2)
    cv2.imshow('',out)
    cv2.waitKey(0)
    
    



run(point)
