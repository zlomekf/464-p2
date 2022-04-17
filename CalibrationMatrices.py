import numpy as np
import matplotlib.pyplot as plt

class CalibrationMatrices():
    def __init__(self, *arg,**kw):        
        self.is_hamburger_style = True

        self.PAPER_X = 21.6 #paper short side in CM
        self.PAPER_Y = 28.0 #paper long side in CM

        self.DIST = 4 #distance in CM between calibration points
        self.NUM_X = 5
        self.NUM_Y = 7

        self.measured = np.zeros((self.NUM_Y, self.NUM_X, 3))
        self.interpolated = np.zeros((self.DIST*self.NUM_Y - (self.DIST-1), self.DIST*self.NUM_X - (self.DIST-1), 3))
    


    def construct_interpolation(self):
        for i in range(0, self.measured.shape[0]):
            for j in range(0, self.measured.shape[1]):
                self.interpolated[self.DIST*i, self.DIST*j] = self.measured[i,j]

        for i in range(0, self.measured.shape[0]-1):
            for j in range(0, self.measured.shape[1]):
                self.interpolated[i*self.DIST + 1,j*self.DIST] = (3*self.measured[i,j] + self.measured[i+1,j]) / 4
                self.interpolated[i*self.DIST + 2,j*self.DIST] = (self.measured[i,j] +self. measured[i+1,j]) / 2
                self.interpolated[i*self.DIST + 3,j*self.DIST] = (self.measured[i,j] + 3*self.measured[i+1,j]) /4

        for i in range(0, self.interpolated.shape[0]):
            for j in range(0,self.measured.shape[1]-1):
                self.interpolated[i, j*self.DIST + 2] = (self.interpolated[i, j*self.DIST] + self.interpolated[i, (j+1)*self.DIST]) /2

        for i in range(0, self.interpolated.shape[0]):
            for j in range(0,self.measured.shape[1]-1):
                self.interpolated[i, j*self.DIST + 1] = (self.interpolated[i, j*self.DIST] + self.interpolated[i, j*self.DIST+2]) /2
                self.interpolated[i, j*self.DIST + 3] = (self.interpolated[i, j*self.DIST + 2] + self.interpolated[i, j*self.DIST+4]) /2

    def main(self):
        self.measured = np.zeros((self.NUM_Y,self.NUM_X))
        for i in range(0, self.measured.shape[0]):
            for j in range(0, self.measured.shape[1]):
                self.measured[i,j] = i+j

        self.interpolated = np.zeros((self.DIST*self.NUM_Y - (self.DIST-1), self.DIST*self.NUM_X - (self.DIST-1)))

        if not self.is_hamburger_style:
            self.measured = self.measured.T
            self.interpolated = self.interpolated.T

        self.construct_interpolation()
        print(self.interpolated.shape)

        for i in range(0, self.interpolated.shape[1]):
          values = self.interpolated[0,i]
          print(i)
          print(values)
        
        plt.imshow(self.interpolated, cmap='hot', interpolation='nearest')
        plt.show()

if __name__=="__main__":
  app = CalibrationMatrices()
  app.main()