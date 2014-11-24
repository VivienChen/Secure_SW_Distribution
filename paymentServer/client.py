"""

CODE ADAPTED FROM:

(C) Copyright 2009 Igor V. Custodio

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""


from ISO8583.ISO8583 import ISO8583
from ISO8583.ISOErrors import *
import socket
import sys
import time


# Configure the client
serverIP = "localhost" 
serverPort = 8583
numberEcho = 1
timeBetweenEcho = 5 # in seconds

bigEndian = True
#bigEndian = False

s = None
for res in socket.getaddrinfo(serverIP, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
                s = socket.socket(af, socktype, proto)
    except socket.error, msg:
        s = None
        continue
    try:
                s.connect(sa)
    except socket.error, msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print ('Could not connect :(')
    sys.exit(1)
        
        
        
for req in range(0,numberEcho):
        iso = ISO8583()
        iso.setMTI('2200')					# MTI values (Authentication request)
        iso.setBit(2,'4321123443211234') 	# Primary account number
        iso.setBit(3,'000000')  			# Processing code
        iso.setBit(4,'000000012300')		# Transaction amount ($ 123.00)
        iso.setBit(7,'1114123456')    		# Transmission date/time MMYYHHMMSS
        iso.setBit(14,'1705')       		# Expiration date YYMM
        iso.setBit(49,'840')        		# Currency American Dollars
        iso.setBit(63,' This is a sample message')
        
        if bigEndian:
                try:
                        message = iso.getNetworkISO() 
                        s.send(message)
                        print ('Sending ... %s' % message)
                        ans = s.recv(2048)
                        print ("\nInput ASCII |%s|" % ans)
                        isoAns = ISO8583()
                        isoAns.setNetworkISO(ans)
                        v1 = isoAns.getBitsAndValues()
                        for v in v1:
                                print ('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']))
                                
                        if isoAns.getMTI() == '2210':
                                print ("\tThat's great !!! The server understand my message !!!")
                        else:
                                print ("The server dosen't understand my message!")
                                        
                except InvalidIso8583, ii:
                        print (ii)
                        break   
                

                time.sleep(timeBetweenEcho)
                
        else:
                try:
                        message = iso.getNetworkISO(False) 
                        s.send(message)
                        print ('Sending ... %s' % message)
                        ans = s.recv(2048)
                        print ("\nInput ASCII |%s|" % ans)
                        isoAns = ISO8583()
                        isoAns.setNetworkISO(ans,False)
                        v1 = isoAns.getBitsAndValues()
                        for v in v1:
                                print ('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']))
                                        
                        if isoAns.getMTI() == '2110':
                                print ("The server accepted the message !!!")
                        else:
                                print ("The server declined the message!")
                        
                except InvalidIso8583, ii:
                        print (ii)
                        break   
                
                time.sleep(timeBetweenEcho)

                
                
print ('Closing...')            
s.close()
