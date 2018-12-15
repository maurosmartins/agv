import serial

class CrawlerComm:

    fVelocity = 0.0
    fPhi = 0.0
    ComPort = ''
    ser = []


    def __init__(self, ComPort, fVelocity, fPhi):
        self.ComPort = ComPort
        self.fVelocity = fVelocity
        self.fPhi = fPhi
        self.ser = serial.Serial(ComPort)

    def Velocity(self, fVelocity):
        self.fVelocity = fVelocity
        self.Update()

    def Phi(self, fPhi):
        self.fPhi = fPhi
        self.Update()

    def Update(self):
        s = str(self.fVelocity) + ';' + str(self.fPhi) + '\r'
        self.ser.write(bytes(s,'UTF-8'))
        #print(s)

    def CloseConnection(self):
        self.ser.close()



if __name__ == "__main__":
    crawler = CrawlerComm('/dev/ttyACM0', 0.0, 0.0)

    crawler.Velocity(0.0)
    crawler.Phi(0.0)


