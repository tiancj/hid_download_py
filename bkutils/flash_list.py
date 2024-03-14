# encoding: utf8

FLASH_ID_XTX_25F08B			=0x14405e,#芯天下flash,w+v:6.5s,e+w+v:11.5s
FLASH_ID_XTX_25F04B			=0x13311c,#芯天下flash-4M
FLASH_ID_XTX_25F16B			= 0x15400b,#XTX 16M
FLASH_ID_XTX_25F32B			= 0x0016400b,#xtx 32M******暂时只用于脱机烧录器上7231的外挂flash
FLASH_ID_XTX_25Q64B			= 0x0017600b,#xtx 64M******暂时只用于脱机烧录器上7231的外挂flash
FLASH_ID_XTX_25F64B			= 0x0017400b,#xtx 64M******暂时只用于脱机烧录器上7231的外挂flash
FLASH_ID_XTX_25Q128B			= 0x0018600b,#xtx 128M
FLASH_ID_XTX_25F128F			= 0x0018400b,#xtx 128M

FLASH_ID_GT25Q16B				= 0x1560C4,#聚辰16M-Bits

FLASH_ID_MXIC_25V8035F		= 0x1423c2,#旺宏flash,w+v:8.2s,e+w+v:17.2s
FLASH_ID_MXIC_25V4035F		= 0x1323c2,#旺宏flash,w+v:8.2s,e+w+v:17.2s
FLASH_ID_MXIC_25V1635F		= 0x1523c2,#旺宏flash,w+v:8.2s,e+w+v:17.2s

FLASH_ID_GD_25D40				=0x134051,#GD flash-4M,w+v:3.1s,e+w+v:5.1s
FLASH_ID_GD_25D80				=0x144051,#GD flash-8M，e+w+v=9.8s
FLASH_ID_GD_1_25D80			=0x1440C8,#GD flash-8M，
FLASH_ID_GD_25WD80E			= 0x1464C8,#GD flash-8M，
FLASH_ID_GD_25WQ64E			= 0x001765c8,
FLASH_ID_GD_25WQ32E			= 0x001665c8,
FLASH_ID_GD_25WQ16E			= 0x001565c8,
FLASH_ID_GD_25Q64				= 0x001740c8,
FLASH_ID_GD_25Q16B			= 0x001540c8,#GD 16M******暂时只用于脱机烧录器上7231的外挂flash
FLASH_ID_GD_25Q41B            = 0x1340c8,#GD flash-4M,w+v:3.1s,e+w+v:5.1s
FLASH_ID_GD_25Q41B_T			=	0x1364c8,#GD flash-4M,w+v:3.1s,e+w+v:5.1s
FLASH_ID_GD_25LQ128E			= 0x1860c8,#media
FLASH_ID_GD_25WQ128E		= 0x1865c8,#media
FLASH_ID_GD25LX256E			= 0x1968C8,

FLASH_ID_Puya_25Q16HB_K	= 0x152085,
FLASH_ID_Puya_25Q40			= 0x136085,#puya 4M,e+w+v:6s，新版w+v=4s，e+w+v=4.3s 普冉
FLASH_ID_Puya_25Q64H			= 0x176085,
FLASH_ID_Puya_25Q80			= 0x146085,#puya 8M,w+v:10.4s,e+w+v:11.3s,新版e+w+v：8.3s
FLASH_ID_Puya_25Q80_38		= 0x154285,#puya 16M
FLASH_ID_Puya_25Q32H			= 0x166085,#puya 32M******暂时只用于脱机烧录器上7231的外挂flash
FLASH_ID_Puya_25Q16SU		= 0x156085,#puya 16M
FLASH_ID_Puya_25Q128HA	= 0x182085,#puya 128M

FLASH_ID_BY_PN25Q80A		=0x1440e0,#GD flash-4M,w+v:3.1s,e+w+v:5.1s
FLASH_ID_BY_PN25Q40A		=0x1340e0,#GD flash-4M,w+v:3.1s,e+w+v:5.1s

FLASH_ID_WB_25Q128JV		= 0x001840ef,

FLASH_ID_DS_ZB25LQ128C		=0x0018505e,

FLASH_ID_ESMT_25QH16B		=0x0015701c,
FLASH_ID_ESMT_25QE32A		=0x0016411c,
FLASH_ID_ESMT_25QW32A	=0x0016611c,

FLASH_ID_TH25Q_16HB			=0x001560eb,
FLASH_ID_TH25Q_80HB         = 0x001460cd,
FLASH_ID_TH25D_40HB			= 0x001360cd,

FLASH_ID_XM25QU128C        =0x00184120,

FLASH_ID_NA = 0x001640c8,		#GD flash

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

def BFD(v,bs,bl):
    return (v&((1<<(bl))-1))<<(bs)

def BIT(n):
    return 1<<n

Kb = 1024
Mb = 1024 * Kb

tblFlashInt = [
    #        MID                            IC Name         manufactor     size        # SR  unprot    prot       mask                  sb    length
 	FlashInt(FLASH_ID_XTX_25F04B,         "PN25F04B",           "xtx",		4 *Mb,		1,		0x00,		0x07,	BFD(0x0f,2,4),					2,     4, [0x05,0xff,0xff,0xff],		    [0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_XTX_25F08B,         "PN25F08B",           "xtx",		8 *Mb,		1,		0x00,		0x07,	BFD(0x0f,2,4),					2,     4, [0x05,0xff,0xff,0xff],		    [0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_XTX_25F16B,         "XT25F16B",	        "xtx",		16 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_XTX_25F32B,         "XT25F32B",	        "xtx",		32 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_XTX_25Q64B,         "XT25Q64B",           "xtx",		64 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_XTX_25F64B,         "XT25F64B",	        "xtx",		64 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_XTX_25Q128B,		  "XT25Q128B",			"xtx",		128 *Mb,	3,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0x15,0xff],			[0x01,0x31,0x11,0xff]),
	FlashInt(FLASH_ID_XTX_25F128F,		  "XT25F128F",			"xtx",		128 *Mb,	3,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0x15,0xff],			[0x01,0x31,0x11,0xff]),																																															                
	FlashInt(FLASH_ID_Puya_25Q40,		  "P25Q40",				"Puya",		4 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0x31,0xff,0xff]),
	FlashInt(FLASH_ID_Puya_25Q80,		  "P25Q80",				"Puya",		8 *Mb,		2,		0x00,		0x07,	BIT(14)|BFD(0x1f,2,5),		2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0x31,0xff,0xff]),
	FlashInt(FLASH_ID_Puya_25Q80_38,	  "P25Q80",				"Puya",		16 *Mb,		1,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0x31,0xff,0xff]),
	FlashInt(FLASH_ID_Puya_25Q16HB_K,	  "P25Q16HB_K",		    "Puya",		16 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0x31,0xff,0xff]),
	FlashInt(FLASH_ID_Puya_25Q16SU,		  "P25Q16SU",			"Puya",		16 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0x31,0xff,0xff]),
	FlashInt(FLASH_ID_Puya_25Q32H,		  "P25Q32H",		    "Puya",		32 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0x31,0xff,0xff]),
	FlashInt(FLASH_ID_Puya_25Q64H,		  "P25Q64H",		    "Puya",		64 *Mb,		2,		0x00,		0x07,	BIT(14)|BFD(0x1f,2,5),		2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0x31,0xff,0xff]),
	FlashInt(FLASH_ID_Puya_25Q128HA,	  "P25Q128HA",			"Puya",		128 *Mb,	2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0x31,0xff,0xff]),
	FlashInt(FLASH_ID_GT25Q16B,			  "GT25Q16B",			"GT",		16 *Mb,		3,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0x15,0xff],			[0x01,0x31,0x11,0xff]),
	FlashInt(FLASH_ID_MXIC_25V8035F,	  "MX25V8035F",		    "WH",		8 *Mb,		2,		0x00,		0x07,	BIT(12)|BFD(0x1f,2,4),		2,     5,     [0x05,0x15,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_MXIC_25V1635F,	  "MX25V1635F",		    "WH",		16 *Mb,		2,		0x00,		0x07,	BIT(12)|BFD(0x1f,2,4),		2,     5,     [0x05,0x15,0xff,0xff],			[0x01,0xff,0xff,0xff]),																																																                
	FlashInt(FLASH_ID_BY_PN25Q40A,		  "PN25Q40A",			"BY",		4 *Mb,		1,		0x00,		0x07,	BIT(14)|BFD(0x1f,2,3),		2,     3,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_BY_PN25Q80A,		  "PN25Q80A",			"BY",		8 *Mb,		1,		0x00,		0x07,	BIT(14)|BFD(0x1f,2,3),		2,     3,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),																																																                
	FlashInt(FLASH_ID_WB_25Q128JV,		  "WB25Q128JV",		    "WB",		128 *Mb,	2,		0x00,		0x07,	BIT(14)|BFD(0x1f,2,5),		2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_DS_ZB25LQ128C,	  "DS_ZB25LQ128C",	    "WB",		128 *Mb,	2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0x15,0xff],			[0x01,0x31,0x11,0xff]),																																														                
	FlashInt(FLASH_ID_ESMT_25QH16B,	      "EN25QH16B",			"ESMT",	    16 *Mb,		1,		0x00,		0x07,	BFD(0xf,2,5),				2,     4,     [0x05,0xff,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_ESMT_25QE32A,	      "EN25QH32A",		    "ESMT",	    32 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_ESMT_25QW32A,	      "EN25QH32A",		    "ESMT",	    32 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),																																																                
	FlashInt(FLASH_ID_GD_25D40,			  "GD25D40",			"GD",		4 *Mb,		1,		0x00,		0x07,	BFD(0x0f,2,3),				2,     3,     [0x05,0xff,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_GD_25Q41B,		  "GD25Q41B",			"GD",		4 *Mb,		1,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,3),	2,     3,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_GD_25Q41B_T,		  "GD25Q41B",			"GD",		4 *Mb,		1,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,3),	2,     3,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_GD_25D80,			  "GD25D80",			"GD",		8 *Mb,		1,		0x00,		0x07,	BFD(0x0f,2,3),				2,     3,     [0x05,0xff,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_GD_1_25D80,		  "GD25D80",			"GD",		8 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_GD_25WD80E,		  "GD25WD80E",		    "GD",		8 *Mb,		1,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0xff,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_GD_25Q16B,		  "GD25Q16B",		    "GD",		16 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_GD_25WQ16E,		  "GD25WQ16E",		    "GD",		16 *Mb,		2,		0x00,		0x07,	BIT(14)|BFD(0x1f,2,5),		2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_GD_25WQ32E,		  "GD25WQ32E",		    "GD",		32 *Mb,		2,		0x00,		0x07,	BIT(14)|BFD(0x1f,2,5),		2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_GD_25WQ64E,		  "GD25WQ64E",		    "GD",		64 *Mb,		2,		0x00,		0x07,	BIT(14)|BFD(0x1f,2,5),		2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt( FLASH_ID_GD_25Q64,		  "GD25Q64",		    "GD",		64 *Mb,		1,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt( FLASH_ID_GD_25LQ128E,		  "GD25LQ128E",		    "GD",		128 *Mb,	2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt( FLASH_ID_GD_25WQ128E,	      "GD25WQ128E",		    "GD",		128 *Mb,	2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt( FLASH_ID_GD25LX256E,		  "GD25LX256E",		    "GD",		256 *Mb,	1,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0xff,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt( FLASH_ID_TH25D_40HB,		  "TH25D_40HB",		    "TH",		4 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_TH25Q_80HB,		  "TH25Q_80HB",		    "TH",		8 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt(FLASH_ID_TH25Q_16HB,		  "TH25Q_16HB",		    "TH",		16 *Mb,		2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),
	FlashInt( FLASH_ID_XM25QU128C,		  "XM25QU128C",		    "XMC",		128 *Mb,	2,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),																																															                
	FlashInt(FLASH_ID_NA,				  "NA_NA",				"NA",		32 *Mb,		1,		0x00,		0x07,	BIT(14) | BFD(0x1f,2,5),	2,     5,     [0x05,0x35,0xff,0xff],			[0x01,0xff,0xff,0xff]),

]


def GetFlashInfo(mid:int):
    for item in tblFlashInt:
        if item.mid == mid:
            return item
    return None