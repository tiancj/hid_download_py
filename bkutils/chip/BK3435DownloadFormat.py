import time
from .ExternDownloadFormat import CHIP_EXTERN_Reset, CHIP_EXTERN_End
from ..commands import RESET_ENABLE_PIN, WRITE_COMMAND_CMD, SOFT_SPI, HARD_SPI, DOWNLOAD_STATE, VPP_VCC_POWER_UPDATE
from ..ManageChipList import EXTERN_FLASH_FORMAT

FT_MSG_SIZE_FLASH = 0x40

def CHIP_BK3435_Reset(hidDev, spi_mode=SOFT_SPI, DownFormat=EXTERN_FLASH_FORMAT):
    if spi_mode == HARD_SPI:
        ChangeInterface(hidDev, DownFormat)

    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    send_buf[0] = RESET_ENABLE_PIN
    hidDev.WriteHid(send_buf)

    for _ in range(150):
        send_buf[0] = WRITE_COMMAND_CMD
        send_buf[1] = 0xD2
        hidDev.WriteHid(send_buf)

    time.sleep(0.1)

    return CHIP_EXTERN_Reset(hidDev)


def CHIP_BK3435_Start(*arg):
    return True

def CHIP_BK3435_End(hidDev):
    return CHIP_EXTERN_End(hidDev)

def ChangeInterface(hidDev, DownFormat):
    send_buf = bytearray(5)
    send_buf[0] = VPP_VCC_POWER_UPDATE
    send_buf[1] = DOWNLOAD_STATE
    send_buf[2] = HARD_SPI
    send_buf[3] = 100
    send_buf[4] = DownFormat
    hidDev.WriteHid(send_buf)

    out_buf = hidDev.ReadHid(1)
    if out_buf[0] != 0xEE:
        print("Vpp打开失败！")
        return False

    return True



