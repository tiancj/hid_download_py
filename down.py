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

def WriteHid(dev, txBuffer):
    outbuffer = bytearray(65)
    outbuffer[1:1+len(txBuffer)+1] = txBuffer
    return dev.write(outbuffer)

def ReadHid(dev, cnt=FT_MSG_SIZE_FLASH, timeout=1000):
    outbuf = dev.read(65, timeout)
    return outbuf[1:cnt+1]

def Wait_Busy_Down(dev):
    while True:
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        send_buf[0] = READ_REG_CMD
        send_buf[1] = 0
        send_buf[2] = 5
        WriteHid(dev, send_buf)
        out_buf = ReadHid(dev, 1)
        if not (out_buf[0] & 0x01):
            break


# 1.
def GetDeviceNumber(dev):
    send_buf = bytearray(1)
    send_buf[0] = FM_NUMBER
    WriteHid(dev, send_buf)
    out_buf = ReadHid(dev, 1)
    if out_buf[0] != 0xFF:
        return out_buf[0]
    return None

# 2.
def SetVccVppLoadStatu(dev):
    send_buf = bytearray(5)
    send_buf[0] = VPP_VCC_POWER_UPDATE
    send_buf[1] = 0
    send_buf[2] = 2 # soft spi
    send_buf[3] = 0
    send_buf[4] = 0
    WriteHid(dev, send_buf)
    out_buf = ReadHid(dev, 1)
    if out_buf[0] != 0xEE:
        return True
    return False


# 3. 
def CHIP_EXTERN_Reset(dev):
    chip_id = Read_ID(dev)

    # for default chip id
    CHIP_ENABLE_Command(dev)
    send_buf = bytearray(1)
    send_buf[0] = 0x00
    Statu_Write(dev, SPI_STATU_WR_LOW_CMD, send_buf)


# 3.
def Read_ID(dev):
    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    send_buf[0] = READ_FLASH_CMD
    send_buf[1] = SPI_ID_READ_CMD
    send_buf[5] = 0
    send_buf[6] = 3
    WriteHid(dev, send_buf)
    out_buf = ReadHid(dev, 3)
    return out_buf

def CHIP_ENABLE_Command(dev):
    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    send_buf[0] = WRITE_COMMAND_CMD
    send_buf[1] = SPI_CHIP_ENABLE_CMD
    WriteHid(dev, send_buf)
    out_buf = ReadHid(dev, 3)
    # return out_buf
    Wait_Busy_Down(dev)

def Statu_Write(dev, cmd, cmdHead):
    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    send_buf[0] = WRITE_FLASH_CMD
    send_buf[1] = cmd
    send_buf[5] = 0x0
    send_buf[6] = len(cmdHead)
    send_buf[7:7+len(cmdHead)+1] = cmdHead
    WriteHid(dev, send_buf)
    Wait_Busy_Down(dev)

# ChipErase(cDlg)
def CHIP_EXTERN_Erase(dev):
    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    send_buf[0] = WRITE_COMMAND_CMD
    send_buf[1] = SPI_CHIP_ERASE_CMD
    WriteHid(dev, send_buf)
    Wait_Busy_Down(dev)


def DownImage(dev, filename):
    CHIP_EXTERN_Reset(dev)
    CHIP_EXTERN_Erase(dev)
    WriteImage(dev, filename)
    # DownloadStatu(dev)

def FlashLoadStanby(dev, cmd, size):
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
    WriteHid(dev, send_buf)

def DevWriteImage(dev, f, writeLength):
    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    for i in range(FT_MSG_SIZE_FLASH):
        send_buf[i] = 0xff
    send_buf[0] = WRITE_IMAGE_DATA_CMD
    buf = f.read(writeLength)
    send_buf[1:1+len(buf)+1] = buf
    WriteHid(dev, send_buf)

def DownloadImageData(dev, filename):
    statinfo = os.stat(filename)
    size = statinfo.st_size
    total_num = int((size + HID_BUF - 1)/HID_BUF)
    i = 0
    f = open(filename, "rb")
    while i < total_num:
        DevWriteImage(dev, f, HID_BUF)
    f.close()


def WriteImage(dev, filename):
    statinfo = os.stat(filename)
    size = statinfo.st_size
    FlashLoadStanby(dev, WRITE_IMAGE_START_CMD, size)
    DownloadImageData(dev, filename)
    FlashLoadFinish(dev)


def FlashLoadFinish(dev):
    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    send_buf[0] = WRITE_IMAGE_FINISH_CMD
    WriteHid(dev, send_buf)
    out_buf = ReadHid(dev, 1)
    return out_buf  # != 0x8

def SetVccVppIdleStatu(dev):
    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    send_buf[0] = VPP_VCC_POWER_UPDATE
    send_buf[1] = IDLE_STATE
    send_buf[2] = SOFT_SPI
    send_buf[3] = 0
    send_buf[4] = 0
    WriteHid(dev, send_buf)
    out_buf = ReadHid(dev, 1)
    return out_buf # 0xEE
   

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} <filename>'.format(sys.argv[0]))
        sys.exit(-1)

    dev = hid.open(0x10c4, 0x0033)

    #1.
    dn = GetDeviceNumber(dev)

    #2. 
    SetVccVppLoadStatu(dev)

    #3.
    DownImage(dev, sys.argv[1])

    #4.
    SetVccVppIdleStatu(dev)


