# encoding: utf8

FLASH_ID_XTX_25F08B=0x14405e        # 芯天下flash,w+v:6.5s,e+w+v:11.5s
FLASH_ID_MXIC_25V8035F=0x1423c2     # 旺宏flash,w+v:8.2s,e+w+v:17.2s
FLASH_ID_XTX_25F04B=0x13311c        # 芯天下flash-4M
FLASH_ID_GD_25D40=0x134051          # GD flash-4M,w+v:3.1s,e+w+v:5.1s
FLASH_ID_GD_25D80=0x144051          # GD flash-8M，e+w+v=9.8s
FLASH_ID_GD_1_25D80=0x1440C8        # GD flash-8M，
FLASH_ID_Puya_25Q80=0x146085        # puya 8M,w+v:10.4s,e+w+v:11.3s,新版e+w+v：8.3s
FLASH_ID_Puya_25Q40=0x136085        # puya 4M,e+w+v:6s，新版w+v=4s，e+w+v=4.3s
FLASH_ID_Puya_25Q32H=0x166085       # puya 32M******暂时只用于脱机烧录器上7231的外挂flash
FLASH_ID_GD_25Q16=0x001540c8        # GD 16M******暂时只用于脱机烧录器上7231的外挂flash
FLASH_ID_GD_25Q16B=0x001540c8       # GD 16M******暂时只用于脱机烧录器上7231的外挂flash
FLASH_ID_XTX_25F16B=0x15400b        # XTX 16M
FLASH_ID_XTX_25F32B	=0x0016400b     # xtx 32M******暂时只用于脱机烧录器上7231的外挂flash

FLASH_ID_MXIC_25V4035F=0x1323c2     # 旺宏flash,w+v:8.2s,e+w+v:17.2s
FLASH_ID_MXIC_25V1635F=0x1523c2     # 旺宏flash,w+v:8.2s,e+w+v:17.2s
FLASH_ID_GD_25Q41B=0x1340c8         # GD flash-4M,w+v:3.1s,e+w+v:5.1s
FLASH_ID_BY_PN25Q80A=0x1440e0       # GD flash-4M,w+v:3.1s,e+w+v:5.1s
FLASH_ID_BY_PN25Q40A=0x1340e0       # GD flash-4M,w+v:3.1s,e+w+v:5.1s

FLASH_ID_XTX_25Q64B	=0x0017600b     # xtx 64M******暂时只用于脱机烧录器上7231的外挂flash
FLASH_ID_XTX_25F64B	=0x0017400b     # xtx 64M******暂时只用于脱机烧录器上7231的外挂flash
FLASH_ID_Puya_25Q64H=0x00176085
FLASH_ID_GD_25Q64=0x001740c8
FLASH_ID_WB_25Q128JV=0x001840ef
FLASH_ID_ESMT_25QH16B=0x0015701c
FLASH_ID_GD_25WQ64E=0x001765c8
FLASH_ID_GD_25WQ32E=0x001665c8
FLASH_ID_GD_25WQ16E=0x001565c8
FLASH_ID_TH25Q_16HB = 0x001560eb
FLASH_ID_TH25Q_80HB = 0x001460cd
FLASH_ID_NA = 0x001640c8

FLASH_ID_UNKNOWN=-1

class FlashInt:
    def __init__(self, mid, icNam, manName, szMem, szSR,
            cwUnp, cwEnp, cwMsk, sb, lb, cwdRd, cwdWr):
        self.mid = mid
        self.icNam = icNam
        self.manName = manName
        self.szMem = szMem
        self.szSR = szSR
        self.cwUnp = cwUnp
        self.cwEnp = cwEnp
        self.cwMsk = cwMsk
        self.sb = sb
        self.lb = lb
        self.cwdRd = cwdRd
        self.cwdWr = cwdWr

    def __str__(self):
        return f"mid: {self.mid}, name: {self.icNam}, manufactor: {self.manName}, size: {self.szMem}"

def BFD(v,bs,bl):
    return (v&((1<<(bl))-1))<<(bs)

def BIT(n):
    return 1<<n

tblFlashInt = [
    #        MID                      IC Name         manufactor     size        # SR  unprot    prot       mask                  sb    length
    FlashInt(FLASH_ID_XTX_25F08B,     "PN25F08B",     "xtx",      8 *1024*1024,   1,    0x00,    0x07,   BFD(0x0f,2,4),           2,    4,    [0x05,0xff,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_XTX_25F04B,     "PN25F04B",     "xtx",      4 *1024*1024,   1,    0x00,    0x07,   BFD(0x0f,2,4),           2,    4,    [0x05,0xff,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_GD_25D40,       "GD25D40",      "GD",       4 *1024*1024,   1,    0x00,    0x07,   BFD(0x0f,2,3),           2,    3,    [0x05,0xff,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_GD_25D80,       "GD25D80",      "GD",       8 *1024*1024,   1,    0x00,    0x07,   BFD(0x0f,2,3),           2,    3,    [0x05,0xff,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_GD_1_25D80,     "GD25D80",      "GD",       8 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_Puya_25Q80,     "P25Q80",       "Puya",     8 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_Puya_25Q40,     "P25Q40",       "Puya",     4 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_Puya_25Q32H,    "P25Q32H",      "Puya",    32 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_Puya_25Q64H,    "P25Q64H",      "Puya",    64 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_XTX_25F16B,     "XT25F16B",     "xtx",     16 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_GD_25Q16B,      "GD25Q16B",     "GD",      16 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_MXIC_25V8035F,  "MX25V8035F",   "WH",       8 *1024*1024,   2,    0x00,    0x07,   BIT(12)|BFD(0x1f,2,4),   2,    5,    [0x05,0x15,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_MXIC_25V1635F,  "MX25V1635F",   "WH",      16 *1024*1024,   2,    0x00,    0x07,   BIT(12)|BFD(0x1f,2,4),   2,    5,    [0x05,0x15,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_XTX_25F32B,     "XT25F32B",     "xtx",     32 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_GD_25Q41B,      "GD25Q41B",     "GD",       4 *1024*1024,   1,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,3),   2,    3,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_BY_PN25Q40A,    "PN25Q40A",     "BY",       4 *1024*1024,   1,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,3),   2,    3,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_BY_PN25Q80A,    "PN25Q80A",     "BY",       8 *1024*1024,   1,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,3),   2,    3,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_XTX_25F64B,     "XT25F64B",     "xtx",     64 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_XTX_25Q64B,     "XT25Q64B",     "xtx",     64 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_WB_25Q128JV,    "WB25Q128JV",   "WB",     128 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_ESMT_25QH16B,   "EN25QH16B",    "ESMT",    16 *1024*1024,   1,    0x00,    0x07,   BFD(0xf,2,5),            2,    4,    [0x05,0xff,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_TH25Q_16HB,     "TH25Q_16HB",   "TH",      16 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_TH25Q_80HB,     "TH25Q_80HB",   "TH",       8 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_NA,             "NA_NA",        "NA",      32 *1024*1024,   1,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_GD_25WQ16E,     "GD25WQ16E",    "GD",      16 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_GD_25WQ32E,     "GD25WQ32E",    "GD",      32 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
    FlashInt(FLASH_ID_GD_25WQ64E,     "GD25WQ64E",    "GD",      64 *1024*1024,   2,    0x00,    0x07,   BIT(14)|BFD(0x1f,2,5),   2,    5,    [0x05,0x35,0xff,0xff],   [0x01,0xff,0xff,0xff]),
]


def GetFlashInfo(mid:int):
    for item in tblFlashInt:
        if item.mid == mid:
            return item
    return None