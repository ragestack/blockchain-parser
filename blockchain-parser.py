'''
Blockchain parser
Copyright (c) 2015-2018 Denis Leonov <466611@gmail.com>
'''

import os
import datetime
import hashlib

def HexToInt(s):
    t = ''
    if s == '':
        r = 0
    else:
        t = '0x' + s
        r = int(t,16)
    return r
    
def reverse(input):
    L = len(input)
    if (L % 2) <> 0:
        return 'Error 32b number length!'
        print ('Error 32b number length!')
    else:
        Res = ''
        L = L // 2
        for i in range(L):
            T = input[i*2] + input[i*2+1]
            Res = T + Res
            T = ''
        return (Res);

dirA = 'd:/_blocks/' 
#dirA = sys.argv[1]
dirB = 'd:/_hash/'
#dirA = sys.argv[2]

fList = os.listdir(dirA)
fList.sort()

for i in fList:
    nameSrc = i
    nameRes = nameSrc.replace('.dat','.hash')
    resList = []
    a = 0
    t = dirA + nameSrc
    resList.append('Start ' + t + ' in ' + str(datetime.datetime.now()))
    print 'Start ' + t + ' in ' + str(datetime.datetime.now())

    f = open(t,'rb')
    tmpHex = ''
    fSize = os.path.getsize(t)
    while f.tell() != fSize:
        for j in range(4):
            b = f.read(1)
            b = b.encode('hex').upper()
            tmpHex = b + tmpHex
        #if tmpHex <> 'D9B4BEF9':
            #print 'Magic number = ' + tmpHex
        #print
        #print('Magic number = ' + tmpHex)
        tmpHex = ''
        for j in range(4):
            b = f.read(1)
            b = b.encode('hex').upper()
            tmpHex = b + tmpHex
        resList.append('Block size = ' + tmpHex)
        #print('Block size = ' + tmpHex)
        tmpHex = ''
        tmpPos3 = f.tell()
        while f.tell() != tmpPos3 + 80:
            b = f.read(1)
            b = b.encode('hex').upper()
            tmpHex = tmpHex + b
        tmpHex = tmpHex.decode('hex')
        tmpHex = hashlib.new('sha256', tmpHex).digest()
        tmpHex = hashlib.new('sha256', tmpHex).digest()
        tmpHex = tmpHex.encode('hex')
        tmpHex = tmpHex.upper()
        tmpHex = reverse(tmpHex)
        resList.append('SHA256 hash of the current block hash = ' + tmpHex)
        #print('SHA256 hash of the current block hash = ' + tmpHex)
        f.seek(tmpPos3,0)
        
        tmpHex = ''
        
        #f.seek(4,1)

        for j in range(4):
            b = f.read(1)
            b = b.encode('hex').upper()
            tmpHex = b + tmpHex
        resList.append('Version number = ' + tmpHex)
        #print('Version number = ' + tmpHex)
        tmpHex = ''
        
        for j in range(32):
            b = f.read(1)
            b = b.encode('hex').upper()
            tmpHex = b + tmpHex
        resList.append('SHA256 hash of the previous block hash = ' + tmpHex)
        #print('SHA256 hash of the previous block hash = ' + tmpHex)
        tmpHex = ''
        for j in range(32):
            b = f.read(1)
            b = b.encode('hex').upper()
            tmpHex = b + tmpHex
        resList.append('MerkleRoot hash = ' + tmpHex)
        #print('MerkleRoot hash = ' + tmpHex)
        tmpHex = ''
        for j in range(4):
            b = f.read(1)
            b = b.encode('hex').upper()
            tmpHex = b + tmpHex
        resList.append('Time stamp > ' + tmpHex)
        #print('Time stamp > ' + tmpHex)

        tmpHex = ''

        #f.seek(4,1)

        for j in range(4):
            b = f.read(1)
            b = b.encode('hex').upper()
            tmpHex = b + tmpHex
        resList.append('Difficulty = ' + tmpHex)
        #print('Difficulty = ' + tmpHex)
        tmpHex = ''

        for j in range(4):
            b = f.read(1)
            b = b.encode('hex').upper()
            tmpHex = b + tmpHex
        resList.append('Random number > ' + tmpHex)
        #print('Random number > ' + tmpHex)
        tmpHex = ''
        b = f.read(1)
        bInt = int(b.encode('hex'),16)
        c = 0
        if bInt < 253:
            c = 1
            tmpHex = b.encode('hex').upper()
        if bInt == 253: c = 3
        if bInt == 254: c = 5
        if bInt == 255: c = 9
        for j in range(1,c):
            b = f.read(1)
            b = b.encode('hex').upper()
            tmpHex = b + tmpHex
        txCount = int(tmpHex,16)
        resList.append('Transactions count = ' + str(txCount))
        #print('Transactions count = ' + str(txCount) + ', bInt = ' + str(bInt) + ' ' + tmpHex)
        resList.append('')
        tmpHex = ''
        tmpPos1 = 0
        tmpPos2 = 0
        RawTX = ''
        for k in range(txCount):
            #print
            tmpPos1 = f.tell()
            for j in range(4):
                b = f.read(1)
                b = b.encode('hex').upper()
                tmpHex = b + tmpHex
            resList.append('transactionVersionNumber = ' + tmpHex)
            RawTX = reverse(tmpHex)
            #print('transactionVersionNumber = ' + tmpHex)
            tmpHex = ''

            b = f.read(1)
            bInt = int(b.encode('hex'),16)
            Witness = False
            
            if bInt == 0:
                c = 0
                c = f.read(1)
                bInt = int(c.encode('hex'),16)
                #print 'bInt = ', str(bInt)
                c = 0
                c = f.read(1)
                bInt = int(c.encode('hex'),16)
                #print 'bInt = ', str(bInt)
                Witness = True
                resList.append('Witness activated >>')
                #print('Witness activated >>')

            c = 0
            if bInt < 253:
                c = 1
                tmpHex = hex(bInt)[2:].upper().zfill(2)
                #print tmpHex
            if bInt == 253: c = 3
            if bInt == 254: c = 5
            if bInt == 255: c = 9
            for j in range(1,c):
                b = f.read(1)
                b = b.encode('hex').upper()
                tmpHex = b + tmpHex

            RawTX = RawTX + reverse(tmpHex)
            
            inCount = int(tmpHex,16)
            resList.append('Inputs count = ' + tmpHex)
            #print('Inputs count = ' + tmpHex)
            tmpHex = ''
            for m in range(inCount):
                for j in range(32):
                    b = f.read(1)
                    b = b.encode('hex').upper()
                    tmpHex = b + tmpHex
                resList.append('TX from hash = ' + tmpHex)

                RawTX = RawTX + reverse(tmpHex)

                #print('TX from hash = ' + tmpHex)
                tmpHex = ''
                for j in range(4):
                    b = f.read(1)
                    b = b.encode('hex').upper()
                    tmpHex = b + tmpHex
                resList.append('N output = ' + tmpHex)

                RawTX = RawTX + reverse(tmpHex)
                
                #print('N output = ' + tmpHex)
                tmpHex = ''

                b = f.read(1)
                bInt = int(b.encode('hex'),16)
                c = 0
                if bInt < 253:
                    c = 1
                    tmpHex = b.encode('hex').upper()
                if bInt == 253: c = 3
                if bInt == 254: c = 5
                if bInt == 255: c = 9
                for j in range(1,c):
                    b = f.read(1)
                    b = b.encode('hex').upper()
                    tmpHex = b + tmpHex
                    
                scriptLength = int(tmpHex,16)

                RawTX = RawTX + reverse(tmpHex)

                tmpHex = ''
                for j in range(scriptLength):
                    b = f.read(1)
                    b = b.encode('hex').upper()
                    tmpHex = tmpHex + b

                resList.append('Input script = ' + tmpHex)

                RawTX = RawTX + tmpHex

                #print('Input script length = ' + str(scriptLength))
                tmpHex = ''

                for j in range(4):
                    b = f.read(1)
                    b = b.encode('hex').upper()
                    tmpHex = tmpHex + b
                resList.append('sequenceNumber = ' + tmpHex)

                RawTX = RawTX + tmpHex
                
                #print('sequenceNumber = ' + tmpHex)
                tmpHex = ''

            b = f.read(1)
            bInt = int(b.encode('hex'),16)
            c = 0
            if bInt < 253:
                c = 1
                tmpHex = b.encode('hex').upper()
            if bInt == 253: c = 3
            if bInt == 254: c = 5
            if bInt == 255: c = 9
            for j in range(1,c):
                b = f.read(1)
                b = b.encode('hex').upper()
                tmpHex = b + tmpHex
            outputCount = int(tmpHex,16)
            resList.append('Outputs count = ' + str(outputCount))

            RawTX = RawTX + reverse(tmpHex)
            
            #print('Outputs count = ' + str(outputCount))
            tmpHex = ''

            for m in range(outputCount):
                for j in range(8):
                    b = f.read(1)
                    b = b.encode('hex').upper()
                    tmpHex = b + tmpHex
                Value = tmpHex

                RawTX = RawTX + reverse(tmpHex)
                
                #print('Value = ' + Value)
                tmpHex = ''
                b = f.read(1)
                bInt = int(b.encode('hex'),16)
                c = 0
                if bInt < 253:
                    c = 1
                    tmpHex = b.encode('hex').upper()
                if bInt == 253: c = 3
                if bInt == 254: c = 5
                if bInt == 255: c = 9
                for j in range(1,c):
                    b = f.read(1)
                    b = b.encode('hex').upper()
                    tmpHex = b + tmpHex
                scriptLength = int(tmpHex,16)

                RawTX = RawTX + reverse(tmpHex)
                
                #print('scriptLength = ' + str(scriptLength))
                
                tmpHex = ''
                #print f.tell(), scriptLength
                    
                for j in range(scriptLength):
                    b = f.read(1)
                    b = b.encode('hex').upper()
                    tmpHex = tmpHex + b
                resList.append('Value = ' + Value)
                resList.append('Output script = ' + tmpHex)

                RawTX = RawTX + tmpHex
                
                #print('Output script = ' + tmpHex)
                tmpHex = ''

            if Witness == True:
                for m in range(inCount):
                    tmpHex = ''
                    b = f.read(1)
                    bInt = int(b.encode('hex'),16)
                    c = 0
                    if bInt < 253:
                        c = 1
                        tmpHex = b.encode('hex').upper()
                    if bInt == 253: c = 3
                    if bInt == 254: c = 5
                    if bInt == 255: c = 9
                    for j in range(1,c):
                        b = f.read(1)
                        b = b.encode('hex').upper()
                        tmpHex = b + tmpHex
                    WitnessLength = int(tmpHex,16)
                    tmpHex = ''
                    for j in range(WitnessLength):
                        tmpHex = ''
                        b = f.read(1)
                        bInt = int(b.encode('hex'),16)
                        c = 0
                        if bInt < 253:
                            c = 1
                            tmpHex = b.encode('hex').upper()
                        if bInt == 253: c = 3
                        if bInt == 254: c = 5
                        if bInt == 255: c = 9
                        for j in range(1,c):
                            b = f.read(1)
                            b = b.encode('hex').upper()
                            tmpHex = b + tmpHex
                        WitnessItemLength = int(tmpHex,16)
                        tmpHex = ''
                        for p in range(WitnessItemLength):
                            b = f.read(1)
                            b = b.encode('hex').upper()
                            tmpHex = b + tmpHex
                        resList.append('Witness ' + str(m) + ' ' + str(j) + ' ' + str(WitnessItemLength) + ' ' + tmpHex)
                        #print('Witness ' + str(m) + ' ' + str(j) + ' ' + str(WitnessItemLength) + ' ' + tmpHex)
                        tmpHex = ''

            Witness = False
            for j in range(4):
                b = f.read(1)
                b = b.encode('hex').upper()
                tmpHex = b + tmpHex
            resList.append('Lock time = ' + tmpHex)

            RawTX = RawTX + reverse(tmpHex)
            
            #print('Lock time = ' + tmpHex)
            
            tmpHex = ''

            tmpHex = RawTX
            tmpHex = tmpHex.decode('hex')
            tmpHex = hashlib.new('sha256', tmpHex).digest()
            tmpHex = hashlib.new('sha256', tmpHex).digest()
            tmpHex = tmpHex.encode('hex')
            tmpHex = tmpHex.upper()
            tmpHex = reverse(tmpHex)
            
            resList.append('TX hash = ' + tmpHex)

            tmpHex = ''
            resList.append('')
            RawTX = ''

        a += 1

    f.close()
    f = open(dirB + nameRes,'w')
    for j in resList:
        f.write(j + '\n')
    f.close()

print datetime.datetime.now()
nameSrc = ''
nameRes = ''
dirA= ''
dirB = ''
tmpC = ''
resList = []
fList = []

