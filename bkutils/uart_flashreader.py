# encoding: utf8
#
# UART Download Tool
#
# Copyright (c) BekenCorp. (chunjian.tian@bekencorp.com).  All rights reserved.
#
# This software may be distributed under the terms of the BSD license.
# See README for more details.

import time
from .boot_intf import CBootIntf
from serial import Timeout
import binascii
from tqdm import tqdm
from .flash_list import *

debug = False

# make crc32 table
crc32_table = []
for i in range(0,256):
    c = i
    for j in range(0,8):
        if c&1:
            c = 0xEDB88320 ^ (c >> 1)
        else:
            c = c >> 1
    crc32_table.append(c)

# print(crc32_table)

def crc32_ver2(crc, buf):
    for c in buf:
        crc = (crc>>8) ^ crc32_table[(crc^c)&0xff]
    return crc

class UartFlashReader(object):
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, unprotect=False):
        # self.bootItf = CBootIntf(port, 115200, 0.01)
        self.bootItf = CBootIntf(port, 115200, 0)
        self.target_baudrate = baudrate
        self.unprotect = unprotect
        self.pbar = None

    def log(self, text):
        """
        print text to tqdm progress bar
        """
        if not self.pbar:
            print("{}".format(text))
        else:
            self.pbar.set_description("{:<16}".format(text))

    def do_reset_signal(self):
        self.bootItf.ser.dtr = 0
        self.bootItf.ser.rts = 1
        time.sleep(0.2)
        self.bootItf.ser.rts = 0

    def readflash(self, startAddr=0x11000, readLength=(0x1000*16)):
        self.do_reset_signal()
        self.log("Getting bus...")
        timeout = Timeout(10)
        while True:
            r = self.bootItf.LinkCheck()
            if r:
                break
            if timeout.expired():
                self.log('Cannot get bus.')
                return
            count += 1
            if count > 500:
                self.bootItf.Start_Cmd(b"reboot\r\n")
                count = 0
        self.log("Gotten Bus...")
        time.sleep(0.01)
        self.bootItf.Drain()

        # Step3: set baudrate, delay 100ms
        if self.target_baudrate != 115200:
            if not self.bootItf.SetBR(self.target_baudrate, 20):
                self.log("Set baudrate failed")
                return
            self.log("Set baudrate successful")

        if self.unprotect:
            # Get Mid
            mid = self.bootItf.GetFlashMID()
            # print("\n\n mid: {:x}\n\n".format(mid))
            if self._Do_Boot_ProtectFlash(mid, True) != 1:
                self.log("Unprotect Failed")
                return
        
        addr = startAddr & 0xfffff000
        count = 0
        buffer = bytes()
        while count < readLength:
            sector = self.bootItf.ReadSector(addr)
            if sector is not None:
                buffer += sector
            addr += 0x1000
            count += 0x1000

        self.log("Read Successful")

        for i in range(3):
            time.sleep(0.01)
            self.bootItf.SendReboot()

        return buffer[:readLength]
        
    
    def _Do_Boot_ProtectFlash(self, mid:int, unprotect:bool):
        # 1. find flash info
        flash_info = GetFlashInfo(mid)
        if flash_info is None:
            return -1
        if debug:
            print(flash_info.icNam, flash_info.manName)

        timeout = Timeout(1)

        # 2. write (un)protect word
        cw = flash_info.cwUnp if unprotect else flash_info.cwEnp
        while True:
            sr = 0

            # read sr register
            for i in range(flash_info.szSR):
                f = self.bootItf.ReadFlashSR(flash_info.cwdRd[i])
                if f[0]:
                    sr |= f[2] << (8 * i)
                    if debug: print("sr: {:x}".format(sr))

            if debug:
                print("final sr: {:x}".format(sr))
                print("msk: {:x}".format(flash_info.cwMsk))
                print("cw: {:x}, sb: {}, lb: {}".format(cw, flash_info.sb, flash_info.lb))
                print("bfd: {:x}".format(BFD(cw, flash_info.sb, flash_info.lb)))

            # if (un)protect word is set
            if (sr & flash_info.cwMsk) == BFD(cw, flash_info.sb, flash_info.lb):
                return 1
            if timeout.expired():
                return -2
            # // set (un)protect word
            srt = sr & (flash_info.cwMsk ^ 0xffffffff)
            srt |= BFD(cw, flash_info.sb, flash_info.lb)
            f = self.bootItf.WriteFlashSR(flash_info.szSR, flash_info.cwdWr[0], srt & 0xffff)

            time.sleep(0.01)

        return 1


if __name__ == '__main__':
    reader = UartFlashReader()
