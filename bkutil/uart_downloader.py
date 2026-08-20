# encoding: utf8
#
# UART Download Tool
#
# Copyright (c) BekenCorp. (chunjian.tian@bekencorp.com).  All rights reserved.
#
# This software may be distributed under the terms of the BSD license.
# See README for more details.

import time
from .boot_intf import CBootIntf
try:
    from serial import Timeout
except ImportError:
    from serial.serialutil import Timeout
import binascii
from tqdm import tqdm
from .flash_list import *
from .crc32v2 import *

debug = False
STATUS_WIDTH = 16
STATUS_PAD = '\u00a0'

class UartDownloader(object):
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, unprotect=False, verbose=False):
        self.bootItf = CBootIntf(port, 115200, 0.001)
        self.target_baudrate = baudrate
        self.unprotect = unprotect
        self.verbose = verbose
        self.pbar = None
        self._pbar_total = 0
        self._mid = None

    def _pad_status(self, text):
        text = str(text)
        if len(text) >= STATUS_WIDTH:
            return text[:STATUS_WIDTH]
        return text + STATUS_PAD * (STATUS_WIDTH - len(text))

    def log(self, text, bar_desc=True, refresh=None):
        if not self.pbar:
            print(text)
            return
        text = str(text)
        if not bar_desc or len(text) > STATUS_WIDTH:
            self.pbar.write(text)
            return
        if refresh is None:
            refresh = True
        self.pbar.set_description_str(self._pad_status(text), refresh=refresh)

    def _make_pbar(self, total, status=''):
        return tqdm(
            total=total,
            desc=self._pad_status(status),
            ascii=True,
            ncols=80,
            dynamic_ncols=False,
            unit_scale=False,
            bar_format='{desc} : |{bar:24}| {percentage:3.0f}% [{elapsed}<{remaining}]',
        )

    def _ensure_pbar(self, status=''):
        if self.pbar is None and self._pbar_total > 0:
            self.pbar = self._make_pbar(self._pbar_total, status)

    def _estimate_pbar_total(self, byte_len, partitions=1):
        sectors = max(1, byte_len // 0x1000)
        # erase may include extra alignment sectors beyond payload size
        return sectors * 2 + 32 * partitions

    def do_reset_signal(self):
        self.bootItf.ser.dtr = 0
        self.bootItf.ser.rts = 1
        time.sleep(0.2)
        self.bootItf.ser.rts = 0

    def _prepare_file_data(self, pfile):
        fileLen = filOLen = len(pfile)
        padding_len = 0x100 - (fileLen & 0xff)
        if padding_len:
            pfile += b'\xff' * padding_len
            fileLen += padding_len
            filOLen += padding_len
        fileCrc = crc32_ver2(0xffffffff, pfile)
        return pfile, fileLen, filOLen, fileCrc

    def _connect(self):
        self._ensure_pbar("Getting Bus...")
        timeout = Timeout(10)
        self.do_reset_signal()

        count = 0
        self.bootItf.SendBkRegReboot()
        while True:
            r = self.bootItf.LinkCheck()
            if r:
                break
            if timeout.expired():
                self.log('Cannot get bus.')
                return False
            count += 1
            if count > 20:
                self.bootItf.SendBkRegReboot()
                if self.bootItf.ser.baudrate == 115200:
                    self.bootItf.ser.baudrate = 921600
                elif self.bootItf.ser.baudrate == 921600:
                    self.bootItf.ser.baudrate = 115200
                self.bootItf.Start_Cmd(b"reboot\r\n")
                if self.bootItf.ser.baudrate != 115200:
                    self.bootItf.ser.baudrate = 115200
                count = 0

        self.log("Gotten Bus...")
        time.sleep(0.01)
        self.bootItf.Drain()

        if self.target_baudrate != 115200:
            if not self.bootItf.SetBR(self.target_baudrate, 20):
                self.log("Set baudrate failed")
                return False
            self.log("Set baudrate OK")

        if self.unprotect:
            self._mid = self.bootItf.GetFlashMID()
            if self._Do_Boot_ProtectFlash(self._mid, True) != 1:
                self.log("Unprotect Failed")
                return False
        return True

    def _pbar_step(self, step=1):
        if not self.pbar:
            return
        remaining = self.pbar.total - self.pbar.n
        if remaining > 0:
            self.pbar.update(min(step, remaining))
            self.pbar.refresh()

    def _complete_pbar(self):
        if not self.pbar:
            return
        self.pbar.n = self.pbar.total
        self.pbar.refresh()

    def _finalize(self, success=True):
        if self.unprotect and self._mid is not None:
            self._Do_Boot_ProtectFlash(self._mid, False)
        if success:
            self._complete_pbar()
            self.log("Write OK")
            if self.pbar:
                self.pbar.refresh()
            for _ in range(3):
                time.sleep(0.01)
                self.bootItf.SendReboot()
        if self.pbar:
            self.pbar.close()
            self.pbar = None

    def _erase_block(self, cmd, addr, retry=1):
        self._ensure_pbar()
        for attempt in range(retry):
            if self.bootItf.EraseBlock(cmd, addr):
                self._pbar_step(16 if cmd == 0xd8 else 1)
                return True
            if attempt + 1 < retry:
                time.sleep(0.05)
        return False

    def _program_data(self, pfile, startAddr, fileLen=None, fileCrc=None):
        if fileLen is None or fileCrc is None:
            pfile, fileLen, filOLen, fileCrc = self._prepare_file_data(pfile)
        else:
            filOLen = fileLen

        eraseAddr = startAddr
        ss = s0 = eraseAddr & 0xfffff000
        filSPtr = 0

        if eraseAddr & 0xfff:
            self.log("Aligning...")
            buf = self.bootItf.ReadSector(s0)
            l = 0x1000 - (eraseAddr & 0xfff)
            fl = l if l < fileLen else fileLen
            buf[eraseAddr & 0xfff:eraseAddr & 0xfff + fl] = pfile[:fl]
            if not self._erase_block(0x20, s0):
                self.log("EraseBlock Failed")
                return False
            if not self.bootItf.WriteSector(s0, buf):
                self.log("WriteSector Failed")
                return False
            filOLen -= fl
            filSPtr = fl
            s0 += 0x1000
            ss = s0
            if filOLen <= 0:
                return self._verify_crc(startAddr, fileLen, fileCrc)

        filEPtr = fileLen
        s1 = eraseAddr + fileLen
        if s1 & 0xfff:
            buf = bytearray(b'\xff' * 4096)
            buf[:s1 & 0xfff] = pfile[filEPtr - (s1 & 0xfff):]
            if not self._erase_block(0x20, s1 & 0xfffff000, retry=4):
                self.log("EraseBlock Failed")
                return False
            if not self.bootItf.WriteSector(s1 & 0xfffff000, buf):
                self.log("WriteSector Failed")
                return False
            filEPtr = filEPtr - (s1 & 0xfff)
            filOLen = filOLen - (s1 & 0xfff)

        len1 = ss + filOLen
        len0 = s0 & 0xffff0000
        if s0 & 0xffff:
            len0 += 0x10000
        if filOLen > len0 - s0:
            while s0 < len0:
                if not self._erase_block(0x20, s0):
                    self.log("EraseBlock Failed")
                    return False
                s0 += 0x1000

        len1 = ss + filOLen
        self.log("Erasing")
        while s0 < len1:
            rmn = len1 - s0
            if rmn > 0x10000:
                if not self._erase_block(0xd8, s0):
                    self.log("EraseBlock Failed")
                    return False
                s0 = s0 + 0x10000
            else:
                if not self._erase_block(0x20, s0):
                    self.log("EraseBlock Failed")
                    return False
                s0 = s0 + 0x1000

        self.log("Writing")
        i = 0
        while i < filOLen:
            for _ in range(4):
                if self.bootItf.WriteSector(ss + i, pfile[filSPtr + i:filSPtr + i + 4 * 1024]):
                    self._pbar_step(1)
                    break
            else:
                self.log("WriteSector Failed")
                return False
            i += 0x1000

        return self._verify_crc(startAddr, fileLen, fileCrc)

    def _verify_crc(self, startAddr, fileLen, fileCrc):
        self.log("CRC verify")
        if fileLen & 0xff:
            l2 = (fileLen & ~0xff) + 0x100
        else:
            l2 = fileLen
        crcTo = fileLen * 15 / 1024 / 1024
        if crcTo < 15:
            crcTo = 15
        ret, crc = self.bootItf.ReadCRC(startAddr, startAddr + l2 - 1, crcTo)
        if not ret:
            self.log("Read CRC Failed")
            return False
        if crc != fileCrc:
            self.log("CRC not equal")
            return False
        return True

    def programm(self, filename, startAddr=0x11000):
        with open(filename, "rb") as f:
            pfile = f.read()
        _, _, filOLen, _ = self._prepare_file_data(pfile)
        self._pbar_total = self._estimate_pbar_total(filOLen)
        self.pbar = None
        if not self._connect():
            self._finalize(success=False)
            return
        success = self._program_data(pfile, startAddr)
        self._finalize(success=success)

    def program_bin_list(self, bin_list):
        byte_len = sum(item.iFileLength for item in bin_list)
        self._pbar_total = self._estimate_pbar_total(byte_len, len(bin_list))
        self.pbar = None
        if not self._connect():
            self._finalize(success=False)
            return
        success = True
        for idx, bin_info in enumerate(bin_list):
            if not bin_info.bDataPort:
                if self.verbose:
                    self.log(f"[{idx}] skip cbus @0x{bin_info.iStartAddress:x}", bar_desc=False)
                continue
            if self.verbose:
                self.log(
                    f"[{idx}] start: 0x{bin_info.iStartAddress:x}, length: 0x{bin_info.iFileLength:x}",
                    bar_desc=False,
                )
            if not self._program_data(
                bin_info.pfile,
                bin_info.iStartAddress,
                bin_info.iFileLength,
                bin_info.iFileCRC,
            ):
                success = False
                break
        self._finalize(success=success)

    def _Do_Boot_ProtectFlash(self, mid:int, unprotect:bool):
        # 1. find flash info
        flash_info = GetFlashInfo(mid)
        if flash_info is None:
            return -1
        if debug:
            print(flash_info.icNam, flash_info.manName)

        timeout = Timeout(1)

        # 2. write (un)protect word
        cw = flash_info.cwUnp if unprotect else flash_info.cwEnp
        while True:
            sr = 0

            # read sr register
            for i in range(flash_info.szSR):
                f = self.bootItf.ReadFlashSR(flash_info.cwdRd[i])
                if f[0]:
                    sr |= f[2] << (8 * i)
                    if debug: print("sr: {:x}".format(sr))

            if debug:
                print("final sr: {:x}".format(sr))
                print("msk: {:x}".format(flash_info.cwMsk))
                print("cw: {:x}, sb: {}, lb: {}".format(cw, flash_info.sb, flash_info.lb))
                print("bfd: {:x}".format(BFD(cw, flash_info.sb, flash_info.lb)))

            # if (un)protect word is set
            if (sr & flash_info.cwMsk) == BFD(cw, flash_info.sb, flash_info.lb):
                return 1
            if timeout.expired():
                return -2
            # // set (un)protect word
            srt = sr & (flash_info.cwMsk ^ 0xffffffff)
            srt |= BFD(cw, flash_info.sb, flash_info.lb)
            f = self.bootItf.WriteFlashSR(flash_info.szSR, flash_info.cwdWr[0], srt & 0xffff)

            time.sleep(0.01)

        return 1

    def chip_erase(self):
        self._pbar_total = 100
        self.pbar = None
        if not self._connect():
            self._finalize(success=False)
            return

        self.log("Erasing")
        self.pbar.update(99)
        self.bootItf.EraseAllFlash()

        if self.unprotect:
            self._Do_Boot_ProtectFlash(self._mid, False)
        self.log("Chip Erase Done")
        self.pbar.update(1)

        for _ in range(3):
            time.sleep(0.01)
            self.bootItf.SendReboot()

        self.pbar.close()
        self.pbar = None

if __name__ == '__main__':
    downloader = UartDownloader()
