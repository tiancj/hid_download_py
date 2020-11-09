#!/usr/bin/env python3
# encoding: utf8
#
# HID Download Tool
#
# Copyright (c) BekenCorp. (chunjian.tian@bekencorp.com).  All rights reserved.
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

from .hid_device import HidDevice
from .hid_commands import *
from .hid_chip_list import *
import os
import sys
import platform
from tqdm import tqdm

HID_BUF = 63
FT_MSG_SIZE_FLASH = 0x40
posix = True
if platform.system() == 'Windows':
    posix = False

class HidDownloader:

    """
    HID Downloader tool for Beken

    downloader = HidDownloader(CHIP_TYPE_BK7231U, "bk7231_crc.bin")
    downloader.Download()
    """

    def __init__(self, chipIndex, spi_mode=SOFT_SPI, erase_mode=Erase_ALL, 
                        vid=0x10c4, pid=0x0033, path=None, extra=0):
        self.chipIndex = chipIndex  # chip type
        self.spi_mode = spi_mode
        self.erase_mode = erase_mode
        self.vid = vid
        self.pid = pid
        self.path = path
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
        total_num = (size + HID_BUF - 1)//HID_BUF
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
            self.dev = HidDevice(self.vid, self.pid, self.path)
            self.dev.Open()
        except OSError as e:
            self.log("打开SPI失败")
            self.pbar.close()
            return False

        try:
            self.GetDeviceNumber()
            if self.ChipStartDownload(filename):
                # print('Success')
                self.log("烧录成功")
            else:
                # print('Failed')
                self.log("烧录失败")
        except OSError as e:
            self.log("烧录失败")
        self.pbar.close()

    def ChipStartDownload(self, filename):
        if not self.SetVccVppLoadStatu():
            # print("Vpp打开失败(!=0xee)！")
            self.log("Vpp打开失败")
            return False
        if not self.DownImage(filename):
            return False
        if not self.SetVccVppIdleStatu(True):
            return False
        return True


    def SelectChipType(self):
        # return self.DownFormat, SpiDivClkListGet(self.DownFormat)
        return self.DownFormat, SpiDivClkListGet(self.chipIndex)


    ## Verfied
    def SetVccVppLoadStatu(self):
        send_buf = bytearray(5)
        send_buf[0] = VPP_VCC_POWER_UPDATE
        send_buf[1] = DOWNLOAD_STATE
        send_buf[2] = self.spi_mode
        ChipSelect, SpiClkDiv = self.SelectChipType()
        # print("ChipSelect {}, SpiClkDiv {}".format( ChipSelect, SpiClkDiv))
        send_buf[3] = SpiClkDiv
        send_buf[4] = ChipSelect
        self.dev.WriteHid(send_buf)
        out_buf = self.dev.ReadHid(1)
        if out_buf[0] != 0xEE:
            return False
        return True

    def SetVccVppIdleStatu(self, success):
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        send_buf[0] = VPP_VCC_POWER_UPDATE
        send_buf[1] = IDLE_STATE if success else ERROR_STATE
        send_buf[2] = SOFT_SPI
        ChipSelect, SpiClkDiv = self.SelectChipType()
        send_buf[3] = SpiClkDiv
        send_buf[4] = ChipSelect
        self.dev.WriteHid(send_buf)
        out_buf = self.dev.ReadHid(1)
        if out_buf[0] != 0xEE:
            return False
        return True

    def DownImage(self, filename):
        reset = ResetGet(self.chipIndex)
        if reset:
            # print("->>芯片复位中....")
            self.log("芯片复位中")
            if not reset(self, self.spi_mode, self.DownFormat):
                # print("downImage复位失败!!")
                self.log("复位失败")
                return False
        
        erase = EraseGet(self.chipIndex)
        if erase:
            # print("->>芯片擦除中....")
            self.log("芯片擦除中")
            if not erase(self):
                self.log("擦除失败!!")
                return False

        # print("->>芯片下载中....")
        self.log("芯片下载中")
        return self.WriteImage(filename)


    def WriteImage(self, filename):
        statinfo = os.stat(filename)
        size = statinfo.st_size
        size = (size+255)//256*256
        self.FlashLoadStanby(WRITE_IMAGE_START_CMD, size)
        self.DownloadImageData(filename, size)
        self.FlashLoadFinish()
        return True

    def FlashLoadStanby(self, cmd, size):
        """
        芯片烧录信息加载
        """
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        send_buf[0] = cmd
        send_buf[1] = size & 0xFF
        send_buf[2] = (size & 0xFF00) >> 8
        send_buf[3] = (size & 0xFF0000) >> 16
        send_buf[4] = (size & 0xFF000000) >> 24
        send_buf[5] = self.ImageSectorLen//256
        send_buf[6] = self.ImageSectorLen%256
        send_buf[7] = 0     # FIXME  GetBlockId(SectorLength, MaxFileSize)
        send_buf[8] = 0     # FIXME
        self.dev.WriteHid(send_buf)

    def DevWriteImage(self, f, writeLength):
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        for i in range(FT_MSG_SIZE_FLASH):
            send_buf[i] = 0xff
        send_buf[0] = WRITE_IMAGE_DATA_CMD
        buf = f.read(writeLength)
        if buf:
            send_buf[1:1+len(buf)+1] = buf
        self.dev.WriteHid(send_buf)


    def DownloadImageData(self, filename, size):
        total_num = (size + HID_BUF - 1)//HID_BUF
        i = 0
        f = open(filename, "rb")

        while i < total_num:
            # print("\rWriting:   {:.2f}%".format((i/total_num)*100), end='')
            self.pbar.update(1)
            self.DevWriteImage(f, HID_BUF)
            i += 1
        # print('\rWrite End               ')
        self.log("写入结束")
        f.close()

    def FlashLoadFinish(self):
        end = EndGet(self.chipIndex)
        if end:
            if not end(self):
                self.log("芯片结束下载超时")
                return False
        
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        send_buf[0] = 0
        self.dev.WriteHid(send_buf)
        out_buf = self.dev.ReadHid(1)
        if out_buf and out_buf[0] != 0x48:
            self.log("芯片校验失败")
            return False

    def GetDeviceNumber(self):
        send_buf = bytearray(1)
        send_buf[0] = FM_NUMBER
        self.dev.WriteHid(send_buf)
        out_buf = self.dev.ReadHid(1)
        if out_buf and out_buf[0] != 0xFF:
            return out_buf[0]
        return None
