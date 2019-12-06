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

debug = False
verbose = True


def WriteHid(dev, txBuffer):
    # outbuffer = bytearray(65)
    # # print(len(outbuffer))
    # outbuffer[1:1+len(txBuffer)] = txBuffer
    # # print(len(outbuffer))
    outbuffer = bytearray(64)
    outbuffer[:len(txBuffer)] = txBuffer
    if debug:
        print('TX: ', '00 ' + ''.join(['{:02X} '.format(i) for i in outbuffer]))
    return dev.write(outbuffer)

def ReadHid(dev, cnt=FT_MSG_SIZE_FLASH, timeout=1000):
    outbuf = dev.read(64, timeout)
    if debug:
        print('RX: ', '00 ' + ''.join(['{:02X} '.format(i) for i in outbuf]))
    # return outbuf[1:cnt+1]
    return outbuf[:cnt]


def GetDeviceNumber(dev):
    send_buf = bytearray(1)
    send_buf[0] = FM_NUMBER
    WriteHid(dev, send_buf)
    out_buf = ReadHid(dev, 1)
    if out_buf[0] != 0xFF:
        return out_buf[0]
    return None

