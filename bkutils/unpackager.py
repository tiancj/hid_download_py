# encoding: utf8
#
# UART Download Tool
#
# Copyright (c) BekenCorp. (chunjian.tian@bekencorp.com).  All rights reserved.
#
# This software may be distributed under the terms of the BSD license.
# See README for more details.

#from serial import serialutil
import binascii
import os

debug = False

class Unpackager(object):
    def __init__(self, sourcefile, destfile):
        with open(sourcefile, "rb") as f:
            source = f.read()
        sourceLen = len(source)

        end = sourceLen - 256

        # find end of firmware
        while (end > 0):
            if not source[end] == 0xff:
                #self.log("{:x} = {:x}".format(end, source[end]))
                break
            #self.log("{:x} = {:x}".format(end, source[end]))
            end-=1
        
        sourceLen = end


        dest = b''
        i = 0
        while (i < sourceLen):
            dest += source[i:i+32]
            i += 34

        f = open(destfile, "wb")
        f.write(dest)
        f.close()
        self.log("Wrote unpackaged file to "+destfile)

        os.system("encrypt "+destfile+"  510fb093 a3cbeadc 5993a17e c7adeb03 10000")



    def log(self, text):
        print("{}".format(text))

