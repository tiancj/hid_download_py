import time
import struct 
from ..commands import *

FT_MSG_SIZE_FLASH = 0x40

SPI_CHIP_ERASE_CMD		= 0xc7
SPI_CHIP_ENABLE_CMD		= 0x06
SPI_READ_PAGE_CMD   	= 0x03
SPI_WRITE_PAGE_CMD   	= 0x02
SPI_SECTRO_ERASE_CMD	= 0x20
SPI_SECUR_SECTOR_ERASE	= 0x44
SPI_ID_READ_CMD			= 0x9F
SPI_STATU_WR_LOW_CMD	= 0x01
SPI_STATU_WR_HIG_CMD	= 0x31

def Wait_Busy_Down(hidDev):
    while True:
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        send_buf[0] = READ_REG_CMD
        send_buf[1] = 0x00
        send_buf[2] = 0x05
        hidDev.WriteHid(send_buf)
        out_buf = hidDev.ReadHid(1)
        if not (out_buf[0] & 0x01):
            break
        time.sleep(0.1)

def Read_ID(hidDev):
    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    send_buf[0] = READ_FLASH_CMD
    send_buf[1] = SPI_ID_READ_CMD
    send_buf[5] = 0x00
    send_buf[6] = 0x03
    hidDev.WriteHid(send_buf)
    out_buf = hidDev.ReadHid(3)
    flash_id = out_buf
    flash_id.append(0)
    flash_id = bytes(flash_id)
    flash_id = struct.unpack('<I', flash_id[0:4])[0]
    return flash_id

def CHIP_ENABLE_Command(hidDev):
    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    send_buf[0] = WRITE_COMMAND_CMD
    send_buf[1] = SPI_CHIP_ENABLE_CMD
    hidDev.WriteHid(send_buf)
    Wait_Busy_Down(hidDev)

def Statu_Write(hidDev, cmd, cmdHead):
    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    send_buf[0] = WRITE_FLASH_CMD
    send_buf[1] = cmd
    send_buf[5] = 0x0
    send_buf[6] = len(cmdHead)
    send_buf[7:7+len(cmdHead)+1] = cmdHead
    hidDev.WriteHid(send_buf)
    Wait_Busy_Down(hidDev)

def CHIP_EXTERN_Reset(hidDev, *args):
    RunStatu = True
    
    Id = Read_ID(hidDev)
    print("flash_id: {:X}".format(Id))

    if Id == 0x001340C8 or Id == 0x001640C8:
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        CHIP_ENABLE_Command(hidDev)
        send_buf[0] = 0
        Statu_Write(hidDev, SPI_STATU_WR_LOW_CMD, send_buf)
        send_buf[0] = 0
        Statu_Write(hidDev, SPI_STATU_WR_HIG_CMD, send_buf)
    elif Id == 0x001440E0 or Id == 0x001423C2:
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        CHIP_ENABLE_Command(hidDev)
        send_buf[0] = 0x00
        send_buf[1] = 0x08
        Statu_Write(hidDev, SPI_STATU_WR_LOW_CMD, send_buf)
    elif Id == 0x001340E0 or Id == 0x001323C2:
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        CHIP_ENABLE_Command(hidDev)
        send_buf[0] = 0x00
        send_buf[1] = 0x00
        Statu_Write(hidDev, SPI_STATU_WR_LOW_CMD, send_buf)
    elif Id == 0x00FFFFFF or Id == 0x0:
        RunStatu = False
    else:
        send_buf = bytearray(1)
        CHIP_ENABLE_Command(hidDev)
        send_buf[0] = 0
        Statu_Write(hidDev, SPI_STATU_WR_LOW_CMD, send_buf)

    if RunStatu:
        time.sleep(0.5)

    return RunStatu

def CHIP_EXTERN_Erase(hidDev):
    CHIP_ENABLE_Command(hidDev)
    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    send_buf[0] = WRITE_COMMAND_CMD
    send_buf[1] = SPI_CHIP_ERASE_CMD
    hidDev.WriteHid(send_buf)
    Wait_Busy_Down(hidDev)
    return True

def CHIP_EXTERN_End(hidDev):
    RunStatu = True
    
    Id = Read_ID(hidDev)

    if Id == 0x001340C8 or Id == 0x001640C8:
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        CHIP_ENABLE_Command(hidDev)
        send_buf[0] = 0x3c
        Statu_Write(hidDev, SPI_STATU_WR_LOW_CMD, send_buf)
        send_buf[0] = 0x00
        Statu_Write(hidDev, SPI_STATU_WR_HIG_CMD, send_buf)
    elif Id == 0x001440E0 or Id == 0x001423C2:
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        CHIP_ENABLE_Command(hidDev)
        send_buf[0] = 0x3c
        send_buf[1] = 0x08
        Statu_Write(hidDev, SPI_STATU_WR_LOW_CMD, send_buf)
    elif Id == 0x001340E0 or Id == 0x001323C2:
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        CHIP_ENABLE_Command(hidDev)
        send_buf[0] = 0x3c
        send_buf[1] = 0x00
        Statu_Write(hidDev, SPI_STATU_WR_LOW_CMD, send_buf)
    elif Id == 0x00FFFFFF or Id == 0x0:
        RunStatu = False
    else:
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        CHIP_ENABLE_Command(hidDev)
        send_buf[0] = 0
        Statu_Write(hidDev, SPI_STATU_WR_LOW_CMD, send_buf)

    if RunStatu:
        time.sleep(0.5)

    return RunStatu