import sys
import time
import visa


#print ("Available GPIB")
visa = visa.ResourceManager()
#print(visa.list_resources())
DMM3478 = visa.open_resource('GPIB0::1::INSTR',send_end=True, read_termination= '\r\n', write_termination='\r\n')
DMM3478.timeout = 25000

DMM3478.write("F1N6T1Z1")
print str(DMM3478.query("*IDN"))
f = float(DMM3478.query('?'))
print str(f)

