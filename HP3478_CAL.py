import sys
import time
import visa
visa = visa.ResourceManager()
#print(visa.list_resources())

HP3458 = visa.open_resource('GPIB0::22::INSTR',send_end=True, read_termination= None, write_termination=None)
HP3458.write("PRESET NORM;OFORMAT ASCII;INBUF ON;TARM AUTO;TRIG AUTO;NPLC 10;MFORMAT 1;MEM OFF;NDIG 8;END ON")
print ''
HP3458.timeout = 25000
HP3458.clear()
HP3458.write('QFORMAT ALPHA')
print (HP3458.query('END ON;ID?'))[:8]
HP3458.write('FUNC 1') # DCV
HP3458.write('NPLC 100; NDIG 8') 


HP3245 = visa.open_resource('GPIB0::9::INSTR',send_end=True, read_termination= None, write_termination=None)
HP3245.write("MEM OFF;END ON")
print ''
HP3245.clear()
HP3245.timeout = 25000

HP3245.write('OFORMAT ASCII')
HP3245.write('RESET')
HP3245.write('INBUF ON')
HP3245.write('OUTBUF ON')
HP3245.write('APPLY DCV 10')

print (HP3245.query('END ON;IDN?'))
HP3245.write('USE 0')

DMM3478 = visa.open_resource('GPIB0::1::INSTR',send_end=True, read_termination= '\r\n', write_termination='\r\n')
DMM3478.timeout = 25000

myChoice = raw_input("Press 'V' to verify or Press 'C' to calibrate:  ")
if myChoice ==  'V':
#calStatus = DMM3478.query("G4")
#if calStatus == '1000':
    VerifyVolts = [0.0,-0.03,0.03,-0.660,0.660,-1.970,1.970,3,5,10]
    
    for x in range(0, 10):
        vv =  VerifyVolts[x]
        HP3245.write('APPLY DCV ' + str(vv))
        time.sleep(10)
        f = float(DMM3478.read())
        v = HP3458.query('')
        prt = (str(x) + ', ' + str(vv) + ', ' + str(f) + ', ' + str(v)[0:16])
        print prt
        time.sleep(1)

elif myChoice == 'C':
#elif calStatus == '1001':
    #raw_input( "Press CAL button ON")
    
    RangeVolts = ('R-2','R-1','R0','R1','R2')
    RangeFmt = [1000,1000,1,1,1]
    CalVolts = [0.03,0.3,3.0,10.0,100.0]
    

#    DMM3478.write('C1')
    for x in range(0, 4):
        txt = "{:.6f}"
        rv = RangeVolts[x]
        DMM3478.write(rv)
        HP3245.write('APPLY DCV 0')
        v = float(HP3458.query(''))
        time.sleep(10)        
        DMM3478.write("D2+000000")
        time.sleep(5)
        DMM3478.write('C')
        time.sleep(5)
        
        cv =  CalVolts[x]
        HP3245.write('APPLY DCV ' + str(cv))
        time.sleep(5)
        v = float(HP3458.query(''))*RangeFmt[x]
        DMM3478.write('D2+' + txt.format(v))
        
        time.sleep(5)
        DMM3478.write('C')
        time.sleep(5)
        
        prt = (str(x) + ', ' + str(cv) + ', ' + str(v)[0:16])
        print prt
        time.sleep(10)

    print ( "Turn CAL button OFF")

else:
    sys.exit(0)






