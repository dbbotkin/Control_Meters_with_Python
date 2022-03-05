import sys
import time
import visa


visa = visa.ResourceManager()
#print(visa.list_resources())
FLK8842 = visa.open_resource('GPIB0::4::INSTR',send_end=True, read_termination= '\r\n', write_termination='\r\n')
FLK8842.timeout = 25000


print str(FLK8842.query('G8'))

for x in range(1, 11):
    v = float (FLK8842.read())

    prt = (str(x) + ', ' + str(v))
    print prt

#FLK8842.read()
#FLK8842.query('?'))
#FLK8842.write("F0R0S3P10X")

'''
DAQ6510 = visa.open_resource('TCPIP0::192.168.7.110::5025::SOCKET')
DAQ6510.timeout = 1000
DAQ6510.write_termination = '\n'
DAQ6510.read_termination = '\n'

print (DAQ6510.query("*IDN?"))


DAQ6510.write(':DISPlay:LIGHt:STATe ON100')
time.sleep(1) # 1 sec
DAQ6510.write(':DISPlay:LIGHt:STATe ON25')
time.sleep(1) # 1 sec
DAQ6510.write(':DISPlay:LIGHt:STATe ON75')

DAQ6510.write(':FORMat:ASCii:PRECision 10')

(DAQ6510.write(':TRAC:CLE "volts"'))
label = (DAQ6510.query(':ROUT:LAB? (@111)'))
print label

DAQ6510.write(':SENS:FUNC "VOLT:DC", (@111)')
DAQ6510.write(':ROUT:CLOS (@111)')

for x in range(1, 10):

    DAQ6510.write('ROUTe:WRITe ' + str(255) +  ', (@121)')    
    time.sleep(5)
    for x in range(255, -1, -1):
        DAQ6510.write('ROUTe:WRITe ' + str(x) +  ', (@121)')    
        time.sleep(.1)

    DAQ6510.write('ROUTe:WRITe ' + str(0) +  ', (@121)')    
    time.sleep(5)
    
    for x in range(0, 255):
    #    DAQ6510.write(':Read? "volts"')
        DAQ6510.write('ROUTe:WRITe ' + str(x) +  ', (@121)')
        time.sleep(.1)
        
#    DAQ6510.write('ROUTe:WRITe ' + str(256) +  ', (@121)')    
#    time.sleep(5)

   
print (DAQ6510.query(':READ?'))
'''
