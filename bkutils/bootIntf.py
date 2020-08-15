# encoding: utf8
#
# UART Download Tool
#
# Copyright (c) BekenCorp. (chunjian.tian@bekencorp.com).  All rights reserved.
#
# This software may be distributed under the terms of the BSD license.
# See README for more details.

# uart wrapper 
import serial
from .boot_protocol import *
import binascii
import time

debug = False

class CBootIntf(object):
    def __init__(self, port, baudrate, timeout):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def Start_Cmd(self, txbuf, rxLen=0, timeout=0.1):
        if debug:
            print("TX: ", binascii.b2a_hex(txbuf if len(txbuf) < 16 else txbuf[:16], b' '))
        self.ser.timeout = timeout
        self.ser.write(txbuf)
        if True:
            rxbuf = self.ser.read(1024)
            if debug:
                print('RX1: ', binascii.b2a_hex(rxbuf, b' '))
            # print('RXS: ', rxbuf)
            # if rxbuf and (len(rxbuf) == rxLen):
            #   return rxbuf
            return rxbuf
        return None

    def Drain(self):
        self.ser.timeout = 0.1
        self.ser.read(1024)

    def WaitForRespond(self):
        pass

    def LinkCheck(self):
        txbuf = BuildCmd_LinkCheck()
        rxbuf = self.Start_Cmd(txbuf, CalcRxLength_LinkCheck(), 0.001)
        if rxbuf:
            # print('RX2: ', binascii.b2a_hex(rxbuf, b' '))
            if CheckRespond_LinkCheck(rxbuf):
                return True
        return False

    def SetBR(self, baudrate, delay):
        txbuf = BuildCmd_SetBaudRate(baudrate, delay)
        rxbuf = self.Start_Cmd(txbuf, CalcRxLength_SetBaudRate())
        self.ser.baudrate = baudrate
        time.sleep(delay/1000)
        if not rxbuf:
            rxbuf = self.ser.read(1024)
            # print('RX3: ', binascii.b2a_hex(rxbuf, b' '))
        if rxbuf:
            if CheckRespond_SetBaudRate(rxbuf, baudrate, delay):
                return True
        return False

    def ReadSector(self, addr):
        txbuf = BuildCmd_FlashRead4K(addr)
        rxbuf = self.Start_Cmd(txbuf, CalcRxLength_FlashRead4K())
        if rxbuf:
            ret, _, data = CheckRespond_FlashRead4K(rxbuf, addr)
            if ret:
                return data
        return None

    def EraseBlock(self, val, addr):
        txbuf = BuildCmd_FlashErase(addr, val)
        rxbuf = self.Start_Cmd(txbuf, CalcRxLength_FlashErase())
        if rxbuf:
            ret, _ = CheckRespond_FlashErase(rxbuf, addr, val)
            if ret:
                return True
        return False

    def WriteSector(self, addr, buf):
        txbuf = BuildCmd_FlashWrite4K(addr, buf)
        rxbuf = self.Start_Cmd(txbuf, CalcRxLength_FlashWrite4K())
        if rxbuf:
            ret, _ = CheckRespond_FlashWrite4K(rxbuf, addr)
            if ret:
                return True
        return False

    def ReadCRC(self, start, end):
        '''
        Read crc of flash region from @start to @end

        return (True_or_False, crc)
        '''
        txbuf = BuildCmd_CheckCRC(start, end)
        rxbuf = self.Start_Cmd(txbuf, CalcRxLength_CheckCRC)
        if rxbuf:
            return CheckRespond_CheckCRC(rxbuf, start, end)
        return False,0
