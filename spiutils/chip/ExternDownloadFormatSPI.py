import time
import struct
from ..hid_commands import *

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
SPI_READ_REG        	= 0x05

def Wait_Busy_Down(spi):
    while True:
        send_buf = bytearray(2)
        send_buf[0] = SPI_READ_REG
        send_buf[1] = 0x00
        out_buf = spi.xfer2(send_buf)
        if not (out_buf[1] & 0x01):
            break
        time.sleep(0.01)

def Read_ID(spi):
    send_buf = bytearray(4)
    send_buf[0] = SPI_ID_READ_CMD
    send_buf[1] = 0x00
    send_buf[2] = 0x00
    send_buf[3] = 0x00
    out_buf = spi.xfer2(send_buf)
    flash_id = out_buf[1:4]
    flash_id.append(0)
    flash_id = bytes(flash_id)
    flash_id = struct.unpack('<I', flash_id[0:4])[0]
    return flash_id

def CHIP_ENABLE_Command(spi):
    send_buf = bytearray(1)
    send_buf[0] = SPI_CHIP_ENABLE_CMD
    spi.xfer(send_buf)
    Wait_Busy_Down(spi)

def Statu_Write(spi, cmd, cmdHead):
    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    send_buf[0] = cmd
    send_buf[1:len(cmdHead)+1] = cmdHead
    spi.xfer(send_buf)
    Wait_Busy_Down(spi)

def CHIP_EXTERN_Reset(spi_downloader, *args):
    spi = spi_downloader.spi
    RunStatu = True

    Id = Read_ID(spi)
    # print("flash_id: {:X}".format(Id))

    if Id == 0x001340C8 or Id == 0x001640C8:
        send_buf = bytearray(1)
        CHIP_ENABLE_Command(spi)
        send_buf[0] = 0
        Statu_Write(spi, SPI_STATU_WR_LOW_CMD, send_buf)
        send_buf[0] = 0
        Statu_Write(spi, SPI_STATU_WR_HIG_CMD, send_buf)
    elif Id == 0x001440E0 or Id == 0x001423C2:
        send_buf = bytearray(2)
        CHIP_ENABLE_Command(spi)
        send_buf[0] = 0x00
        send_buf[1] = 0x08
        Statu_Write(spi, SPI_STATU_WR_LOW_CMD, send_buf)
    elif Id == 0x001340E0 or Id == 0x001323C2:
        send_buf = bytearray(2)
        CHIP_ENABLE_Command(spi)
        send_buf[0] = 0x00
        send_buf[1] = 0x00
        Statu_Write(spi, SPI_STATU_WR_LOW_CMD, send_buf)
    elif Id == 0x00FFFFFF or Id == 0x0:
        RunStatu = False
    else:
        send_buf = bytearray(1)
        CHIP_ENABLE_Command(spi)
        send_buf[0] = 0
        Statu_Write(spi, SPI_STATU_WR_LOW_CMD, send_buf)

    if RunStatu:
        time.sleep(0.5)

    return RunStatu

def CHIP_EXTERN_Erase(spi_downloader):
    spi = spi_downloader.spi
    CHIP_ENABLE_Command(spi)
    send_buf = bytearray(1)
    send_buf[0] = SPI_CHIP_ERASE_CMD
    spi.xfer(send_buf)
    Wait_Busy_Down(spi)
    return True

def CHIP_EXTERN_End(spi_downloader):
    spi = spi_downloader.spi
    RunStatu = True

    Id = Read_ID(spi)

    if Id == 0x001340C8 or Id == 0x001640C8:
        send_buf = bytearray(1)
        CHIP_ENABLE_Command(spi)
        send_buf[0] = 0x3c
        Statu_Write(spi, SPI_STATU_WR_LOW_CMD, send_buf)
        send_buf[0] = 0x00
        Statu_Write(spi, SPI_STATU_WR_HIG_CMD, send_buf)
    elif Id == 0x001440E0 or Id == 0x001423C2:
        send_buf = bytearray(2)
        CHIP_ENABLE_Command(spi)
        send_buf[0] = 0x3c
        send_buf[1] = 0x08
        Statu_Write(spi, SPI_STATU_WR_LOW_CMD, send_buf)
    elif Id == 0x001340E0 or Id == 0x001323C2:
        send_buf = bytearray(2)
        CHIP_ENABLE_Command(spi)
        send_buf[0] = 0x3c
        send_buf[1] = 0x00
        Statu_Write(spi, SPI_STATU_WR_LOW_CMD, send_buf)
    elif Id == 0x00FFFFFF or Id == 0x0:
        RunStatu = False
    else:
        send_buf = bytearray(1)
        CHIP_ENABLE_Command(spi)
        send_buf[0] = 0
        Statu_Write(spi, SPI_STATU_WR_LOW_CMD, send_buf)

    if RunStatu:
        time.sleep(0.5)

    return RunStatu