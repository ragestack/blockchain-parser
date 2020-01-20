# -*- coding: utf-8 -*-
#
# Blockchain parser
# Copyright (c) 2015-2020 Denis Leonov <466611@gmail.com>
#

import os
import datetime
import hashlib

def reverse(input):
    L = len(input)
    if (L % 2) != 0:
        return None
    else:
        Res = ''
        L = L // 2
        for i in range(L):
            T = input[i*2] + input[i*2+1]
            Res = T + Res
            T = ''
        return (Res);

def merkle_root(lst): # https://gist.github.com/anonymous/7eb080a67398f648c1709e41890f8c44
    sha256d = lambda x: hashlib.sha256(hashlib.sha256(x).digest()).digest()
    hash_pair = lambda x, y: sha256d(x[::-1] + y[::-1])[::-1]
    if len(lst) == 1: return lst[0]
    if len(lst) % 2 == 1:
        lst.append(lst[-1])
    return merkle_root([hash_pair(x,y) for x, y in zip(*[iter(lst)]*2)])

dirA = './_blocks/' # Directory where blk*.dat files are stored
#dirA = sys.argv[1]
dirB = './_result/' # Directory where to save parsing results
#dirA = sys.argv[2]

fList = os.listdir(dirA)
fList = [x for x in fList if (x.endswith('.dat') and x.startswith('blk'))]
fList.sort()

for i in fList:
    nameSrc = i
    nameRes = nameSrc.replace('.dat','.txt')
    resList = []
    a = 0
    t = dirA + nameSrc
    resList.append('Start ' + t + ' in ' + str(datetime.datetime.now()))
    print ('Start ' + t + ' in ' + str(datetime.datetime.now()))
    f = open(t,'rb')
    tmpHex = ''
    fSize = os.path.getsize(t)
    while f.tell() != fSize:
        for j in range(4):
            b = f.read(1)
            b = b.hex().upper()
            tmpHex = b + tmpHex
        tmpHex = ''
        for j in range(4):
            b = f.read(1)
            b = b.hex().upper()
            tmpHex = b + tmpHex
        resList.append('Block size = ' + tmpHex)
        tmpHex = ''
        tmpPos3 = f.tell()
        while f.tell() != tmpPos3 + 80:
            b = f.read(1)
            b = b.hex().upper()
            tmpHex = tmpHex + b
        tmpHex = bytes.fromhex(tmpHex)
        tmpHex = hashlib.new('sha256', tmpHex).digest()
        tmpHex = hashlib.new('sha256', tmpHex).digest()
        tmpHex = tmpHex.hex()
        tmpHex = tmpHex.upper()
        tmpHex = reverse(tmpHex)
        resList.append('SHA256 hash of the current block hash = ' + tmpHex)
        f.seek(tmpPos3,0)
        tmpHex = ''
        for j in range(4):
            b = f.read(1)
            b = b.hex().upper()
            tmpHex = b + tmpHex
        resList.append('Version number = ' + tmpHex)
        tmpHex = ''
        for j in range(32):
            b = f.read(1)
            b = b.hex().upper()
            tmpHex = b + tmpHex
        resList.append('SHA256 hash of the previous block hash = ' + tmpHex)
        tmpHex = ''
        for j in range(32):
            b = f.read(1)
            b = b.hex().upper()
            tmpHex = b + tmpHex
        resList.append('MerkleRoot hash = ' + tmpHex)
        MerkleRoot = tmpHex
        tmpHex = ''
        for j in range(4):
            b = f.read(1)
            b = b.hex().upper()
            tmpHex = b + tmpHex
        resList.append('Time stamp > ' + tmpHex)
        tmpHex = ''
        for j in range(4):
            b = f.read(1)
            b = b.hex().upper()
            tmpHex = b + tmpHex
        resList.append('Difficulty = ' + tmpHex)
        tmpHex = ''
        for j in range(4):
            b = f.read(1)
            b = b.hex().upper()
            tmpHex = b + tmpHex
        resList.append('Random number > ' + tmpHex)
        tmpHex = ''
        b = f.read(1)
        bInt = int(b.hex(),16)
        c = 0
        if bInt < 253:
            c = 1
            tmpHex = b.hex().upper()
        if bInt == 253: c = 3
        if bInt == 254: c = 5
        if bInt == 255: c = 9
        for j in range(1,c):
            b = f.read(1)
            b = b.hex().upper()
            tmpHex = b + tmpHex
        txCount = int(tmpHex,16)
        resList.append('Transactions count = ' + str(txCount))
        resList.append('')
        tmpHex = ''
        tmpPos1 = 0
        tmpPos2 = 0
        RawTX = ''
        tx_hashes = []
        for k in range(txCount):
            tmpPos1 = f.tell()
            for j in range(4):
                b = f.read(1)
                b = b.hex().upper()
                tmpHex = b + tmpHex
            resList.append('transactionVersionNumber = ' + tmpHex)
            RawTX = reverse(tmpHex)
            tmpHex = ''
            b = f.read(1)
            tmpB = b.hex().upper()
            bInt = int(b.hex(),16)
            Witness = False
            if bInt == 0:
                tmpB = ''
                c = 0
                c = f.read(1)
                bInt = int(c.hex(),16)
                c = 0
                c = f.read(1)
                bInt = int(c.hex(),16)
                tmpB = c.hex().upper()
                Witness = True
                resList.append('Witness activated >>')
            c = 0
            if bInt < 253:
                c = 1
                tmpHex = hex(bInt)[2:].upper().zfill(2)
                tmpB = ''
            if bInt == 253: c = 3
            if bInt == 254: c = 5
            if bInt == 255: c = 9
            for j in range(1,c):
                b = f.read(1)
                b = b.hex().upper()
                tmpHex = b + tmpHex
            inCount = int(tmpHex,16)
            resList.append('Inputs count = ' + tmpHex)
            tmpHex = tmpHex + tmpB
            RawTX = RawTX + reverse(tmpHex)
            tmpHex = ''
            for m in range(inCount):
                for j in range(32):
                    b = f.read(1)
                    b = b.hex().upper()
                    tmpHex = b + tmpHex
                resList.append('TX from hash = ' + tmpHex)
                RawTX = RawTX + reverse(tmpHex)
                tmpHex = ''
                for j in range(4):
                    b = f.read(1)
                    b = b.hex().upper()
                    tmpHex = b + tmpHex
                resList.append('N output = ' + tmpHex)
                RawTX = RawTX + reverse(tmpHex)
                tmpHex = ''
                b = f.read(1)
                tmpB = b.hex().upper()
                bInt = int(b.hex(),16)
                c = 0
                if bInt < 253:
                    c = 1
                    tmpHex = b.hex().upper()
                    tmpB = ''
                if bInt == 253: c = 3
                if bInt == 254: c = 5
                if bInt == 255: c = 9
                for j in range(1,c):
                    b = f.read(1)
                    b = b.hex().upper()
                    tmpHex = b + tmpHex
                scriptLength = int(tmpHex,16)
                tmpHex = tmpHex + tmpB
                RawTX = RawTX + reverse(tmpHex)
                tmpHex = ''
                for j in range(scriptLength):
                    b = f.read(1)
                    b = b.hex().upper()
                    tmpHex = tmpHex + b
                resList.append('Input script = ' + tmpHex)
                RawTX = RawTX + tmpHex
                tmpHex = ''
                for j in range(4):
                    b = f.read(1)
                    b = b.hex().upper()
                    tmpHex = tmpHex + b
                resList.append('sequenceNumber = ' + tmpHex)
                RawTX = RawTX + tmpHex
                tmpHex = ''
            b = f.read(1)
            tmpB = b.hex().upper()
            bInt = int(b.hex(),16)
            c = 0
            if bInt < 253:
                c = 1
                tmpHex = b.hex().upper()
                tmpB = ''
            if bInt == 253: c = 3
            if bInt == 254: c = 5
            if bInt == 255: c = 9
            for j in range(1,c):
                b = f.read(1)
                b = b.hex().upper()
                tmpHex = b + tmpHex
            outputCount = int(tmpHex,16)
            tmpHex = tmpHex + tmpB
            resList.append('Outputs count = ' + str(outputCount))
            RawTX = RawTX + reverse(tmpHex)
            tmpHex = ''
            for m in range(outputCount):
                for j in range(8):
                    b = f.read(1)
                    b = b.hex().upper()
                    tmpHex = b + tmpHex
                Value = tmpHex
                RawTX = RawTX + reverse(tmpHex)
                tmpHex = ''
                b = f.read(1)
                tmpB = b.hex().upper()
                bInt = int(b.hex(),16)
                c = 0
                if bInt < 253:
                    c = 1
                    tmpHex = b.hex().upper()
                    tmpB = ''
                if bInt == 253: c = 3
                if bInt == 254: c = 5
                if bInt == 255: c = 9
                for j in range(1,c):
                    b = f.read(1)
                    b = b.hex().upper()
                    tmpHex = b + tmpHex
                scriptLength = int(tmpHex,16)
                tmpHex = tmpHex + tmpB
                RawTX = RawTX + reverse(tmpHex)
                tmpHex = ''
                for j in range(scriptLength):
                    b = f.read(1)
                    b = b.hex().upper()
                    tmpHex = tmpHex + b
                resList.append('Value = ' + Value)
                resList.append('Output script = ' + tmpHex)
                RawTX = RawTX + tmpHex
                tmpHex = ''
            if Witness == True:
                for m in range(inCount):
                    tmpHex = ''
                    b = f.read(1)
                    bInt = int(b.hex(),16)
                    c = 0
                    if bInt < 253:
                        c = 1
                        tmpHex = b.hex().upper()
                    if bInt == 253: c = 3
                    if bInt == 254: c = 5
                    if bInt == 255: c = 9
                    for j in range(1,c):
                        b = f.read(1)
                        b = b.hex().upper()
                        tmpHex = b + tmpHex
                    WitnessLength = int(tmpHex,16)
                    tmpHex = ''
                    for j in range(WitnessLength):
                        tmpHex = ''
                        b = f.read(1)
                        bInt = int(b.hex(),16)
                        c = 0
                        if bInt < 253:
                            c = 1
                            tmpHex = b.hex().upper()
                        if bInt == 253: c = 3
                        if bInt == 254: c = 5
                        if bInt == 255: c = 9
                        for j in range(1,c):
                            b = f.read(1)
                            b = b.hex().upper()
                            tmpHex = b + tmpHex
                        WitnessItemLength = int(tmpHex,16)
                        tmpHex = ''
                        for p in range(WitnessItemLength):
                            b = f.read(1)
                            b = b.hex().upper()
                            tmpHex = b + tmpHex
                        resList.append('Witness ' + str(m) + ' ' + str(j) + ' ' + str(WitnessItemLength) + ' ' + tmpHex)
                        tmpHex = ''
            Witness = False
            for j in range(4):
                b = f.read(1)
                b = b.hex().upper()
                tmpHex = b + tmpHex
            resList.append('Lock time = ' + tmpHex)
            RawTX = RawTX + reverse(tmpHex)
            tmpHex = ''
            tmpHex = RawTX
            tmpHex = bytes.fromhex(tmpHex)
            tmpHex = hashlib.new('sha256', tmpHex).digest()
            tmpHex = hashlib.new('sha256', tmpHex).digest()
            tmpHex = tmpHex.hex()
            tmpHex = tmpHex.upper()
            tmpHex = reverse(tmpHex)
            resList.append('TX hash = ' + tmpHex)
            tx_hashes.append(tmpHex)
            tmpHex = ''
            resList.append('')
            RawTX = ''
        a += 1
        tx_hashes = [bytes.fromhex(h) for h in tx_hashes]
        tmpHex = merkle_root(tx_hashes).hex().upper()
        if tmpHex != MerkleRoot:
            print ('Merkle roots does not match! >',MerkleRoot,tmpHex)
        tmpHex = ''
    f.close()
    f = open(dirB + nameRes,'w')
    for j in resList:
        f.write(j + '\n')
    f.close()
nameSrc = ''
nameRes = ''
dirA= ''
dirB = ''
tmpC = ''
resList = []
fList = []
