'''    def FDI(self,T):#T介於15~30
        self.img3 = self.img2.astype(int) - self.img.astype(int)
        self.img3 = np.where(self.img3>T ,255,0).astype('uint8')'''