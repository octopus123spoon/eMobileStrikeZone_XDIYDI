import cv2
from pre_process0408 import Process_Image
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

class Input_Video():
    def __init__(self,path,outpath,area):
        self.Path = path
        self.OutPath = outpath
        self.area = area
        self.vc = cv2.VideoCapture(self.Path)
        self.FPS = self.vc.get(5)
        self.FrameCount = int(self.vc.get(7))
        self.w = int(self.vc.get(3))
        self.h = int(self.vc.get(4))
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.XDI = []
        self.YDI = []
        self.run()
        self.xdiydi()
        self.condline = []
        self.xyline()
    def run(self):
        Output = []
        ret, frame = self.vc.read()
        t0 = frame
        mask = (0,0,1080,1920)#(0,400,1080,1300)
        while self.vc.isOpened():
            ret, frame = self.vc.read()
            if not ret:
                break
            t1 = frame
            T = Process_Image(t0, t1, self.area, mask)
            tmp = [int(self.vc.get(1)) for _ in range(len(T.CenterPointX))]
            self.XDI.append([T.CenterPointX,tmp])
            self.YDI.append([T.CenterPointY,tmp])
            cv2.putText(T.out, 'Frame:'+str(self.vc.get(1)), (40, 200), cv2.FONT_HERSHEY_SIMPLEX,3, (0, 255, 255), 3, cv2.LINE_AA)
            Output.append(T.out)
            t0 = t1
            del T 
            del tmp
        self.vc.release()
        VW = cv2.VideoWriter(self.OutPath, cv2.VideoWriter_fourcc(*'mp4v'), self.FPS, (self.w, self.h),isColor = True)#,isColor = False
        for i in range(len(Output)):
            VW.write(Output[i])
        VW.release()


    def xdiydi(self):
        '''
        txt = open(r"/Users/teddy/Desktop/Project/XDI.txt","w+", encoding="utf-8")
        for i in self.XDI:
            txt.write(str(i) + '\n')
        txt.close()

        txt = open(r"/Users/teddy/Desktop/Project/YDI.txt","w+", encoding="utf-8")
        for i in self.YDI:
            txt.write(str(i) + '\n')
        txt.close()'''

        #print(len(self.XDI))
        #print(len(self.YDI))
        
        plt.figure(figsize=(20,10))
        plt.subplot(2,1,1)
        plt.title("XDI")
        for i in self.XDI:
            plt.scatter(i[1],i[0],c='k') 

        plt.subplot(2,1,2)
        plt.title("YDI")
        for i in self.YDI:
            plt.scatter(i[1],i[0],c='k') 
        #plt.savefig(self.OutPath[:-4]+"_out.png")
        plt.savefig(self.OutPath[:-4]+"_out_2.png")


    def xyline(self):
        tmp = [[]]
        k = 0
        tkc = 0
        outr = 0
        i = 0
        g = 0
        #print(len(self.XDI[14]))
        for l in range(len(self.XDI)):
            i = g
            while i in range(len(self.XDI)):
                print (i)
                #print(i[0], end = " ")
                for j in range(len(self.XDI[i][0])):
                    #print(j, end = " ")
                    if tmp[k] == []:
                        tmp[k].append([self.XDI[i][0][j],self.XDI[i][1][j]])
                        tkc = 0
                        break
                    elif abs(int(self.XDI[i][0][j])-int(tmp[k][tkc][0])) <=100 and int(self.XDI[i][1][j]-tmp[k][tkc][1]) == 1:
                        tmp[k].append([self.XDI[i][0][j],self.XDI[i][1][j]])
                        tkc = tkc+1
                        break
                    elif int(self.XDI[i][1][j]-tmp[k][tkc][1]) >= 2:
                        print(self.XDI[i][1][j]-tmp[k][tkc][1]," ",self.XDI[i][1][j]," ",tmp[k][tkc][1])
                        outr = 1
                        break
                i = i+1
                if outr == 1:
                    tmp.append([])
                    k = k+1
                    tkc = 0
                    break
            if outr == 1:
                outr = 0
                g = g+1
                

        '''if not j and abs(int(self.XDI[i][0][j])-int(self.XDI[i][0][j+1])) <100:
            tmp.append([self.XDI[i][0][j],self.XDI[i][1][j]])
            continue
        else:
            continue
        if j and abs(int(self.XDI[i][0][j])-int(tmp[f][k])) < 100:
            tmp.append(f,i[0][j])
            k = k + 1'''
        '''
        tmp2 = [[]]
        k = 0
        for i in range(len(self.XDI)):
            #print(i[0], end = " ")
            for j in range(len(self.XDI[i][0])):
                #print(j, end = " ")
                #try:
                    a = int(self.XDI[i][0][j])
                    print(self.XDI[i][0][j],end = ', ')
                    tmp[k].append([self.XDI[i][0][j],self.XDI[i][1][j]])
                #except IndexError:
                   # pass
            #tmp.append([None,tmp2])
            if i == 2:
                tmp.append([])
                k = k + 1
            if i > 3: break
            print("")            
            f = f + 1
        '''
        '''
            m = int(self.XDI[12][0][0])
            try:
                if self.XDI[14][0][0].isnull():
                    print("Okay")
                else:
                     print("nope")
            except IndexError:
                print("sss")
                pass
            if  j and abs(int(self.XDI[4][0][0])-int(self.XDI[5][0][0])) < 100:
                print("Yeah")
                print(abs(int(self.XDI[4][0][0])-int(self.XDI[5][0][0]))," ",j)
                break
            else:
                print("X")
                print(abs(int(self.XDI[4][0][0])-int(self.XDI[5][0][0]))," ",j)
                break
            #break
        '''
        print("------------------------------")
        for i in tmp:
            print(i)
        #print(self.XDI[7][0][1])
        #for i in self.XDI:
            #print(i,". ",i[1]," ",i[0],"\n")
            #for j in self.XDI
        '''for i in self.XDI:
            print(i, end="\n")'''


            
t0 = time.time()
#a = Input_Video(r"/Users/teddy/Desktop/Project/src/0311/V_20210311_152331_ES0_05332/A3.mp4",'A3.mp4',[400,1600,200,875])
a = Input_Video(r"/Users/asus/Desktop/New_eMobileStrikeZone_IP-main\src/0311/V_20210311_152331_ES0_05332/A3.mp4",'A3.mp4',[400,1600,200,875])
#a = Input_Video(r"C:/Users/asus/Desktop/New_eMobileStrikeZone_IP-main/src/0320/0320_1_96262/0320_1_1_F.mp4",'A3.mp4',[400,1600,200,875])
t1 = time.time()

'''
t0 = time.time()
a = Input_Video(r"/Users/teddy/Desktop/project/src/0320/0320_1_96262/0320_1_1.mp4",'0320_1_1_F.mp4',[640,1920,100,820])
t1 = time.time()
print(t1-t0)
b = Input_Video(r"/Users/teddy/Desktop/project/src/0320/0320_1_96262/0320_1_2.mp4",'0320_1_2_F.mp4',[640,1920,100,820])
t2 = time.time()
print(t2-t1)
c = Input_Video(r"/Users/teddy/Desktop/project/src/0320/0320_1_96262/0320_1_3.mp4",'0320_1_3_F.mp4',[640,1920,100,820])
t3 = time.time()
print(t3-t2)
d = Input_Video(r"/Users/teddy/Desktop/project/src/0320/0320_1_96262/0320_1_4.mp4",'0320_1_4_F.mp4',[640,1920,100,820])
t4 = time.time()
print(t4-t3)
e = Input_Video(r"/Users/teddy/Desktop/project/src/0320/0320_1_96262/0320_1_5.mp4",'0320_1_5_F.mp4',[640,1920,100,820])
t5 = time.time()
print(t5-t4)
f = Input_Video(r"/Users/teddy/Desktop/project/src/0320/0320_1_96262/0320_1_6.mp4",'0320_1_6_F.mp4',[640,1920,100,820])
t6 = time.time()
print(t6-t5)
'''