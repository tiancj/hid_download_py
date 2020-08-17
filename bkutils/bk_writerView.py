# encoding: utf8
#
# UART Download Tool
#
# Copyright (c) BekenCorp. (chunjian.tian@bekencorp.com).  All rights reserved.
#
# This software may be distributed under the terms of the BSD license.
# See README for more details.

import time
from .bootIntf import CBootIntf
from serial import Timeout
import binascii
from tqdm import tqdm

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

class UartDownloader(object):
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        self.bootItf = CBootIntf(port, 115200, 0.005)
        self.target_baudrate = baudrate
        self.pbar = None

    def log(self, text):
        """
        print text to tqdm progress bar
        """
        if not self.pbar:
            print("{}".format(text))
        else:
            self.pbar.set_description("{}".format(text))

    def programm(self, filename, startAddr=0x11000):

        # Step1: read file into system memory
        # TODO: sanity check
        with open(filename, "rb") as f:
            pfile = f.read()
        fileLen = filOLen = len(pfile)
        padding_len = 0x100 - (fileLen & 0xff)
        if padding_len:
            pfile += b'\xff'*padding_len
            fileLen += padding_len
            filOLen += padding_len
            # print("fileLen{}, padding_len {}".format(fileLen, padding_len))
            # print("FILE: ", binascii.b2a_hex(pfile, b' '))
        fileCrc = crc32_ver2(0xffffffff, pfile)
        total_num = filOLen // 0x1000


        # do_reset_signal()
        # reboot = "reboot"
        # self.bootItf.Start_Cmd(reboot)
        # time.sleep(0.1)
        self.pbar = tqdm(total=total_num, ncols=80)
        self.log("Getting Bus...")
        timeout = Timeout(10)

        # Step2: Link Check
        while True:
            r = self.bootItf.LinkCheck()
            if r:
                break
            if timeout.expired():
                self.log('Cannot get bus.')
                self.pbar.close()
                return
            # self.bootItf.Start_Cmd(reboot)
            # time.sleep(0.01)

        self.log("Gotten Bus...")
        self.bootItf.Drain()

        # Step3: set baudrate, delay 100ms
        if self.target_baudrate != 115200:
            if not self.bootItf.SetBR(self.target_baudrate, 50):
                self.log("Set baudrate failed")
                self.pbar.close()
                return
            self.log("Set baudrate successful")


        # Step4: erase 
        # Step4.1: read first 4k if startAddr not aligned with 4K
        eraseAddr = startAddr
        ss = s0 = eraseAddr & 0xfffff000     # 4K对齐的地址
        filSPtr = 0

        if eraseAddr & 0xfff:
            self.log("Aligning Flash Address...")

            # Read 4K from flash
            buf = self.bootItf.ReadSector(s0)
            l = 0x1000 - (eraseAddr & 0xfff)
            fl = l if l < fileLen else fileLen
            buf[eraseAddr&0xfff:eraseAddr&0xfff+fl] = pfile[:fl]
            self.bootItf.EraseBlock(0x20, s0)
            if not self.bootItf.WriteSector(s0, buf):
                self.log("WriteSector Failed")
                self.pbar.close()
                return
            filOLen -= fl
            filSPtr = fl
            s0 += 0x1000
            ss = s0

            if filOLen <= 0:
                # TODO: goto crc check
                return 


        # Step4.2: handle the last 4K
        # now ss is the new eraseAddr.
        # 文件结束地址
        filEPtr = fileLen
        s1 = eraseAddr + fileLen

        # If not 4K aligned, read the last sector, fill the data, write it back
        if s1 & 0xfff:
            # print("Handle file end...")
            buf = bytearray(b'\xff'*4096)   # fill with 0xFF
            buf[:s1&0xfff] = pfile[filEPtr-(s1&0xfff):]  # copy s1&0xfff len
            # print(time.time())
            for _ in range(4):
                if self.bootItf.EraseBlock(0x20, s1&0xfffff000):
                    break
                time.sleep(0.05)
            # time.sleep(0.1)

            # for _ in range(10):
            #    tt = self.bootItf.Read()
            #    print(tt)
            #print(time.time())
            if not self.bootItf.WriteSector(s1&0xfffff000, buf):
                self.log("WriteSector Failed")
                self.pbar.close()
                return
            # print(time.time())

            filEPtr = filEPtr - (s1&0xfff) 
            filOLen = filOLen - (s1&0xfff) 
            if filOLen <= 0:
                # TODO: goto crc check
                pass

        # print("Handle file end done")

        # Step4.3: 对齐64KB，如果擦除区域小于64KB
        len1 = ss + filOLen
        len0 = s0 & 0xffff0000
        if s0 & 0xffff:
            len0 += 0x10000
        if filOLen > len0 - s0:
            while s0 < len0:
                self.bootItf.EraseBlock(0x20, s0)
                s0 += 0x1000

        # print("fileOLen: {}, filSPtr: {}".format(filOLen, filSPtr))
        # Step4.4: Erase 64k, 4k, etc.
        # 按照64KB/4K block擦除
        len1 = ss + filOLen
        while s0 < len1:
            self.log("Erasing")
            rmn = len1 - s0
            if rmn > 0x10000:   # 64K erase
                self.bootItf.EraseBlock(0xd8, s0)
                s0 = s0+0x10000
            else:       # erase 4K
                self.bootItf.EraseBlock(0x20, s0)
                s0 = s0 + 0x1000


        # Step5: Write data
        i = 0
        while i < filOLen:
            self.log("Writing")
            for _ in range(4):
                if self.bootItf.WriteSector(ss+i, pfile[filSPtr+i:filSPtr+i+4*1024]):
                    self.pbar.update(1)
                    break
            else:
                self.log("WriteSector 1 Failed")
                self.pbar.close()
                return
            i += 0x1000


        # Step6: CRC check
        self.log("Verifing")
        if fileLen & 0xff:
            l2 = (fileLen & ~0xff) + 0x100
        else:
            l2 = fileLen
        ret,crc = self.bootItf.ReadCRC(startAddr, startAddr+l2-1)
        if not ret:
            self.log("Read CRC Failed")
            self.pbar.close()
            return
        if crc != fileCrc:
            self.log("CRC not equal")
            self.pbar.close()
            return

        self.log("Write Successful")
        self.pbar.close()

if __name__ == '__main__':
    downloader = UartDownloader()
