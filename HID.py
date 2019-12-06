import hid
import time


debug = True

FT_MSG_SIZE_FLASH = 0x40

class HidDevice(object):
    def __init__(self, vid, pid):
        self.vid = vid
        self.pid = pid
        self.dev = hid.device()

    def Open(self):
        self.dev.open(self.vid, self.pid)

    def WriteHid(self, txBuffer):
        # outbuffer = bytearray(65)
        # # print(len(outbuffer))
        # outbuffer[1:1+len(txBuffer)] = txBuffer
        # # print(len(outbuffer))
        outbuffer = bytearray(64)
        outbuffer[:len(txBuffer)] = txBuffer
        if debug:
            print('TX: ', '00 ' + ''.join(['{:02X} '.format(i) for i in outbuffer]))
        # print("pre: ", time.time())
        ret = self.dev.write(outbuffer)
        # print("after: ", time.time())
        return ret

    def ReadHid(self, cnt=FT_MSG_SIZE_FLASH, timeout=1000):
        outbuf = self.dev.read(64, timeout)
        if debug:
            print('RX: ', '00 ' + ''.join(['{:02X} '.format(i) for i in outbuf]))
        # return outbuf[1:cnt+1]
        return outbuf[:cnt]
