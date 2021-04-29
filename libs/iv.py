import cv2
from pre_process import Process_Image
import sys

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
        self.run()
    def run(self):
        Output = []
        ret, frame = self.vc.read()
        t0 = frame
        mask = (0,0,1080,1920)#(0,400,1080,1300)
        while self.vc.isOpened():
            ret, frame = self.vc.read()
            print(self.vc.get(0))
            if not ret:
                break
            t1 = frame
            T = Process_Image(t0,t1,self.area,mask)
            #tmp = cv2.add(t1,T.out)
            #tmp = cv2.add(t1,cv2.cvtColor(T.out, cv2.COLOR_GRAY2BGR))
            tmp = T.out
            Output.append(tmp)
            t0 = t1
            del T
            del tmp
        self.vc.release()
        VW = cv2.VideoWriter(self.OutPath, cv2.VideoWriter_fourcc(*'mp4v'), self.FPS, (self.w, self.h),isColor = True)#,isColor = False
        for i in range(len(Output)):
            VW.write(Output[i])
        VW.release()



            
#a = Input_Video(r"/Users/teddy/Desktop/project/src/0320/0320_1_96262/0320_1_1.mp4",'0320_1_1_F.mp4')
b = Input_Video(r"/Users/teddy/Desktop/project/src/0320/0320_1_96262/0320_1_2.mp4",'0320_1_2_F.mp4',[640,1920,100,820])
#c = Input_Video(r"/Users/teddy/Desktop/project/src/0320/0320_1_96262/0320_1_3.mp4",'0320_1_3_F.mp4')
#d = Input_Video(r"/Users/teddy/Desktop/project/src/0320/0320_1_96262/0320_1_4.mp4",'0320_1_4_F.mp4')
#e = Input_Video(r"/Users/teddy/Desktop/project/src/0320/0320_1_96262/0320_1_5.mp4",'0320_1_5_F.mp4')
#f = Input_Video(r"/Users/teddy/Desktop/project/src/0320/0320_1_96262/0320_1_6.mp4",'0320_1_6_F.mp4')
