# uart wrapper 
import serial
from .boot_protocol import *

class CBootIntf(object):
    def __init__(self):
        self.ser = serial.Serial(port, bps, timeout=timex)

    def Start_Cmd(self, txbuf, rxLen=0, timeout=10):
        self.ser.write(txbuf)
        if rxLen:
            rxbuf = self.ser.read(rxLen)
            if len(rxbuf) == rxLen:
                return rxbuf
        return None

    def WaitForRespond(self):
        pass

    def LinkCheck(self):
        txbuf = BuildCmd_LinkCheck()
        rxbuf = self.Start_Cmd(txbuf, CalcRxLength_LinkCheck())
        if not rxbuf:
            if CheckRespond_LinkCheck(rxbuf):
                return rxbuf
        return False

    def SetBR(self, baudrate):
        txbuf = BuildCmd_SetBaudRate(baudrate, 100)
        rxbuf = self.Start_Cmd(txbuf, CalcRxLength_SetBaudRate())
        if not rxbuf:
            if CheckRespond_SetBaudRate(rxbuf, baudrate, 100):
                return rxbuf
        return False

    def ReadSector(self, addr):
        txbuf = BuildCmd_FlashRead4K(addr)
        rxbuf = self.Start_Cmd(txbuf, CalcRxLength_FlashRead4K())
        if not rxbuf:
            if CheckRespond_FlashRead4K(rxbuf, addr):
                return rxbuf
        return False

    def EraseBlock(self, val, addr):
        txbuf = BuildCmd_FlashErase(addr, val)
        rxbuf = self.Start_Cmd(txbuf, CalcRxLength_FlashErase())
        if not rxbuf:
            if CheckRespond_FlashErase(rxbuf, addr, val):
                return rxbuf
        return False

    def WriteSector(self, addr, buf):
        txbuf = BuildCmd_FlashWrite4K(addr, buf)
        rxbuf = self.Start_Cmd(txbuf, CalcRxLength_FlashWrite4K())
        if not rxbuf:
            if CheckRespond_FlashWrite4K(txbuf, addr):
                return rxbuf
        return False


    def ReadCRC(self, start, end):
        txbuf = BuildCmd_CheckCRC(start, end)
        rxbuf = self.Start_Cmd(txbuf, CalcRxLength_CheckCRC)
        if not rxbuf:
            if CheckRespond_CheckCRC(txbuf, start, end):
                return rxbuf
        return False
