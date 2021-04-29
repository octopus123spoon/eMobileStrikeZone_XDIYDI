import cv2
import numpy as np
import time
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
    #a1 = r'/Users/teddy/Desktop/project/src/0323/0320_1_2125.jpg'
    #a2 = r'/Users/teddy/Desktop/project/src/0323/0320_1_2126.jpg'
    a0 = r'/Users/asus/Desktop/New_eMobileStrikeZone_IP-main/src/0323/0320_1_2124.jpg'
    a1 = r'/Users/asus/Desktop/New_eMobileStrikeZone_IP-main/src/0323/0320_1_2125.jpg'
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

    t0 = time.time()
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
    #a012 = cv2.morphologyEx(a012, cv2.MORPH_CLOSE, kernel, iterations=1)
    a012 = cv2.GaussianBlur(a012, (7, 7), 0)
    
    '''
    ret, thresh = cv2.threshold(a012, 100, 255, 1)
    cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
    out = np.where(a012,0,0).astype('uint8')
    out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(out, cnts, -1, (255, 255, 255), 3)
    cv2.imshow('',out)
    cv2.waitKey(0)  '''

    ball = cv2.HoughCircles(a012, cv2.HOUGH_GRADIENT, 1, 100, param1=10, param2=15, minRadius=0, maxRadius=70)
    a012 = cv2.cvtColor(a012, cv2.COLOR_GRAY2BGR)
    for i in ball[0]:
        cv2.circle(a012, (i[0], i[1]), int(i[2]), (0, 0, 255), 5)
    t1 = time.time()
    print(t1-t0)
    cv2.imshow('',a012)
    cv2.waitKey(0)



run(point)