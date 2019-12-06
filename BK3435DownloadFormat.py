from ExternDownloadFormat import CHIP_EXTERN_Reset, CHIP_EXTERN_End
from commands import *
FT_MSG_SIZE_FLASH = 0x40

def CHIP_BK3435_Reset(myhid):
    send_buf = bytearray(FT_MSG_SIZE_FLASH)
    send_buf[0] = RESET_ENABLE_PIN
    myhid.WriteHid(send_buf)

    # do {
    send_buf[0] = WRITE_COMMAND_CMD
    send_buf[1] = 0xD2
    myhid.WriteHid(send_buf)
    # while (time--) if WriteHid returns 0xFF

    CHIP_EXTERN_Reset(myhid)


def CHIP_BK3435_Start(*arg):
    return True

def CHIP_BK3435_End(myhid, Id):
    return CHIP_EXTERN_End(myhid, Id)

    

