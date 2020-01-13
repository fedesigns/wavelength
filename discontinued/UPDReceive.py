import socket
import DateTime
import time
import select
import struct
import bitstring
import liblo as lo
import numpy as np

#preprocessing EEG data
def _getDecDigit(digit):
    digits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    for x in range(len(digits)):
        if digit.lower() == digits[x]:
            return(x)
        
def hexToDec(hexNum):
    decNum = 0
    power = 0
    
    for digit in range(len(hexNum), 0, -1):
        try:
            decNum = decNum + 16 ** power * _getDecDigit(hexNum[digit-1])
            power += 1
        except:
            return
    return(int(decNum))



UDP_IP = "100.88.136.244" #UDP IP adress
UDP_PORT = 5000 #UDP port for osc stream
sock = socket.socket(socket.AF_INET,  # Internet
                    socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))
# stocker = []
# counter = 0

outputAddress = lo.Address("127.0.0.1", 5000)


eegdata = np.zeros((5,12))

timestamps = np.zeros(12)

while True:
    data, addr = sock.recvfrom(1024)
    print(data)
    data = str(data).split(",")
    newData=data[1]
    newData.decode('utf-8')
    print(newData)
"""
    newData = newData[1].split("x")
    newData = newData[3:]
    outData = []
    print(newData)
    for i in newData:
        outData += [hexToDec(i[:-1])]
    newerOut = []
    print(outData)
    
    for i in outData:
        if type(i) == int and i > 0:
            newerOut += [i]
    print(newerOut)
    #if "/eeg" in str(data):
    #handle = int(newData[0])+int(newData[1])
    #print(handle)
    """
"""
    for i in range(len(newData)):
        newData[i] = int(newData[i])
        """
"""
    aa = bitstring.Bits(bytes=newerOut[0:])
    print(newData[1:])
    pattern = "uint:16,uint:12,uint:12,uint:12,uint:12,uint:12,uint:12, \
           uint:12,uint:12,uint:12,uint:12,uint:12,uint:12"           
    res = aa.unpack(pattern)  #unpacking ASCII message
    timestamp = res[0]
    newData = res[1:]
    newData = 0.40293 * np.array(newData)
  
    print(timestamp," ", newData)
    """
      #  print(handle)
      
      #  index = int(3)#(handle - 32) / 3)
      #  eegdata[index] = data

       # timestamps[index] = timestamp
"""
        samples are received in this order : 44, 41, 38, 32, 35
        wait until we get 35 and call the data
        """
        #if handle == 35:
"""
            for ind in range(12):
                message = eegdata[0][ind], eegdata[1][ind],
                            eegdata[2][ind], eegdata[3][ind],
                            eegdata[4][ind])
                eegMessage = lo.Message('/muse/eeg', eegdata[0][ind], eegdata[1][ind],
                            eegdata[2][ind], eegdata[3][ind],
                            eegdata[4][ind])
                lo.send(outputAddress, eegMessage)
                '''

        """
"""
                newData = str(data).split(",")
                newData = newData[1].split("x")
                print(newData[1])
                newData = newData[1:]
                outData = []
                print(newData)

                #unpacked = struct.unpack('>64ffffff',newData)

                for i in newData:
                    outData += [hexToDec(i[:-1])]
                newerOut = []
                print(outData)
                
                for i in outData:
                    if type(i) == int and i > 0:
                        newerOut += [i]

                if len(newerOut) == 0:
                    continue
                print('newerOut')
                print(newerOut)

                stocker += [sum(newerOut)/len(newerOut)]
                counter += 1
                print(stocker)
                print(counter)

                if counter == 2:
                    s = sum(stocker)/len(stocker)
                    if s == sum(newerOut)/len(newerOut):
                        return(1)
                    else:
                        return(0)
                       

    if __name__ == "__main__":
        egg_capture()"""