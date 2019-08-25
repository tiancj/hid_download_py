import base
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

class ExternFlash(base.FlashBase):
    def __init__(self, dev):
        super(ExternFlashDownloader, self).__init__(dev)

        # Extern flash parameter
        self.erase_sector = 4*1024
        self.max_image_len = 2*1024*1024
        self.spi_div_clk = 0
        self.down_format = base.EXTERN_FLASH_FORMAT

    def reset(self):
        # CHIP_EXTERN_Reset
        chip_id = self.Read_ID()
        print('chip_id', chip_id)

        # for default chip id
        self.CHIP_ENABLE_Command()
        send_buf = bytearray(1)
        send_buf[0] = 0x00
        self.Statu_Write(SPI_STATU_WR_LOW_CMD, send_buf)

    def start(self):
        # Extern flash has no start
        pass

    def end(self):
        # CHIP_EXTERN_End
        chip_id = self.Read_ID()
        print('chip_id', chip_id)

        # for default chip id
        self.CHIP_ENABLE_Command()
        send_buf = bytearray(1)
        send_buf[0] = 0x3c
        self.Statu_Write(SPI_STATU_WR_LOW_CMD, send_buf)

    def Read_ID(self):
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        send_buf[0] = READ_FLASH_CMD
        send_buf[1] = SPI_ID_READ_CMD
        send_buf[5] = 0
        send_buf[6] = 3
        self.dev.WriteHid(send_buf)
        out_buf = self.dev.ReadHid(3)
        return out_buf

    def CHIP_ENABLE_Command(self):
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        send_buf[0] = WRITE_COMMAND_CMD
        send_buf[1] = SPI_CHIP_ENABLE_CMD
        self.dev.WriteHid(send_buf)
        # out_buf = self.dev.ReadHid(3)
        # return out_buf
        self.Wait_Busy_Down()

    def Wait_Busy_Down(self):
        while True:
            send_buf = bytearray(FT_MSG_SIZE_FLASH)
            send_buf[0] = READ_REG_CMD
            send_buf[1] = 0
            send_buf[2] = 5
            self.dev.WriteHid(send_buf)
            out_buf = self.dev.ReadHid(1)
            if not (out_buf[0] & 0x01):
                break
            time.sleep(0.1)

    def Statu_Write(self, cmd, cmdHead):
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        send_buf[0] = WRITE_FLASH_CMD
        send_buf[1] = cmd
        send_buf[5] = 0x0
        send_buf[6] = len(cmdHead)
        send_buf[7:7+len(cmdHead)+1] = cmdHead
        self.dev.WriteHid(send_buf)
        self.Wait_Busy_Down()

    def erase(self):
        # CHIP_EXTERN_Erase
        send_buf = bytearray(FT_MSG_SIZE_FLASH)
        send_buf[0] = WRITE_COMMAND_CMD
        send_buf[1] = SPI_CHIP_ERASE_CMD
        self.dev.WriteHid(send_buf)
        self.Wait_Busy_Down()
