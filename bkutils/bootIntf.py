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
from serial import Timeout
from .boot_protocol import *
import binascii
import time

debug = False

RECV_HEAD = 0
RECV_BODY = 1

class CBootIntf(object):
    '''
    XXX: This class is timing sensitive.
    '''
    def __init__(self, port, baudrate, timeout):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self._state = RECV_HEAD

    def Start_Cmd(self, txbuf, rxLen=0, timeout=0.05):
        if debug:
            # print("TX: ", binascii.b2a_hex(txbuf if len(txbuf) < 16 else txbuf[:16], b' '))
            print("TX: ", binascii.b2a_hex(txbuf, b' '))
        self.rxLen = rxLen
        if debug:
            print("tx start: ", time.time())
        self.ser.write(txbuf)
        if debug:
            print("tx end: ", time.time())

        if rxLen:
            if debug:
                print("read start: ", time.time())

            rxbuf = self.WaitForRespond(rxLen, timeout)
            if debug and rxbuf:
                print("read end: ", time.time())
                print('RX1: ', binascii.b2a_hex(rxbuf, b' '))
                print('RXS: ', rxbuf)
            # if rxbuf and (len(rxbuf) == rxLen):
            #   return rxbuf
            return rxbuf
        return None

    def Drain(self):
        # self.ser.timeout = 0.01
        self.ser.read(1024)

    def Read(self):
        return self.ser.read(1024)

    # 04 0e 05 01 e0 fc 01 00
    # 04 0e ff 01 e0 fc f4 07 00 0f 00 20 00 c0 03 00
    def WaitForRespond(self, rxLen, timeout):
        timeout = Timeout(timeout)
        read_buf = b''
        state = RECV_HEAD

        while not timeout.expired():
            buf = self.ser.read(1024)
            if debug:
                print('RX1: ', binascii.b2a_hex(buf, b' '))
            if state == RECV_HEAD:
                while buf:
                    pos = buf.find(b'\x04')
                    if pos < 0:
                        buf = None
                        break
                    buf = buf[pos:]
                    if len(buf) >= 7: # minimal len
                        if buf[0:2] == b'\x04\x0e' and buf[3:6] == b'\x01\xe0\xfc': # maybe a valid rx packet
                            read_buf += buf
                            state = RECV_BODY
                            break
                    buf = buf[1:] # forward to next
            if state == RECV_BODY:
                break
        read_buf = buf
        if debug and read_buf:
            print("RDBUF:", read_buf)
        return read_buf
        # return None

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
        self.Start_Cmd(txbuf, 0, 0.05)   # 
        time.sleep(delay/1000/2)
        self.ser.baudrate = baudrate
        rxbuf = self.WaitForRespond(CalcRxLength_SetBaudRate(), 0.5)
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
        rxbuf = self.Start_Cmd(txbuf, CalcRxLength_FlashErase(), 1)
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
        rxbuf = self.Start_Cmd(txbuf, CalcRxLength_CheckCRC, 1)
        if rxbuf:
            return CheckRespond_CheckCRC(rxbuf, start, end)
        return False,0
