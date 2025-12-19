#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
blockchain-parser.py

Author: Denis Leonov
Project: Blockchain Parser (Blockchain Scalpel)
Repository: https://github.com/ragestack/blockchain-parser
Version: 2.0.0

License:
  Blockchain Scalpel License (Source-Available, Non-Commercial)
  Free for non-commercial use with attribution.
  Commercial use and any SaaS/cloud/hosted use require a paid license.

Commercial licensing contact: 466611@gmail.com
Other author's contact info: https://aaris.ru/DL

Limited warranty:
  A limited compatibility warranty related to block format changes
  is provided. See LICENSE and WARRANTY.md for details.
"""

__version__ = "2.0.0"
__author__ = "Denis Leonov"

# SPDX-License-Identifier: LicenseRef-Blockchain-Scalpel

import os, io, sys
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

def merkle_root(h):
    d = lambda b:hashlib.sha256(hashlib.sha256(b).digest()).digest()
    rev = lambda x:x[::-1]
    h = list(map(rev,h))
    while len(h) > 1:
        if len(h)&1:h += h[-1:]
        h = [d(h[i]+h[i+1]) for i in range(0,len(h),2)]
    return rev(h[0])

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

def print_help(script_name):
    print(
        f"Usage:\n"
        f"  python {script_name} <dirA> <dirB>\n\n"
        f"Arguments:\n"
        f"  dirA   Directory where blk*.dat files are stored (must exist)\n"
        f"  dirB   Output directory for parsing results (must already exist)\n"
    )

def main():
    script_name = os.path.basename(sys.argv[0])

    if len(sys.argv) == 2 and sys.argv[1] in ("-h", "--help"):
        print_help(script_name)
        sys.exit(0)

    if len(sys.argv) != 3:
        print("Error: exactly 2 arguments are required.\n", file=sys.stderr)
        print_help(script_name)
        sys.exit(1)
            
    dirA = os.path.abspath(os.path.expanduser(sys.argv[1]))
    dirB = os.path.abspath(os.path.expanduser(sys.argv[2]))

    if not os.path.isdir(dirA):
        print(f"Error: input directory does not exist or is not a directory:\n  {dirA}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(dirB):
        print(
            f"Error: output directory does not exist (create it first):\n  {dirB}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(dirB):
        print(f"Error: output path exists but is not a directory:\n  {dirB}", file=sys.stderr)
        sys.exit(1)

    if not os.access(dirB, os.W_OK):
        print(f"Error: output directory is not writable:\n  {dirB}", file=sys.stderr)
        sys.exit(1)

    kN = os.path.join(dirA, 'xor.dat')

    k_ = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    lk_ = len(k_)
    if os.path.isfile(kN):
        with open(kN, 'rb') as kF:
            k_ = kF.read(lk_)

    fList = [x for x in os.listdir(dirA) if x.endswith('.dat') and x.startswith('blk')]
    rList = [x for x in os.listdir(dirB) if x.endswith('.txt') and x.startswith('blk')]

    rNames = {os.path.splitext(x)[0] for x in rList}

    fList = [x for x in fList if os.path.splitext(x)[0] not in rNames]
    fList.sort()

    for i in fList:
        nameSrc = i
        nameRes = nameSrc.replace('.dat','.txt')
        resList = []
        a = 0
        t = os.path.join(dirA, nameSrc)
        resList.append('Start ' + t + ' in ' + str(datetime.datetime.now()))
        print ('Start ' + t + ' in ' + str(datetime.datetime.now()))
        with open(t,'rb') as f0:
            b_ = bytearray(f0.read())
        if any(k_):
            for ii in range(len(b_)):
                b_[ii] ^= k_[ii%lk_]
        f = io.BytesIO(b_)
        tmpHex = ''
        fSize = os.path.getsize(t)
        while f.tell() != fSize:
            tmpErr = 0
            while tmpHex != 'D9B4BEF9': # it is for to skip zeroes in some blk files
                tmpHex = read_bytes(f,4)
                tmpErr += 1
                if tmpErr > 2:
                    raise ValueError(f"Invalid data: magic number missing — possible truncated {i} file")
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
        f = open(os.path.join(dirB, nameRes),'w')
        for j in resList:
            f.write(j + '\n')
        f.close()

    print ('All done ' + str(datetime.datetime.now()))

if __name__ == "__main__":
    main()
