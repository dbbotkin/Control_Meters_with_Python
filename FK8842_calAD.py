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

DMM8842 = visa.open_resource('GPIB0::8::INSTR',send_end=True, read_termination= '\r\n', write_termination='\r\n')
DMM8842.timeout = 25000
#print str(DMM8842.query('G8'))

calStatus = DMM8842.query("G4")
if calStatus == '1000':
    VerifyAD = [0.0,-0.03,0.03,-0.660,0.660,-1.970,1.970]
    DMM8842.write('R0')
    for x in range(0, 7):
        vv =  VerifyAD[x]
        HP3245.write('APPLY DCV ' + str(vv))
        time.sleep(10)
        f = float(DMM8842.read())
        v = HP3458.query('')
        prt = (str(x) + ', ' + str(vv) + ', ' + str(f) + ', ' + str(v)[0:16])
        print prt
        time.sleep(1)


elif calStatus == '1001':
    CalAD = [0.0,-0.03,-1.01,0.99,0.51,-0.51,-0.26,0.26,0.135,-0.135,-0.0725,0.0725 ]
    Range = ['R1','R2','R3','R8']
    CalVolts = [0.190,1.90,10.0,0.019,]


    DMM8842.write('C1')
    for x in range(0, 12):
        cv =  CalAD[x]
        HP3245.write('APPLY DCV ' + str(cv))
        time.sleep(10)
        DMM8842.write('G2')
        time.sleep(1)
        DMM8842.write('C0')
        time.sleep(20)
        v = HP3458.read()
        prt = (str(x) + ', ' + str(cv) + ', ' + str(v)[0:16])
        print prt


    print( "Now calibrating VDC")
    
    for x in range(0, 4):
        r = Range[x]
        
        DMM8842.write(r)
        HP3245.write('APPLY DCV 0.0')
        time.sleep(10)
        DMM8842.write('G2')
        time.sleep(1)
        DMM8842.write('C0')
        time.sleep(20)
        v = HP3458.read()
        prt = (str(x) + ', ' + ' 0' + ', ' + str(v)[0:16])
        print prt

        cvv = CalVolts[x]
        HP3245.write('APPLY DCV ' + str(cvv))
        time.sleep(10)
        DMM8842.write('G2')
        if x == 2:
            DMM8842.write('N10.0P2')
        time.sleep(1)
        DMM8842.write('C0')
        time.sleep(20)
        v = HP3458.read()
        prt = (str(x) + ', ' + str(cvv) + ', ' + str(v)[0:16])
        print prt
        
    raw_input( "Press CAL button OFF")

else:
    sys.exit(0)






