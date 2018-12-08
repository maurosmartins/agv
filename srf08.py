#import smbus tambem funciona
import smbus2
import time

class SRF:
    I2CAddr = 0
    I2CBus = 0
    Range = -1
    
    WriteRegisters = {'command': 0x00, 'max_gain': 0x01, 'range_register': 0x02}
    ReadRegisters = {'software_revision': 0x00, 'light_sensor': 0x01, 'first_echo_h': 0x02, 'first_echo_l': 0x03}
    Commands = {'range_in':0x50, 'range_cm':0x51, 'range_us':0x52}

    def __init__(self, I2CAddr, I2CBus):
        self.I2CAddr = I2CAddr
        self.I2CBus = I2CBus
        

  
    def GetRange(self):
        
        try:
            self.I2CBus.write_byte_data( self.I2CAddr, self.WriteRegisters['command'], self.Commands['range_us'] )
            time.sleep(0.07)
            NumberOfBytesToRead = 6
            #Due to error in communications the complete set of registers since 0x00 has to be read
            range = self.I2CBus.read_i2c_block_data(self.I2CAddr, self.ReadRegisters['software_revision'], NumberOfBytesToRead)
                                    
        except:
            self.Range = -1
            return -1 #error when reading from a SRF08 Sensor, in this case a negative distance is returned.

        #print( "high={0} low={1}".format(range[2], range[3]) )
        self.Range =  round( ((range[ self.ReadRegisters['first_echo_h'] ]*255) + range[ self.ReadRegisters['first_echo_l'] ] )/60, 1)
        return self.Range
    
#    def ChangeAddr(self, OldI2CAddr, NewI2CAddr):
#        
#        try:
#            ChangeAddrCommand = [0xA0, NewI2CAddr]
#            self.bus.write_i2c_block_data(OldI2CAddr, 0, ChangeAddrCommand)
#        except:
#            return False
#           
#        self.I2CAddr = NewI2CAddr
#        return True
        

if __name__ == "__main__":

        I2CBus = smbus2.SMBus(1)
        
        sonars = []
        #these are 7bits I2C addr. the 8bits addr are 0xE0 (front sensor), 0xE2 (left sensor) and 0xE4 (right sensor)
        sonars.append( SRF(0x70, I2CBus) ) #front
        sonars.append( SRF(0x71, I2CBus) ) #left
        sonars.append( SRF(0x72, I2CBus) ) #right

        while True:
        
            for sonar in sonars:#{
                sonar.GetRange()
                #print( sonar.Range )
             #}
             
            print( "L {0:04.1f} C {1:04.1f} R {2:04.1f} ".format(sonars[1].Range, sonars[0].Range, sonars[2].Range))
                
            time.sleep(1)