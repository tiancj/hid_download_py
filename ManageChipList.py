# tagDownload_Chip EXTERN_FLASH = 0
from ExternDownloadFormat import CHIP_EXTERN_Erase, CHIP_EXTERN_Reset
from BK3435DownloadFormat import *
from BK7231DownloadFormat import *

EXTERN_FLASH = 0
ATMEL_FLASH = 1
CHIP_TYPE_BK2452 = 2
CHIP_TYPE_BK2461 = 3
CHIP_TYPE_BK2471 = 4
CHIP_TYPE_BK2535 =5
CHIP_TYPE_BK3231 =6
CHIP_TYPE_BK3231S =7
CHIP_TYPE_BK3260 =8
CHIP_TYPE_BK3266 =9
CHIP_TYPE_BK3431 =10
CHIP_TYPE_BK3431N =11
CHIP_TYPE_BK3431S =12
CHIP_TYPE_BK3432 =13
CHIP_TYPE_BK3435 =14
CHIP_TYPE_BK5121 =15
CHIP_TYPE_BK5141 =16
CHIP_TYPE_BK5863 =17
CHIP_TYPE_BK5863N =18
CHIP_TYPE_BK5866 =19
CHIP_TYPE_BK5933 =20
CHIP_TYPE_BK7231 =21
CHIP_TYPE_BK7231U =22
CHIP_TYPE_BK7221U =23
CHIP_TYPE_BK7251 =24

# tagDownload_Format
EXTERN_FLASH_FORMAT = 0
ATMEL_FLASH_FORMAT = 1
CHIP_BK2452_FORMAT = 2
CHIP_BK2535_FORMAT = 3
CHIP_BK3266_FORMAT = 4
CHIP_BK3431_FORMAT = 5
CHIP_BK3432_FORMAT = 6
CHIP_BK5121_FORMAT = 7
CHIP_BK5141_FORMAT = 8
CHIP_BK5863_FORMAT = 9
CHIP_DUG_FORMAT = 10
CHIP_BK7231U_FORMAT = 11

# tagDownload_Device
A = 0
B = 1
NO = 2


FLASH_SECTOR_32_SIZE	=		32
FLASH_SECTOR_264_SIZE	=		264
FLASH_SECTOR_128_SIZE	=		128
FLASH_SECTOR_256_SIZE	=		256
FLASH_SECTOR_512_SIZE	=		512

DownTool = (
    "R7=R8=0欧姆；R9=R10=R13=不焊", #A号下载板
    "R7=R8=不焊；R9=R10=R13=0欧姆", #B号下载板
    "None",
)

DeviceAndTool = (
    B,					# EXTERN_FLASH
    B,					# ATMEL_FLASH
    A,					# CHIP_TYPE_BK2452
    A,					# CHIP_TYPE_BK2461
    B,					# CHIP_TYPE_BK2471
    A,					# CHIP_TYPE_BK2535
    A,					# CHIP_TYPE_BK3231
    B,					# CHIP_TYPE_BK3231S
    B,					# CHIP_TYPE_BK3260
    NO,					# CHIP_TYPE_BK3266
    A,					# CHIP_TYPE_BK3431
    A,					# CHIP_TYPE_BK3431N
    B,					# CHIP_TYPE_BK3431S
    A,					# CHIP_TYPE_BK3432
    B,					# CHIP_TYPE_BK3435
    NO,					# CHIP_TYPE_BK5121
    NO,					# CHIP_TYPE_BK5141
    B,					# CHIP_TYPE_BK5863
    B,					# CHIP_TYPE_BK5863N
    A,					# CHIP_TYPE_BK5866
    A,					# CHIP_TYPE_BK5933
    B,					# CHIP_TYPE_BK7231
    B,					# CHIP_TYPE_BK7231U
    B,					# CHIP_TYPE_BK7221U
    B,             	    # CHIP_TYPE_BK7251
)

FlashSectorLengthList = (
    FLASH_SECTOR_256_SIZE,		# EXTERN_FLASH
    FLASH_SECTOR_264_SIZE,		# ATMEL_FLASH
    FLASH_SECTOR_32_SIZE,		# CHIP_TYPE_BK2452
    FLASH_SECTOR_32_SIZE,		# CHIP_TYPE_BK2461
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK2471
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK2535
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK3231
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK3231S
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK3260
    FLASH_SECTOR_256_SIZE - 1,	# CHIP_TYPE_BK3266
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK3431
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK3431N
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK3431S
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK3432
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK3435
    FLASH_SECTOR_128_SIZE,		# CHIP_TYPE_BK5121
    FLASH_SECTOR_512_SIZE,		# CHIP_TYPE_BK5141
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK5863
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK5863N
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK5866
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK5933
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK7231
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK7231U
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK7221U
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK7251
)

FlashEraseSectorLenList = (
    4*1024,						# EXTERN_FLASH
    2112,						# ATMEL_FLASH
    0,							# CHIP_TYPE_BK2452
    0,							# CHIP_TYPE_BK2461
    4*1024,						# CHIP_TYPE_BK2471
    512,						# CHIP_TYPE_BK2535
    4*1024,						# CHIP_TYPE_BK3231
    4*1024,						# CHIP_TYPE_BK3231S
    4*1024,						# CHIP_TYPE_BK3260
    4*1024,						# CHIP_TYPE_BK3266
    4*1024,						# CHIP_TYPE_BK3431
    4*1024,						# CHIP_TYPE_BK3431N
    4*1024,						# CHIP_TYPE_BK3431S
    4*1024,						# CHIP_TYPE_BK3432
    4*1024,						# CHIP_TYPE_BK3435
    128,						# CHIP_TYPE_BK5121
    512,						# CHIP_TYPE_BK5141
    16*1024,					# CHIP_TYPE_BK5863
    4*1024,						# CHIP_TYPE_BK5863N
    4*1024,						# CHIP_TYPE_BK5866
    4*1024,						# CHIP_TYPE_BK5933
    4*1024,						# CHIP_TYPE_BK7231
    4*1024,						# CHIP_TYPE_BK7231U
    4*1024,						# CHIP_TYPE_BK7221U
    4*1024,						# CHIP_TYPE_BK7251
)

DownFormatList = (
    EXTERN_FLASH_FORMAT,		# EXTERN_FLASH
    ATMEL_FLASH_FORMAT,			# ATMEL_FLASH
    CHIP_BK2452_FORMAT,			# CHIP_TYPE_BK2452
    CHIP_BK2452_FORMAT,			# CHIP_TYPE_BK2461
    EXTERN_FLASH_FORMAT,		# CHIP_TYPE_BK2471
    CHIP_BK2535_FORMAT,			# CHIP_TYPE_BK2535
    CHIP_BK3431_FORMAT,			# CHIP_TYPE_BK3231
    EXTERN_FLASH_FORMAT,		# CHIP_TYPE_BK3231S
    EXTERN_FLASH_FORMAT,		# CHIP_TYPE_BK3260
    CHIP_BK3266_FORMAT,			# CHIP_TYPE_BK3266
    CHIP_BK3431_FORMAT,			# CHIP_TYPE_BK3431
    CHIP_BK3431_FORMAT,			# CHIP_TYPE_BK3431N
    EXTERN_FLASH_FORMAT,		# CHIP_TYPE_BK3431S
    CHIP_BK3432_FORMAT,			# CHIP_TYPE_BK3432
    EXTERN_FLASH_FORMAT,		# CHIP_TYPE_BK3435
    CHIP_BK5121_FORMAT,			# CHIP_TYPE_BK5121
    CHIP_BK5141_FORMAT,			# CHIP_TYPE_BK5141
    CHIP_BK5863_FORMAT,			# CHIP_TYPE_BK5863
    EXTERN_FLASH_FORMAT,		# CHIP_TYPE_BK5863N
    CHIP_BK3431_FORMAT,			# CHIP_TYPE_BK5866
    CHIP_BK3431_FORMAT,			# CHIP_TYPE_BK5933
    EXTERN_FLASH_FORMAT,		# CHIP_TYPE_BK7231
    CHIP_BK7231U_FORMAT,		# CHIP_TYPE_BK7231U //changed by wang
    CHIP_BK7231U_FORMAT,		# CHIP_TYPE_BK7221U //changed by wang
    CHIP_BK7231U_FORMAT,		# CHIP_TYPE_BK7251U //changed by wang
)

FlashLoadFileMaxSize = (
    2 * 1024 * 1024,		# EXTERN_FLASH
    528 * 1024,				# ATMEL_FLASH
    8 * 1024,				# CHIP_TYPE_BK2452
    8 * 1024,				# CHIP_TYPE_BK2461
    2 * 1024 *1024,			# CHIP_TYPE_BK2471
    32 * 1024,				# CHIP_TYPE_BK2535
    256 * 1024,				# CHIP_TYPE_BK3231
    2 * 1024 * 1024,		# CHIP_TYPE_BK3231S
    2 * 1024 * 1024,		# CHIP_TYPE_BK3260
    2 * 1024 * 1024,		# CHIP_TYPE_BK3266
    128 * 1024,				# CHIP_TYPE_BK3431
    128 * 1024,				# CHIP_TYPE_BK3431N
    2 * 1024 * 1024,		# CHIP_TYPE_BK3431S
    160 * 1024,				# CHIP_TYPE_BK3432
    2 * 1024 * 1024,		# CHIP_TYPE_BK3435
    32 * 1024,				# CHIP_TYPE_BK5121
    32 * 1024,				# CHIP_TYPE_BK5141
    192 * 1024,				# CHIP_TYPE_BK5863
    1024 * 1024,		    # CHIP_TYPE_BK5863N  
    64 * 1024,				# CHIP_TYPE_BK5866
    32 * 1024,				# CHIP_TYPE_BK5933
    2 * 1024 * 1024,		# CHIP_TYPE_BK7231 
    2 * 1024 * 1024,		# CHIP_TYPE_BK7231U
    2 * 1024 * 1024,		# CHIP_TYPE_BK7221U
    2 * 1024 * 1024,		# CHIP_TYPE_BK7251
)

SpiDivClkList = (
    0,		# EXTERN_FLASH
    0,		# ATMEL_FLASH
    4,		# CHIP_TYPE_BK2452
    4,		# CHIP_TYPE_BK2461
    4,		# CHIP_TYPE_BK2471
    4,		# CHIP_TYPE_BK2535
    4,		# CHIP_TYPE_BK3231
    0,		# CHIP_TYPE_BK3231S
    0,		# CHIP_TYPE_BK3260
    0,		# CHIP_TYPE_BK3266
    4,		# CHIP_TYPE_BK3431
    4,		# CHIP_TYPE_BK3431N
    0,		# CHIP_TYPE_BK3431S
    4,		# CHIP_TYPE_BK3432
    0,		# CHIP_TYPE_BK3435
    4,		# CHIP_TYPE_BK5121
    4,		# CHIP_TYPE_BK5141
    4,		# CHIP_TYPE_BK5863
    0,		# CHIP_TYPE_BK5863N
    4,		# CHIP_TYPE_BK5866
    4,		# CHIP_TYPE_BK5933
    0,		# CHIP_TYPE_BK7231
    0,		# CHIP_TYPE_BK7231U
    0,		# CHIP_TYPE_BK7221U
    0,		# CHIP_TYPE_BK7251
)

RollCodeLengthList = (
    0,		# EXTERN_FLASH
    0,		# ATMEL_FLASH
    4,		# CHIP_TYPE_BK2452
    4,		# CHIP_TYPE_BK2461
    0,		# CHIP_TYPE_BK2471
    0,		# CHIP_TYPE_BK2535
    4,		# CHIP_TYPE_BK3231
    0,		# CHIP_TYPE_BK3231S
    0,		# CHIP_TYPE_BK3260
    0,		# CHIP_TYPE_BK3266
    4,		# CHIP_TYPE_BK3431
    4,		# CHIP_TYPE_BK3431N
    0,		# CHIP_TYPE_BK3431S
    4,		# CHIP_TYPE_BK3432
    0,		# CHIP_TYPE_BK3435
    0,		# CHIP_TYPE_BK5121
    0,		# CHIP_TYPE_BK5141
    0,		# CHIP_TYPE_BK5863
    0,		# CHIP_TYPE_BK5863N
    4,		# CHIP_TYPE_BK5866
    0,		# CHIP_TYPE_BK5933
    0,		# CHIP_TYPE_BK7231
    0,		# CHIP_TYPE_BK7231U
    0,		# CHIP_TYPE_BK7221U
    0,		# CHIP_TYPE_BK7251
)

ChipStrList = (
    "通用 Flash",	# EXTERN_FLASH
    "ATMEL Flash",	# ATMEL_FLASH
    "BK2452",		# CHIP_TYPE_BK2452
    "BK2461",		# CHIP_TYPE_BK2461
    "BK2471",		# CHIP_TYPE_BK2471
    "BK2535",		# CHIP_TYPE_BK2535
    "BK3231",		# CHIP_TYPE_BK3231
    "BK3231s",		# CHIP_TYPE_BK3231S
    "BK3260",		# CHIP_TYPE_BK3260
    "BK3266",		# CHIP_TYPE_BK3266
    "BK3431",		# CHIP_TYPE_BK3431
    "BK3431n",		# CHIP_TYPE_BK3431N
    "BK3431s",		# CHIP_TYPE_BK3431S
    "BK3432",		# CHIP_TYPE_BK3432
    "BK3435",		# CHIP_TYPE_BK3435
    "BK5121",		# CHIP_TYPE_BK5121
    "BK5141",		# CHIP_TYPE_BK5141
    "BK5863",		# CHIP_TYPE_BK5863
    "BK5863n",		# CHIP_TYPE_BK5863N
    "BK5866",		# CHIP_TYPE_BK5866
    "BK5933",		# CHIP_TYPE_BK5933
    "BK7231",		# CHIP_TYPE_BK7231
    "BK7231U",		# CHIP_TYPE_BK7231U
    "BK7221U",		# CHIP_TYPE_BK7221U
    "BK7251",		# CHIP_TYPE_BK7251
)

HelpInforList = (
    "None",						# EXTERN_FLASH
    "BK2461<=8KB,其他<=32KB",	# ATMEL_FLASH
    "None",						# CHIP_TYPE_BK2452
    "None",						# CHIP_TYPE_BK2461
    "TSTEN=HIGH,P30=HIGH",		# CHIP_TYPE_BK2471
    "None",						# CHIP_TYPE_BK2535
    "None",						# CHIP_TYPE_BK3231
    "TSTEN=HIGH,P30=HIGH",		# CHIP_TYPE_BK3231S
    "MBIST=HIGH",				# CHIP_TYPE_BK3260
    "UART Download",			# CHIP_TYPE_BK3266
    "None",						# CHIP_TYPE_BK3431
    "None",						# CHIP_TYPE_BK3431N
    "None",						# CHIP_TYPE_BK3431S
    "None",						# CHIP_TYPE_BK3432
    "None",						# CHIP_TYPE_BK3435
    "None",						# CHIP_TYPE_BK5121
    "I2C Download",				# CHIP_TYPE_BK5141
    "GACTIVE=HIGH",				# CHIP_TYPE_BK5863
    "None",						# CHIP_TYPE_BK5863N
    "None",						# CHIP_TYPE_BK5866
    "None",						# CHIP_TYPE_BK5933
    "None",						# CHIP_TYPE_BK7231
    "None",						# CHIP_TYPE_BK7231U
    "None",						# CHIP_TYPE_BK7221U
    "None",						# CHIP_TYPE_BK7251
)

Reset = (
    CHIP_EXTERN_Reset,			# EXTERN_FLASH
    None, #CHIP_ATEMEL_Reset,			# ATMEL_FLASH
    None, #CHIP_BK2452_Reset,			# CHIP_TYPE_BK2452
    None, #CHIP_BK2452_Reset,			# CHIP_TYPE_BK2461
    CHIP_EXTERN_Reset,			# CHIP_TYPE_BK2471
    None, #CHIP_BK2535_Reset,			# CHIP_TYPE_BK2535
    None, #CHIP_BK3231_Reset,			# CHIP_TYPE_BK3231
    CHIP_EXTERN_Reset,			# CHIP_TYPE_BK3231S
    CHIP_EXTERN_Reset,			# CHIP_TYPE_BK3260
    None, #CHIP_BK3266_Reset,			# CHIP_TYPE_BK3266
    None, #CHIP_BK3431_Reset,			# CHIP_TYPE_BK3431
    None, #CHIP_BK3431n_Reset,			# CHIP_TYPE_BK3431N
    None, #CHIP_BK3431s_Reset,			# CHIP_TYPE_BK3431S
    None, #CHIP_BK3432_Reset,			# CHIP_TYPE_BK3432
    CHIP_BK3435_Reset,			# CHIP_TYPE_BK3435
    None, #CHIP_BK5121_Reset,			# CHIP_TYPE_BK5121
    None, #CHIP_BK5141_Reset,			# CHIP_TYPE_BK5141
    None, #CHIP_BK3231_Reset,			# CHIP_TYPE_BK5863
    None, #CHIP_BK5863N_Reset,			# CHIP_TYPE_BK5863N
    None, #CHIP_BK3231_Reset,			# CHIP_TYPE_BK5866
    None, #CHIP_BK3231_Reset,			# CHIP_TYPE_BK5933
    CHIP_EXTERN_Reset,			# CHIP_TYPE_BK7231
    CHIP_BK3435_Reset,			# CHIP_TYPE_BK7231U
    CHIP_BK3435_Reset,			# CHIP_TYPE_BK7221U
    CHIP_BK3435_Reset,			# CHIP_TYPE_BK7251
)

Erase = (
    CHIP_EXTERN_Erase,			# EXTERN_FLASH
    None, #CHIP_ATEMEL_Erase,			# ATMEL_FLASH
    None,						# CHIP_TYPE_BK2452
    None,						# CHIP_TYPE_BK2461
    CHIP_EXTERN_Erase,			# CHIP_TYPE_BK2471
    None, #CHIP_BK2535_Erase,			# CHIP_TYPE_BK2535
    None, #CHIP_BK3231_Erase,			# CHIP_TYPE_BK3231
    CHIP_EXTERN_Erase,			# CHIP_TYPE_BK3231S
    CHIP_EXTERN_Erase,			# CHIP_TYPE_BK3260
    None, #CHIP_BK3266_Erase,			# CHIP_TYPE_BK3266
    None, #CHIP_BK3231_Erase,			# CHIP_TYPE_BK3431
    None, #CHIP_BK3231_Erase,			# CHIP_TYPE_BK3431N
    CHIP_EXTERN_Erase,			# CHIP_TYPE_BK3431S
    None, #CHIP_BK3432_Erase,			# CHIP_TYPE_BK3432
    CHIP_EXTERN_Erase,			# CHIP_TYPE_BK3435
    None, #CHIP_BK5121_Erase,			# CHIP_TYPE_BK5121
    None, #CHIP_BK5141_Erase,			# CHIP_TYPE_BK5141
    None, #CHIP_BK5863_Erase,			# CHIP_TYPE_BK5863
    None, #CHIP_BK5863N_Erase,			# CHIP_TYPE_BK5863N
    None, #CHIP_BK3231_Erase,			# CHIP_TYPE_BK5866
    None, #CHIP_BK3231_Erase,			# CHIP_TYPE_BK5933
    CHIP_EXTERN_Erase,			# CHIP_TYPE_BK7231
    CHIP_EXTERN_Erase,			# CHIP_TYPE_BK7231U
    CHIP_EXTERN_Erase,			# CHIP_TYPE_BK7221U
    CHIP_EXTERN_Erase,			# CHIP_TYPE_BK7251
)

Start = (
    None,						# EXTERN_FLASH
    None,						# ATMEL_FLASH
    None,						# CHIP_TYPE_BK2452
    None,						# CHIP_TYPE_BK2461
    None,						# CHIP_TYPE_BK2471
    None, #CHIP_BK3231_Start,			# CHIP_TYPE_BK2535
    None, #CHIP_BK3231_Start,			# CHIP_TYPE_BK3231
    None,						# CHIP_TYPE_BK3231S
    None,						# CHIP_TYPE_BK3260
    None,						# CHIP_TYPE_BK3266
    None, #CHIP_BK3231_Start,			# CHIP_TYPE_BK3431
    None, #CHIP_BK3231_Start,			# CHIP_TYPE_BK3431N
    None,						# CHIP_TYPE_BK3431S
    None, #CHIP_BK3231_Start,			# CHIP_TYPE_BK3432
    CHIP_BK3435_Start,			# CHIP_TYPE_BK3435
    None, #CHIP_BK5121_Start,			# CHIP_TYPE_BK5121
    None,						# CHIP_TYPE_BK5141
    None, #CHIP_BK3231_Start,			# CHIP_TYPE_BK5863
    None,						# CHIP_TYPE_BK5863N
    None, #CHIP_BK3231_Start,			# CHIP_TYPE_BK5866
    None, #CHIP_BK3231_Start,			# CHIP_TYPE_BK5933
    None,						# CHIP_TYPE_BK7231
    CHIP_BK3435_Start,			# CHIP_TYPE_BK7231U
    CHIP_BK3435_Start,			# CHIP_TYPE_BK7221U
    CHIP_BK3435_Start,			# CHIP_TYPE_BK7251
)

End = (
    CHIP_EXTERN_End,			# EXTERN_FLASH
    None,						# ATMEL_FLASH
    None, #CHIP_BK2452_End,			# CHIP_TYPE_BK2452
    None, #CHIP_BK2452_End,			# CHIP_TYPE_BK2461
    CHIP_EXTERN_End,			# CHIP_TYPE_BK2471
    None, #CHIP_BK3231_End,			# CHIP_TYPE_BK2535
    None, #CHIP_BK3231_End,			# CHIP_TYPE_BK3231
    CHIP_EXTERN_End,			# CHIP_TYPE_BK3231S
    CHIP_EXTERN_End,			# CHIP_TYPE_BK3260
    None, #CHIP_BK3266_End,			# CHIP_TYPE_BK3266
    None, #CHIP_BK3431_End,			# CHIP_TYPE_BK3431
    None, #CHIP_BK3431n_End,			# CHIP_TYPE_BK3431N
    None, #CHIP_BK3431s_End,			# CHIP_TYPE_BK3431S
    None, #CHIP_BK3432_End,			# CHIP_TYPE_BK3432
    CHIP_BK3435_End,			# CHIP_TYPE_BK3435
    None, #CHIP_BK5121_End,			# CHIP_TYPE_BK5121
    None,						# CHIP_TYPE_BK5141
    None, #CHIP_BK3231_End,			# CHIP_TYPE_BK5863
    None,						# CHIP_TYPE_BK5863N
    None, #CHIP_BK3231_End,			# CHIP_TYPE_BK5866
    None, #CHIP_BK3231_End,			# CHIP_TYPE_BK5933
    CHIP_EXTERN_End,			# CHIP_TYPE_BK7231
    CHIP_BK3435_End,			# CHIP_TYPE_BK7231U
    CHIP_BK3435_End,			# CHIP_TYPE_BK7221U
    CHIP_BK3435_End,			# CHIP_TYPE_BK7251
)

writeDbug = (
    None, #CHIP_EXTERN_WriteDebug,		# EXTERN_FLASH
    None,			            # ATMEL_FLASH
    None,			            # CHIP_TYPE_BK2452
    None,			            # CHIP_TYPE_BK2461
    None,			            # CHIP_TYPE_BK2471
    None, #CHIP_BK2535_WriteDebug,		# CHIP_TYPE_BK2535
    None,			            # CHIP_TYPE_BK3231
    None,			            # CHIP_TYPE_BK3231S
    None,			            # CHIP_TYPE_BK3260
    None,			            # CHIP_TYPE_BK3266
    None,			            # CHIP_TYPE_BK3431
    None,			            # CHIP_TYPE_BK3431N
    None,			            # CHIP_TYPE_BK3431S
    None, #CHIP_BK3432_WriteDebug,		# CHIP_TYPE_BK3432
    None, #CHIP_BK3435_WriteDebug,		# CHIP_TYPE_BK3435
    None, #CHIP_BK5121_WriteDebug,		# CHIP_TYPE_BK5121
    None, #CHIP_BK5141_WriteDebug,		# CHIP_TYPE_BK5141
    None,			            # CHIP_TYPE_BK5863
    None,			            # CHIP_TYPE_BK5863N
    None, #CHIP_BK5866_WriteDebug,		# CHIP_TYPE_BK5866
    None,			            # CHIP_TYPE_BK5933
    None,			            # CHIP_TYPE_BK7231
    None, #CHIP_BK3435_WriteDebug,		# CHIP_TYPE_BK7231U
    None, #CHIP_BK3435_WriteDebug,		# CHIP_TYPE_BK7221U
    None, #CHIP_BK3435_WriteDebug,		# CHIP_TYPE_BK7251
)

ReadDbug = (
    None, #CHIP_EXTERN_ReadDebug,		# EXTERN_FLASH
    None,			            # ATMEL_FLASH
    None,			            # CHIP_TYPE_BK2452
    None,			            # CHIP_TYPE_BK2461
    None,			            # CHIP_TYPE_BK2471
    None, #CHIP_BK2535_ReadDebug,		# CHIP_TYPE_BK2535
    None,			            # CHIP_TYPE_BK3231
    None,			            # CHIP_TYPE_BK3231S
    None,			            # CHIP_TYPE_BK3260
    None,			            # CHIP_TYPE_BK3266
    None,			            # CHIP_TYPE_BK3431
    None,			            # CHIP_TYPE_BK3431N
    None,			            # CHIP_TYPE_BK3431S
    None, #CHIP_BK3432_ReadDebug,		# CHIP_TYPE_BK3432
    None, #CHIP_BK3435_ReadDebug,		# CHIP_TYPE_BK3435
    None, #CHIP_BK5121_ReadDebug,		# CHIP_TYPE_BK5121
    None, #CHIP_BK5141_ReadDebug,		# CHIP_TYPE_BK5141
    None,			            # CHIP_TYPE_BK5863
    None,			            # CHIP_TYPE_BK5863N
    None, #CHIP_BK5866_ReadDebug,		# CHIP_TYPE_BK5866
    None,			            # CHIP_TYPE_BK5933
    None,			            # CHIP_TYPE_BK7231
    None, #CHIP_BK3435_ReadDebug,		# CHIP_TYPE_BK7231U
    None, #CHIP_BK3435_ReadDebug,		# CHIP_TYPE_BK7221U
    None, #CHIP_BK3435_ReadDebug,		# CHIP_TYPE_BK7251
)

ConfigWrite = (
    None,			            # EXTERN_FLASH
    None,			            # ATMEL_FLASH
    None,			            # CHIP_TYPE_BK2452
    None,			            # CHIP_TYPE_BK2461
    None,			            # CHIP_TYPE_BK2471
    None,			            # CHIP_TYPE_BK2535
    None,			            # CHIP_TYPE_BK3231
    None,			            # CHIP_TYPE_BK3231S
    None,			            # CHIP_TYPE_BK3260
    None,			            # CHIP_TYPE_BK3266
    None, #CHIP_BK3431_Config,			# CHIP_TYPE_BK3431
    None, #CHIP_BK3431n_Config,		# CHIP_TYPE_BK3431N
    None,			            # CHIP_TYPE_BK3431S
    None, #CHIP_BK3432_Config,			# CHIP_TYPE_BK3432
    None, #CHIP_BK3435_Config,			# CHIP_TYPE_BK3435
    None,			            # CHIP_TYPE_BK5121
    None,			            # CHIP_TYPE_BK5141
    None,			            # CHIP_TYPE_BK5863
    None, #CHIP_BK5863n_Config,		# CHIP_TYPE_BK5863N
    None,			            # CHIP_TYPE_BK5866
    None,			            # CHIP_TYPE_BK5933
    None,			            # CHIP_TYPE_BK7231
    None,			            # CHIP_TYPE_BK7231U  //ex val = CHIP_BK3435_Config
    None,			            # CHIP_TYPE_BK7221U  //ex val = CHIP_BK3435_Config
    None,			            # CHIP_TYPE_BK7251  //ex val = CHIP_BK3435_Config
)

ConfigAnalyze = (
    None,			            # EXTERN_FLASH
    None,			            # ATMEL_FLASH
    None, #CHIP_BK2452_Config,			# CHIP_TYPE_BK2452
    None, #CHIP_BK2452_Config,			# CHIP_TYPE_BK2461
    None,			            # CHIP_TYPE_BK2471
    None, #CHIP_BK3431s_Config,		# CHIP_TYPE_BK2535
    None,			            # CHIP_TYPE_BK3231
    None, #CHIP_BK3231s_Config,		# CHIP_TYPE_BK3231S
    None,			            # CHIP_TYPE_BK3260
    None, #CHIP_BK3266_Config,			# CHIP_TYPE_BK3266
    None,			            # CHIP_TYPE_BK3431
    None,			            # CHIP_TYPE_BK3431N
    None, #CHIP_BK3431s_Config,		# CHIP_TYPE_BK3431S
    None,			            # CHIP_TYPE_BK3432
    None,			            # CHIP_TYPE_BK3435
    None,			            # CHIP_TYPE_BK5121
    None,			            # CHIP_TYPE_BK5141
    None,			            # CHIP_TYPE_BK5863
    None,			            # CHIP_TYPE_BK5863N
    None,			            # CHIP_TYPE_BK5866
    None,			            # CHIP_TYPE_BK5933
    None, #CHIP_BK3431s_Config,		# CHIP_TYPE_BK7231
    None, #CHIP_BK3431s_Config,    	# CHIP_TYPE_BK7231U 
    None, #CHIP_BK3431s_Config,		# CHIP_TYPE_BK7221U
    None, #CHIP_BK3431s_Config,		# CHIP_TYPE_BK7251
)

ConfigLoad = (
    None,			            # EXTERN_FLASH
    None,			            # ATMEL_FLASH
    None,			            # CHIP_TYPE_BK2452
    None,			            # CHIP_TYPE_BK2461
    None,			            # CHIP_TYPE_BK2471
    None,			            # CHIP_TYPE_BK2535
    None,			            # CHIP_TYPE_BK3231
    None,			            # CHIP_TYPE_BK3231S
    None,			            # CHIP_TYPE_BK3260
    None, #CHIP_BK3266_LoadConfig,		# CHIP_TYPE_BK3266
    None,			            # CHIP_TYPE_BK3431
    None,			            # CHIP_TYPE_BK3431N
    None, #CHIP_BK3431s_LoadConfig,	# CHIP_TYPE_BK3431S
    None,			            # CHIP_TYPE_BK3432
    None,			            # CHIP_TYPE_BK3435
    None,			            # CHIP_TYPE_BK5121
    None,			            # CHIP_TYPE_BK5141
    None,			            # CHIP_TYPE_BK5863
    None,			            # CHIP_TYPE_BK5863N
    None,			            # CHIP_TYPE_BK5866
    None,			            # CHIP_TYPE_BK5933
    None, #CHIP_BK7231_LoadConfig,		# CHIP_TYPE_BK7231
    None, #CHIP_BK7231_LoadConfig,		# CHIP_TYPE_BK7231U
    None,			            # CHIP_TYPE_BK7221U
    None,			            # CHIP_TYPE_BK7251
)

AddrCheck = (
    None,			            # EXTERN_FLASH
    None,			            # ATMEL_FLASH
    None,			            # CHIP_TYPE_BK2452
    None,			            # CHIP_TYPE_BK2461
    None,			            # CHIP_TYPE_BK2471
    None,			            # CHIP_TYPE_BK2535
    None,			            # CHIP_TYPE_BK3231
    None,			            # CHIP_TYPE_BK3231S
    None,			            # CHIP_TYPE_BK3260
    None,			            # CHIP_TYPE_BK3266
    None,			            # CHIP_TYPE_BK3431
    None,			            # CHIP_TYPE_BK3431N
    None,			            # CHIP_TYPE_BK3431S
    None,			            # CHIP_TYPE_BK3432
    None,			            # CHIP_TYPE_BK3435
    None,			            # CHIP_TYPE_BK5121
    None,			            # CHIP_TYPE_BK5141
    None,			            # CHIP_TYPE_BK5863
    None,			            # CHIP_TYPE_BK5863N
    None,			            # CHIP_TYPE_BK5866
    None,			            # CHIP_TYPE_BK5933
    CHIP_BK7231_AddrCheck,		# CHIP_TYPE_BK7231
    None,			            # CHIP_TYPE_BK7231U
    None,			            # CHIP_TYPE_BK7221U
    None,			            # CHIP_TYPE_BK7251
)

OffLineTool = (
    (None,0),			# EXTERN_FLASH
    (None,0),			# ATMEL_FLASH
    (None,0),			# CHIP_TYPE_BK2452
    (None,0),			# CHIP_TYPE_BK2461
    (None,0),			# CHIP_TYPE_BK2471
    (None,0),			# CHIP_TYPE_BK2535
    (None,0),			# CHIP_TYPE_BK3231
    (None,0),			# CHIP_TYPE_BK3231S
    (None,0),			# CHIP_TYPE_BK3260
    (None,0),			# CHIP_TYPE_BK3266
    (None,0),			# CHIP_TYPE_BK3431
    (None,0),			# CHIP_TYPE_BK3431N
    (None,0),			# CHIP_TYPE_BK3431S
    (None,0),			# CHIP_TYPE_BK3432
    (None,0),			# CHIP_TYPE_BK3435
    (None,0),			# CHIP_TYPE_BK5121
    (None,0),			# CHIP_TYPE_BK5141
    (None,0),			# CHIP_TYPE_BK5863
    (None,0),			# CHIP_TYPE_BK5863N
    (None,0),			# CHIP_TYPE_BK5866
    (None,0),			# CHIP_TYPE_BK5933
    (None,0), #(ucBK7231DownloadBoardBinFile,ucBK7231DownloadBoadrBinLen),		# CHIP_TYPE_BK7231
    (None,0),			# CHIP_TYPE_BK7231U
    (None,0),			# CHIP_TYPE_BK7221U
    (None,0),			# CHIP_TYPE_BK7251
)

OffLinePrepareBin = (
    None,			# EXTERN_FLASH
    None,			# ATMEL_FLASH
    None,			# CHIP_TYPE_BK2452
    None,			# CHIP_TYPE_BK2461
    None,			# CHIP_TYPE_BK2471
    None,			# CHIP_TYPE_BK2535
    None,			# CHIP_TYPE_BK3231
    None,			# CHIP_TYPE_BK3231S
    None,			# CHIP_TYPE_BK3260
    None,			# CHIP_TYPE_BK3266
    None,			# CHIP_TYPE_BK3431
    None,			# CHIP_TYPE_BK3431N
    None,			# CHIP_TYPE_BK3431S
    None,			# CHIP_TYPE_BK3432
    None,			# CHIP_TYPE_BK3435
    None,			# CHIP_TYPE_BK5121
    None,			# CHIP_TYPE_BK5141
    None,			# CHIP_TYPE_BK5863
    None,			# CHIP_TYPE_BK5863N
    None,			# CHIP_TYPE_BK5866
    None,			# CHIP_TYPE_BK5933
    None, #CHIP_BK7231_PrepareOffLoadBin,		# CHIP_TYPE_BK7231
    None,			# CHIP_TYPE_BK7231U
    None,			# CHIP_TYPE_BK7221U
    None,			# CHIP_TYPE_BK7251
)

DugWndShow = (
    None, #CHIP_EXTERN_WndDebug,			# EXTERN_FLASH
    None,			# ATMEL_FLASH
    None,			# CHIP_TYPE_BK2452
    None,			# CHIP_TYPE_BK2461
    None,			# CHIP_TYPE_BK2471
    None, #CHIP_BK2535_WndDebug,			# CHIP_TYPE_BK2535
    None,			# CHIP_TYPE_BK3231
    None,			# CHIP_TYPE_BK3231S
    None,			# CHIP_TYPE_BK3260
    None,			# CHIP_TYPE_BK3266
    None,			# CHIP_TYPE_BK3431
    None,			# CHIP_TYPE_BK3431N
    None,			# CHIP_TYPE_BK3431S
    None, #CHIP_BK3432_WndDebug,			# CHIP_TYPE_BK3432
    None, #CHIP_BK3435_WndDebug,			# CHIP_TYPE_BK3435
    None, #CHIP_BK5121_WndDebug,			# CHIP_TYPE_BK5121
    None, #CHIP_BK5141_WndDebug,			# CHIP_TYPE_BK5141
    None,			# CHIP_TYPE_BK5863
    None,			# CHIP_TYPE_BK5863N
    None, #CHIP_BK5866_WndDebug,			# CHIP_TYPE_BK5866
    None,			# CHIP_TYPE_BK5933
    None,			# CHIP_TYPE_BK7231
    None, #CHIP_BK3435_WndDebug,			# CHIP_TYPE_BK7231U
    None, #CHIP_BK3435_WndDebug,			# CHIP_TYPE_BK7221U
    None, #CHIP_BK3435_WndDebug,			# CHIP_TYPE_BK7251
)

def DownToolGet(SelectChipNumb):
    return DownTool[SelectChipNumb]

def DeviceAndToolGet(SelectChipNumb):
	return DeviceAndTool[SelectChipNumb]

def  FlashSectorLengthBufGet(SelectChipNumb):
	return FlashSectorLengthList[SelectChipNumb]

def FlashSectorLengthListGet(SelectChipNumb):
	return FlashSectorLengthList[SelectChipNumb]

def FlashEraseSectorLenGet(SelectChipNumb):
	return FlashEraseSectorLenList[SelectChipNumb]

def DownFormatListGet(SelectChipNumb):
	return DownFormatList[SelectChipNumb]

def FlashLoadFileMaxSizeGet(SelectChipNumb):
	return FlashLoadFileMaxSize[SelectChipNumb]

def SpiDivClkListGet(SelectChipNumb):
	return SpiDivClkList[SelectChipNumb]

def RollCodeLengthListGet(SelectChipNumb):
	return RollCodeLengthList[SelectChipNumb]

def ChipStrListGet(SelectChipNumb):
	return ChipStrList[SelectChipNumb]

def HelpInforListGet(SelectChipNumb):
	return HelpInforList[SelectChipNumb]

def ResetGet(SelectChipNumb):
	return Reset[SelectChipNumb]

def EraseGet(SelectChipNumb):
	return Erase[SelectChipNumb]

def StartGet(SelectChipNumb):
	return Start[SelectChipNumb]

def EndGet(SelectChipNumb):
	return End[SelectChipNumb]

def writeDebugGet(SelectChipNumb):
	return writeDbug[SelectChipNumb]

def readDebugGet(SelectChipNumb):
	return ReadDbug[SelectChipNumb]

def ConfigAnalyzeGet(SelectChipNumb):
	return ConfigAnalyze[SelectChipNumb]

def ConfigWriteGet(SelectChipNumb):
	return ConfigWrite[SelectChipNumb]

def ConfigLoadGet(SelectChipNumb):
	return ConfigLoad[SelectChipNumb]

def AddrCheckGet(SelectChipNumb):
	return AddrCheck[SelectChipNumb]

def OffLineToolGet(SelectChipNumb):
	return OffLineTool[SelectChipNumb]

def OffLinePrepareBinGet(SelectChipNumb):
	return OffLinePrepareBin[SelectChipNumb]

def DugWndShowGet(SelectChipNumb):
	return DugWndShow[SelectChipNumb]
