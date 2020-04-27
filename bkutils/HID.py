import hid
import time

debug = False

FT_MSG_SIZE_FLASH = 0x40

class HidDevice(object):

    """HID device Wrapper"""

    def __init__(self, vid=0x10c4, pid=0x0033, path=None):
        self.vid = vid
        self.pid = pid
        self.path = path
        self.dev = hid.device()

    def Open(self):
        if self.path:
            self.dev.open_path(self.path)
        else:
            self.dev.open(self.vid, self.pid)

    def WriteHid(self, txBuffer):
        """write txBuffer to hid device"""
        outbuffer = bytearray(64)
        outbuffer[:len(txBuffer)] = txBuffer
        if debug:
            print('TX: ', ''.join(['{:02X} '.format(i) for i in outbuffer]))
        return self.dev.write(outbuffer)

    def ReadHid(self, cnt=FT_MSG_SIZE_FLASH, timeout=1000):
        outbuf = self.dev.read(64, timeout)
        if debug:
            print('RX: ', ''.join(['{:02X} '.format(i) for i in outbuf]))
        return outbuf[:cnt]
