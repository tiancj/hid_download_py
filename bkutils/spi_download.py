#!/usr/bin/env python3
# encoding: utf8
#
# direct SPI Download Tool - e.gt. on RPI
#
# Copyright (c) BekenCorp. (chunjian.tian@bekencorp.com).  All rights reserved.
# Copyright (c) Btsimonh. All rights reserved on modifications.
#
# This software may be distributed under the terms of the BSD license.
# See README for more details.

# 
# OnReset  //afx_msg
# OnErase  //afx_msg
# OnUploadImage  //afx_msg
# OnDownloadImage //afx_msg ->
#   InDownloadEnvironment ->
#       DriverLinkHidHandle(tagDownload)
#           Progreess(tagDownload)  //DownloadProc
#           DownloadProc ->
#               ChipStartDownload ->
#                   ReadLoadEditDrop        加载Image文件
#                   SetVccVppLoadStatu
#                   DownImage
#                   SetVccVppIdleStatu
#               DownloadEnd
#
# spi_mode： 	HARD_SPI, HARD_UART, SOFT_SPI, SOFT_I2C
# erase_mode： 	Erase_UNUSE, Erase_ALL, Erase_MAIN
# b_object_mode： 下载方式 OFF_LINE_TOOL(离线下载), CHIP(芯片下载),
# b_number_mode： 设备号获取方式  FROM_DIVER, FROM_DEFAUT
# m_StartAddrForContor: 
# m_StartAddr: 起始地址
# m_LoadLength：为0时擦除整个flash
# ObjectChip.Index： 芯片选择
# FuncSelect：	tagDownload, tagDumpimage, tagErase, tagReset, tagInDebug, tagOutDebug, NoDef,

from .hid_commands import *
from .hid_chip_listSPI import *
import os
import sys
import platform
from tqdm import tqdm
import spidev
import time
import RPi.GPIO as GPIO

CENGPIO = 22
SPI_BUF = 256
FT_MSG_SIZE_FLASH = 0x40
posix = True
if platform.system() == 'Windows':
    posix = False

class SpiDownloader:

    """
    SPI Downloader tool for Beken

    downloader = SpiDownloader(CHIP_TYPE_BK7231U, "bk7231_crc.bin", extra, startaddr, baudrate)
    downloader.Download()
    """

    def __init__(self, chipIndex, erase_mode=Erase_UNUSE, 
                        path=None, extra=0, startaddr=0x11000, baudrate=50000, length=0x1000):
        self.chipIndex = chipIndex  # chip type
        self.erase_mode = erase_mode
        self.path = path
        self.startaddr = startaddr
        self.readlen = length
        self.baudrate = baudrate
        # print("chipIndex ", chipIndex)
        self.DownFormat = DownFormatListGet(chipIndex)
        self.MaxFileSize = FlashLoadFileMaxSizeGet(chipIndex)
        self.ImageSectorLen = FlashSectorLengthListGet(chipIndex)
        self.EraseSectorLen = FlashEraseSectorLenGet(chipIndex)
        self.MaxFileSize = FlashLoadFileMaxSizeGet(chipIndex)
        self.RollCodeLen = RollCodeLengthListGet(chipIndex)
        self.pbar = None
        self.extra = extra

    def log(self, text):
        """
        print text to tqdm progress bar
        """
        if not self.pbar:
            print("[{}]: {}".format(self.extra, text))
        else:
            self.pbar.set_description("[{}]: {}".format(self.extra, text))

    def Download(self, filename):
        """
        download filename to BK72xx by SPI
        """
        statinfo = os.stat(filename)
        size = statinfo.st_size
        size = (size+255)//256*256
        total_num = (size + SPI_BUF - 1)//SPI_BUF
        if posix:
            self.pbar = tqdm(total=total_num, position=self.extra, ncols=80)
        else:
            self.pbar = tqdm(total=total_num, position=self.extra, ncols=60, 
                    # bar_format="{l_bar}{bar}| [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
                    # bar_format="{l_bar}{bar}| [{elapsed}<{remaining}, ' ']"
                    # bar_format="{l_bar}{bar}|[{rate_fmt}{postfix}]"
                    bar_format="{desc} {percentage:3.0f}% [{elapsed}/{remaining}{postfix}, {rate_fmt}{postfix}]"
                )

        try:
            self.spi = spidev.SpiDev()
            self.spi.open(0, 0)
            self.spi.max_speed_hz = self.baurate
            GPIO.setup(CENGPIO, GPIO.OUT)

        except OSError as e:
            self.log("Can't open SPI, check the driver is enabled in the OS")
            self.pbar.close()
            return False

        try:
            if self.ChipStartDownload(filename):
                # print('Success')
                self.log("Success")
            else:
                # print('Failed')
                self.log("Failed")
        except OSError as e:
            self.log("Exception")
        self.pbar.close()

    def Read(self, filename):
        """
        read filename from BK72xx by SPI
        """
        size = self.readlen
        size = (size+255)//256*256
        total_num = (size + SPI_BUF - 1)//SPI_BUF
        if posix:
            self.pbar = tqdm(total=total_num, position=self.extra, ncols=80)
        else:
            self.pbar = tqdm(total=total_num, position=self.extra, ncols=60, 
                    # bar_format="{l_bar}{bar}| [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
                    # bar_format="{l_bar}{bar}| [{elapsed}<{remaining}, ' ']"
                    # bar_format="{l_bar}{bar}|[{rate_fmt}{postfix}]"
                    bar_format="{desc} {percentage:3.0f}% [{elapsed}/{remaining}{postfix}, {rate_fmt}{postfix}]"
                )

        try:
            self.spi = spidev.SpiDev()
            self.spi.open(0, 0)
            self.spi.max_speed_hz = self.baurate
            GPIO.setup(CENGPIO, GPIO.OUT)

        except OSError as e:
            self.log("Can't open SPI, check the driver is enabled in the OS")
            self.pbar.close()
            return False

        try:
            if self.ReadStart(filename):
                # print('Success')
                self.log("Success")
            else:
                # print('Failed')
                self.log("Failed")
        except OSError as e:
            self.log("Exception")
        self.pbar.close()

    def ReadStart(self, filename):
        # set CEN low for 1s
        self.ChipReset()
        reset = ResetGet(self.chipIndex)
        if reset:
            # print("->>芯片复位中....")
            self.log("Attempt Reset")
            if not reset(self, self.DownFormat):
                # print("downImage复位失败!!")
                self.log("reset failed")
                return False
        count = 0
        addr = self.startaddr
        f = open(filename, "wb")
        size = self.readlen
        size = (size+255)//256*256

        while count < size:
            buf = f.read(256)
            send_buf = bytearray(4+256)
            send_buf[0] = 0x03
            send_buf[1] = (addr & 0xFF0000) >> 16
            send_buf[2] = (addr & 0xFF00) >> 8
            send_buf[3] = addr & 0xFF
            result = self.spi.xfer2(send_buf)
            count += 256
            addr += 256
            f.write(result[4:4+256])
            self.pbar.update(1)

        f.close()

        self.ChipReset()
        return True


    def ChipReset():
        # set CEN low for 1s
        GPIO.setup(CENGPIO, GPIO.OUT)
        GPIO.output(led, GPIO.LOW)
        time.sleep(1)
        GPIO.output(led, GPIO.HIGH)

    def ChipStartDownload(self, filename):
        # set CEN low for 1s
        self.ChipReset()

        if not self.DownImage(filename):
            return False

        self.ChipReset()
        return True

    def SelectChipType(self):
        # return self.DownFormat, SpiDivClkListGet(self.DownFormat)
        return self.DownFormat, SpiDivClkListGet(self.chipIndex)

    def DownImage(self, filename):
        reset = ResetGet(self.chipIndex)
        if reset:
            # print("->>芯片复位中....")
            self.log("Attempt Reset")
            if not reset(self, self.DownFormat):
                # print("downImage复位失败!!")
                self.log("reset failed")
                return False
        
        if erase_mode == ERASE_ALL:
            erase = EraseGet(self.chipIndex)
            if erase:
                # print("->>芯片擦除中....")
                self.log("whole chip erased")
                if not erase(self):
                    self.log("whole chip erase failed!!")
                    return False

        # print("->>芯片下载中....")
        self.log("writing..")
        return self.WriteImage(filename)


    def WriteImage(self, filename):
        #self.FlashLoadStanby(WRITE_IMAGE_START_CMD, size)

        statinfo = os.stat(filename)
        size = statinfo.st_size
        size = (size+255)//256*256

        count = 0
        addr = self.startaddr
        f = open(filename, "rb")

        while count < size:
            if self.erase_mode != ERASE_ALL:
                if not (addr & 0xfff):
                    CHIP_ENABLE_Command(self.spi)
                    send_buf = bytearray(4+256)
                    send_buf[0] = 0x20
                    send_buf[1] = (addr & 0xFF0000) >> 16
                    send_buf[2] = (addr & 0xFF00) >> 8
                    send_buf[3] = addr & 0xFF
                    send_buf[4:4+256] = self.spi.xfer(send_buf)
                    Wait_Busy_Down(self.spi)

            buf = f.read(256)
            if buf:
                CHIP_ENABLE_Command(self.spi)
                send_buf = bytearray(4+256)
                send_buf[0] = 0x03
                send_buf[1] = (addr & 0xFF0000) >> 16
                send_buf[2] = (addr & 0xFF00) >> 8
                send_buf[3] = addr & 0xFF
                send_buf[4:4+256] = buf
                self.spi.xfer(send_buf)
            count += 256
            addr += 256
            self.pbar.update(1)
            
        f.close()

        self.FlashLoadFinish()
        return True

    def FlashLoadFinish(self):
        end = EndGet(self.chipIndex)
        if end:
            if not end(self):
                self.log("flash end commands failed")
                return False
        return True
