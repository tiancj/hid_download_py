import time
from .ExternDownloadFormatSPI import CHIP_EXTERN_Reset, CHIP_EXTERN_End
from ..hid_commands import RESET_ENABLE_PIN, WRITE_COMMAND_CMD, SOFT_SPI, HARD_SPI, DOWNLOAD_STATE, VPP_VCC_POWER_UPDATE

FT_MSG_SIZE_FLASH = 0x40

def CHIP_BK3435_Reset(spi_downloader, DownFormat):
    spi_downloader.ChipReset()
    send_buf = bytearray(150)
    for _ in range(150):
        send_buf[0] = 0xD2
        reply = spi_downloader.spi.xfer2(send_buf)

    time.sleep(0.1)

    return CHIP_EXTERN_Reset(spi_downloader)


def CHIP_BK3435_Start(*arg):
    return True

def CHIP_BK3435_End(hid_downloader):
    return CHIP_EXTERN_End(hid_downloader)

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



