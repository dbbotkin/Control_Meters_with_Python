import sys
import time
import visa


#print ("Available GPIB")
visa = visa.ResourceManager()
#print(visa.list_resources())
DMM8842 = visa.open_resource('GPIB0::4::INSTR' ,send_end=True, read_termination= '\r\n', write_termination='\r\n') 
DMM8842.timeout = 25000

(DMM8842.write('R7'))
print str(DMM8842.query("G4"))
f = float(DMM8842.read())
print str(f)

