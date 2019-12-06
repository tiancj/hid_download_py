from ExternDownloadFormat import CHIP_EXTERN_Reset, CHIP_EXTERN_End
from commands import *
import time
FT_MSG_SIZE_FLASH = 0x40

def CHIP_BK3435_Reset(hidDev):
    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    send_buf[0] = RESET_ENABLE_PIN
    hidDev.WriteHid(send_buf)

    for i in range(150):
        send_buf[0] = WRITE_COMMAND_CMD
        send_buf[1] = 0xD2
        ret = hidDev.WriteHid(send_buf)

    time.sleep(0.1)

    return CHIP_EXTERN_Reset(hidDev)


def CHIP_BK3435_Start(*arg):
    return True

def CHIP_BK3435_End(hidDev):
    return CHIP_EXTERN_End(hidDev)

    

