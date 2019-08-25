#!/usr/bin/env python3

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
# b_spi_mode： 	HARD_SPI, HARD_UART, SOFT_SPI, SOFT_I2C
# b_erase_mode： 	Erase_UNUSE, Erase_ALL, Erase_MAIN
# b_object_mode： 下载方式 OFF_LINE_TOOL(离线下载), CHIP(芯片下载),
# b_number_mode： 设备号获取方式  FROM_DIVER, FROM_DEFAUT
# m_StartAddrForContor: 
# m_StartAddr: 起始地址
# m_LoadLength：为0时擦除整个flash
# ObjectChip.Index： 芯片选择
# FuncSelect：	tagDownload, tagDumpimage, tagErase, tagReset, tagInDebug, tagOutDebug, NoDef,

import os
import hid
import sys
import time
import extern_flash

# Chip Type
EXTERN_FLASH = 0
CHIP_TYPE_BK7231 = 1
CHIP_TYPE_BK7231U = 2
CHIP_TYPE_BK7221U = 3
CHIP_TYPE_BK7251 = 4

# Flash Sector Length
FLASH_SECTOR_256_SIZE = 256

# Download Format
EXTERN_FLASH_FORMAT = 0
CHIP_BK7231U_FORMAT = 1



READ_IMAGE_START_CMD = 0
FM_VERSION = 1
FM_NUMBER = 2
VPP_VCC_POWER_UPDATE = 3
WRITE_COMMAND_CMD = 4
READ_REG_CMD = 5
WRITE_REG_CMD = 6
READ_FLASH_CMD = 7
WRITE_FLASH_CMD = 8
WRITE_IMAGE_FINISH_CMD = 9
READ_AUTO_START_CMD = 0xa
WRITE_IMAGE_DATA_CMD = 0xb
WRITE_IMAGE_START_CMD = 0xc
RESET_ENABLE_PIN = 0xd
UART_COMAND_WRITE = 0xe
UART_CHANGE_1M_RATE = 0xf
RESET_VCC_ENABLE_PIN = 0x10
SECTER_WRITE = 0x11
UART_CHANGE_BASE_RATE = 0x12
SET_FLASH_FLAG_SET = 0x13

EXTERN_FLASH_FORMAT = 0
CHIP_BK7231U_FORMAT = 11

DOWNLOAD_STATE = 0
IDLE_STATE = 1
ERROR_STATE = 2

HARD_SPI = 0
HARD_UART = 1
SOFT_SPI = 2
SOFT_I2C = 3

b_spi_mode = SOFT_SPI

# CHIP_BK3435_Reset
SPI_CHIP_ERASE_CMD		= 0xc7
SPI_CHIP_ENABLE_CMD		= 0x06
SPI_READ_PAGE_CMD   	= 0x03
SPI_WRITE_PAGE_CMD   	= 0x02
SPI_SECTRO_ERASE_CMD	= 0x20
SPI_SECUR_SECTOR_ERASE	= 0x44
SPI_ID_READ_CMD			= 0x9F
SPI_STATU_WR_LOW_CMD	= 0x01
SPI_STATU_WR_HIG_CMD	= 0x31

FT_MSG_SIZE_FLASH = 0x40
HID_BUF = 63

debug = True

class HidDevice(object):
    def __init__(self, vid=0x10c4, pid=0x0033):
        self.vid = vid
        self.pid = pid
        self.dev = hid.device()

    def WriteHid(self, txBuffer):
        # outbuffer = bytearray(65)
        # # print(len(outbuffer))
        # outbuffer[1:1+len(txBuffer)] = txBuffer
        # # print(len(outbuffer))
        outbuffer = bytearray(64)
        outbuffer[:len(txBuffer)] = txBuffer
        if debug:
            print('TX: ', '00 ' + ''.join(['{:02X} '.format(i) for i in outbuffer]))
        return self.dev.write(outbuffer)

    def ReadHid(self, cnt=FT_MSG_SIZE_FLASH, timeout=1000):
        outbuf = self.dev.read(64, timeout)
        if debug:
            print('RX: ', '00 ' + ''.join(['{:02X} '.format(i) for i in outbuf]))
        # return outbuf[1:cnt+1]
        return outbuf[:cnt]

    def Open(self):
        self.dev.open(self.vid, self.pid)
        # print("dev", dev)

    def Close(self):
        self.dev.close()


class FlashBase(object):
    def __init__(self, dev):
        # default values
        self.dev = dev
        self.erase_sector = 4*1024
        self.max_image_len = 2*1024*1024
        self.spi_div_clk = 0
        self.down_format = EXTERN_FLASH_FORMAT

    def reset(self):
        raise NotImplementedError

    def erase(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def end(self):
        raise NotImplementedError

class HidDownloader(object):
    def __init__(self, filename):
        self.filename = filename
        self.dev = HidDevice()
        self.flash = extern_flash.ExternFlash(self.dev)

    def GetDeviceNumber(self):
        send_buf = bytearray(1)
        send_buf[0] = FM_NUMBER
        self.dev.WriteHid(send_buf)
        out_buf = self.dev.ReadHid(1)
        if out_buf[0] != 0xFF:
            return out_buf[0]
        return None

    def SetVccVppLoadStatu(self):
        send_buf = bytearray(5)
        send_buf[0] = VPP_VCC_POWER_UPDATE
        send_buf[1] = 0
        send_buf[2] = 2 # soft spi
        send_buf[3] = 0
        send_buf[4] = 0
        self.dev.WriteHid(send_buf)
        out_buf = self.dev.ReadHid(1)
        if out_buf[0] != 0xEE:
            return True
        return False

    def DownImage(self):
        self.flash.reset()  # CHIP_EXTERN_Reset(dev)
        #   CHIP_ENABLE_Command(dev)   FIXME TODO
        self.flash.erase()  # 04 C7
        self.WriteImage()
        self.flash.end()
        self.FlashLoadFinish()

    def FlashLoadStanby(self, cmd, size):
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        send_buf[0] = cmd
        send_buf[1] = size & 0xFF
        send_buf[2] = (size & 0xFF00) >> 8
        send_buf[3] = (size & 0xFF0000) >> 16
        send_buf[4] = (size & 0xFF000000) >> 24
        send_buf[5] = 1
        send_buf[6] = 0
        send_buf[7] = 0
        send_buf[8] = 0
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
    
    def DownloadImageData(self, size):
        #statinfo = os.stat(filename)
        #size = statinfo.st_size
        total_num = (size + HID_BUF - 1)//HID_BUF
        i = 0
        f = open(self.filename, "rb")
        while i < total_num:
            self.DevWriteImage(f, HID_BUF)
            i += 1
        f.close()

    def WriteImage(self):
        statinfo = os.stat(self.filename)
        size = statinfo.st_size
        size = (size+255)//256*256
        self.FlashLoadStanby(WRITE_IMAGE_START_CMD, size)
        self.DownloadImageData(size)

    def FlashLoadFinish(self):
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        send_buf[0] = WRITE_IMAGE_FINISH_CMD
        self.dev.WriteHid(send_buf)
        out_buf = self.dev.ReadHid(1)
        return out_buf  # != 0x8

    def SetVccVppIdleStatu(self):
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        send_buf[0] = VPP_VCC_POWER_UPDATE
        send_buf[1] = IDLE_STATE
        send_buf[2] = SOFT_SPI
        send_buf[3] = 0
        send_buf[4] = 0
        self.dev.WriteHid(send_buf)
        out_buf = self.dev.ReadHid(1)
        return out_buf # 0xEE

    def startDownload(self):
        self.dev.Open()
        dn = self.GetDeviceNumber()
        print('dn', dn)
        self.SetVccVppLoadStatu()
        self.DownImage()
        self.SetVccVppIdleStatu()
        self.dev.Close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} <filename>'.format(sys.argv[0]))
        sys.exit(-1)

    hid_downloader = HidDownloader(sys.argv[1])
    hid_downloader.startDownload()

    