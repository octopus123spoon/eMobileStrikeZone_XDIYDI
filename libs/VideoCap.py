import os
import numpy as np
import cv2
import time 


class VideoCap():
    def __init__(self,path):
        self.path = path
        self.Out_Dir = self.path[:-4] + '_' + str(time.time())[-5:] + '/'
        if os.path.isdir(self.Out_Dir):
            pass
        else:
            os.makedirs(self.Out_Dir)
        self.vc = cv2.VideoCapture(self.path)
        self.FPS = self.vc.get(5)
        self.FrameCount = int(self.vc.get(7))
        self.w = int(self.vc.get(3))
        self.h = int(self.vc.get(4))
        self.fourcc = int(self.vc.get(6))
        self.print = False
        self.vc.release()

    def CutByMs(self,name, start, end):
        video = []
        vc = cv2.VideoCapture(self.path)
        vc.set(cv2.CAP_PROP_POS_FRAMES,int(start/1000*self.FPS))
        vc.read()
        print('Start Cutting......')
        while vc.isOpened():
            ret, frame = vc.read()
            if self.print:
                print(vc.get(0))
            if not ret:
                break
            if vc.get(0) >= end:
                break
            if vc.get(0) >= start:
                video.append(frame)
            #cv2.imshow('frame', frame)
            #if cv2.waitKey(1) == ord('q'):
            #    break
        vc.release()
        out = cv2.VideoWriter(self.Out_Dir+name, cv2.VideoWriter_fourcc(*'mp4v'), self.FPS, (self.w, self.h))
        for i in range(len(video)):
            out.write(video[i])
        out.release()
        print('Cut Finish!!')



    def CutByFrame(self, name, start, end):
        video = []
        vc = cv2.VideoCapture(self.path)
        vc.set(cv2.CAP_PROP_POS_FRAMES,int(start))
        vc.read()
        print('Start Cutting......')
        while vc.isOpened():
            ret, frame = vc.read()
            if self.print:
                print(vc.get(1))
            if not ret:
                break
            if vc.get(1) >= end:
                break
            if vc.get(1) >= start:
                video.append(frame)
            #cv2.imshow('frame', frame)
            #if cv2.waitKey(1) == ord('q'):
            #    break
        vc.release()
        out = cv2.VideoWriter(self.Out_Dir+name, cv2.VideoWriter_fourcc(*'mp4v'), self.FPS, (self.w, self.h))
        for i in range(len(video)):
            out.write(video[i])
        out.release()
        print('Cut Finish!!')

    def CapByMs(self, start, end):
        filename = self.path.split('/')[-1][:-4]
        count = 1
        vc = cv2.VideoCapture(self.path)
        vc.set(cv2.CAP_PROP_POS_FRAMES,int(start/1000*self.FPS))
        vc.read()
        print('Start Capturing......')
        while vc.isOpened():
            ret, frame = vc.read()
            if self.print:
                print(vc.get(0))
            if not ret:
                break
            if vc.get(0) >= end:
                break
            if vc.get(0) >= start:
                cv2.imwrite(self.Out_Dir+filename+str(count)+'.jpg',frame)
                count += 1
            #cv2.imshow('frame', frame)
            #if cv2.waitKey(1) == ord('q'):
            #    break
        vc.release()
        print('Capture Finish!!')
    
    def CapByFrame(self, start, end):
        filename = self.path.split('/')[-1][:-4]
        count = 1
        vc = cv2.VideoCapture(self.path)
        vc.set(cv2.CAP_PROP_POS_FRAMES,int(start))
        vc.read()
        print('Start Capturing......')
        while vc.isOpened():
            ret, frame = vc.read()
            if self.print:
                print(vc.get(1))
            if not ret:
                break
            if vc.get(1) >= end:
                break
            if vc.get(1) >= start:
                cv2.imwrite(self.Out_Dir+filename+str(count)+'.jpg',frame)
                count += 1
            #cv2.imshow('frame', frame)
            #if cv2.waitKey(1) == ord('q'):
            #    break
        vc.release()
        print('Capture Finish!!')

    def TFMByMs(self, start, end):
        filename = self.path.split('/')[-1][:-4]
        vc = cv2.VideoCapture(self.path)
        vc.set(cv2.CAP_PROP_POS_FRAMES,int(start/1000*self.FPS))
        ret,frame = vc.read()
        shape = frame.shape
        Output = np.zeros((shape[0], shape[1]))
        tmp1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print('Start Capturing......')
        while vc.isOpened():
            ret, frame = vc.read()
            if self.print:
                print(vc.get(0))
            if not ret:
                break
            if vc.get(0) >= end:
                break
            if vc.get(0) >= start:
                tmp2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                Output += abs(tmp2.astype(int)-tmp1.astype(int))
                tmp1 = tmp2
            #cv2.imshow('frame', frame)
            #if cv2.waitKey(1) == ord('q'):
            #    break
        vc.release()
        cv2.imwrite(self.Out_Dir+ 'TFM_Output_' + str(time.time())[-5:]  +'.jpg',Output)
        print('Capture Finish!!')

A = VideoCap(r'/Users/teddy/Desktop/project/src/0320/0320_1_96262/0320_1_2.mp4')
A.CapByFrame(0,9999)

'''
A.CutByMs('0320_1_1.mp4',4500,7500)
A.CutByMs('0320_1_2.mp4',16000,19000)
A.CutByMs('0320_1_3.mp4',27000,30000)
A.CutByMs('0320_1_4.mp4',40000,43500)
A.CutByMs('0320_1_5.mp4',52000,56000)
A.CutByMs('0320_1_6.mp4',63000,67000)'''