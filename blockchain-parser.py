# -*- coding: utf-8 -*-
#
# Blockchain parser
# Copyright (c) 2015-2021 Denis Leonov <466611@gmail.com>
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

def read_bytes(file,n,byte_order = 'L'):
    data = file.read(n)
    if byte_order == 'L':
        data = data[::-1]
    data = data.hex().upper()
    return data

def read_varint(file):
    b = file.read(1)
    bInt = int(b.hex(),16)
    c = 0
    data = ''
    if bInt < 253:
        c = 1
        data = b.hex().upper()
    if bInt == 253: c = 3
    if bInt == 254: c = 5
    if bInt == 255: c = 9
    for j in range(1,c):
        b = file.read(1)
        b = b.hex().upper()
        data = b + data
    return data

dirA = './blocks/' # Directory where blk*.dat files are stored
#dirA = sys.argv[1]
dirB = './result/' # Directory where to save parsing results
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
        tmpHex = read_bytes(f,4)
        resList.append('Magic number = ' + tmpHex)
        tmpHex = read_bytes(f,4)
        resList.append('Block size = ' + tmpHex)
        tmpPos3 = f.tell()
        tmpHex = read_bytes(f,80,'B')
        tmpHex = bytes.fromhex(tmpHex)
        tmpHex = hashlib.new('sha256', tmpHex).digest()
        tmpHex = hashlib.new('sha256', tmpHex).digest()
        tmpHex = tmpHex[::-1]        
        tmpHex = tmpHex.hex().upper()
        resList.append('SHA256 hash of the current block hash = ' + tmpHex)
        f.seek(tmpPos3,0)
        tmpHex = read_bytes(f,4)
        resList.append('Version number = ' + tmpHex)
        tmpHex = read_bytes(f,32)
        resList.append('SHA256 hash of the previous block hash = ' + tmpHex)
        tmpHex = read_bytes(f,32)
        resList.append('MerkleRoot hash = ' + tmpHex)
        MerkleRoot = tmpHex
        tmpHex = read_bytes(f,4)
        resList.append('Time stamp = ' + tmpHex)
        tmpHex = read_bytes(f,4)
        resList.append('Difficulty = ' + tmpHex)
        tmpHex = read_bytes(f,4)
        resList.append('Random number = ' + tmpHex)
        tmpHex = read_varint(f)
        txCount = int(tmpHex,16)
        resList.append('Transactions count = ' + str(txCount))
        resList.append('')
        tmpHex = ''; RawTX = ''; tx_hashes = []
        for k in range(txCount):
            tmpHex = read_bytes(f,4)
            resList.append('TX version number = ' + tmpHex)
            RawTX = reverse(tmpHex)
            tmpHex = ''
            Witness = False
            b = f.read(1)
            tmpB = b.hex().upper()
            bInt = int(b.hex(),16)
            if bInt == 0:
                tmpB = ''
                f.seek(1,1)
                c = 0
                c = f.read(1)
                bInt = int(c.hex(),16)
                tmpB = c.hex().upper()
                Witness = True
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
            for m in range(inCount):
                tmpHex = read_bytes(f,32)
                resList.append('TX from hash = ' + tmpHex)
                RawTX = RawTX + reverse(tmpHex)
                tmpHex = read_bytes(f,4)                
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
                tmpHex = read_bytes(f,scriptLength,'B')
                resList.append('Input script = ' + tmpHex)
                RawTX = RawTX + tmpHex
                tmpHex = read_bytes(f,4,'B')
                resList.append('Sequence number = ' + tmpHex)
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
            for m in range(outputCount):
                tmpHex = read_bytes(f,8)
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
                tmpHex = read_bytes(f,scriptLength,'B')
                resList.append('Value = ' + Value)
                resList.append('Output script = ' + tmpHex)
                RawTX = RawTX + tmpHex
                tmpHex = ''
            if Witness == True:
                for m in range(inCount):
                    tmpHex = read_varint(f)
                    WitnessLength = int(tmpHex,16)
                    for j in range(WitnessLength):
                        tmpHex = read_varint(f)
                        WitnessItemLength = int(tmpHex,16)
                        tmpHex = read_bytes(f,WitnessItemLength)
                        resList.append('Witness ' + str(m) + ' ' + str(j) + ' ' + str(WitnessItemLength) + ' ' + tmpHex)
                        tmpHex = ''
            Witness = False
            tmpHex = read_bytes(f,4)
            resList.append('Lock time = ' + tmpHex)
            RawTX = RawTX + reverse(tmpHex)
            tmpHex = RawTX
            tmpHex = bytes.fromhex(tmpHex)
            tmpHex = hashlib.new('sha256', tmpHex).digest()
            tmpHex = hashlib.new('sha256', tmpHex).digest()
            tmpHex = tmpHex[::-1]
            tmpHex = tmpHex.hex().upper()
            resList.append('TX hash = ' + tmpHex)
            tx_hashes.append(tmpHex)
            resList.append(''); tmpHex = ''; RawTX = ''
        a += 1
        tx_hashes = [bytes.fromhex(h) for h in tx_hashes]
        tmpHex = merkle_root(tx_hashes).hex().upper()
        if tmpHex != MerkleRoot:
            print ('Merkle roots does not match! >',MerkleRoot,tmpHex)
    f.close()
    f = open(dirB + nameRes,'w')
    for j in resList:
        f.write(j + '\n')
    f.close()
