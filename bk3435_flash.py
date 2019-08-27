import base
import time
import struct


class BK3435Flash(base.FlashBase):
    def __init__(self, dev):
        super().__init__(dev)

        # Extern flash parameter
        self.erase_sector = 4*1024
        self.max_image_len = 2*1024*1024
        self.spi_div_clk = 0
        self.down_format = base.CHIP_BK7231U_FORMAT

    def reset(self):
        pass

    def start(self):
        pass

    def end(self):
        pass

    def erase(self):
        pass
