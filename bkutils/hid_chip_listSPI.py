# encoding: utf8
#
# HID Download Tool
#
# Copyright (c) BekenCorp. (chunjian.tian@bekencorp.com).  All rights reserved.
#
# This software may be distributed under the terms of the BSD license.
# See README for more details.
#
# tagDownload_Chip EXTERN_FLASH = 0
from .chip.ExternDownloadFormatSPI import CHIP_EXTERN_Erase, CHIP_EXTERN_Reset
from .chip.BK3435DownloadFormatSPI import *
from .chip.BK7231DownloadFormatSPI import *

EXTERN_FLASH = 0
CHIP_TYPE_BK7231 = 1
CHIP_TYPE_BK7231U = 2
CHIP_TYPE_BK7221U = 3
CHIP_TYPE_BK7251 = 4

# tagDownload_Format
EXTERN_FLASH_FORMAT = 0
CHIP_BK7231U_FORMAT = 11

FLASH_SECTOR_32_SIZE    = 32
FLASH_SECTOR_264_SIZE   = 264
FLASH_SECTOR_128_SIZE   = 128
FLASH_SECTOR_256_SIZE   = 256
FLASH_SECTOR_512_SIZE   = 512

FlashSectorLengthList = (
    FLASH_SECTOR_256_SIZE,		# EXTERN_FLASH
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK7231
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK7231U
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK7221U
    FLASH_SECTOR_256_SIZE,		# CHIP_TYPE_BK7251
)

FlashEraseSectorLenList = (
    4*1024,						# EXTERN_FLASH
    4*1024,						# CHIP_TYPE_BK7231
    4*1024,						# CHIP_TYPE_BK7231U
    4*1024,						# CHIP_TYPE_BK7221U
    4*1024,						# CHIP_TYPE_BK7251
)

DownFormatList = (
    EXTERN_FLASH_FORMAT,		# EXTERN_FLASH
    EXTERN_FLASH_FORMAT,		# CHIP_TYPE_BK7231
    CHIP_BK7231U_FORMAT,		# CHIP_TYPE_BK7231U //changed by wang
    CHIP_BK7231U_FORMAT,		# CHIP_TYPE_BK7221U //changed by wang
    CHIP_BK7231U_FORMAT,		# CHIP_TYPE_BK7251U //changed by wang
)

FlashLoadFileMaxSize = (
    2*1024*1024,		    # EXTERN_FLASH
    2*1024*1024,		    # CHIP_TYPE_BK7231 
    2*1024*1024,		    # CHIP_TYPE_BK7231U
    2*1024*1024,		    # CHIP_TYPE_BK7221U
    2*1024*1024,		    # CHIP_TYPE_BK7251
)

SpiDivClkList = (
    0,		                    # EXTERN_FLASH
    0,		                    # CHIP_TYPE_BK7231
    0,		                    # CHIP_TYPE_BK7231U
    0,		                    # CHIP_TYPE_BK7221U
    0,		                    # CHIP_TYPE_BK7251
)

RollCodeLengthList = (
    0,		                    # EXTERN_FLASH
    0,		                    # CHIP_TYPE_BK7231
    0,		                    # CHIP_TYPE_BK7231U
    0,		                    # CHIP_TYPE_BK7221U
    0,		                    # CHIP_TYPE_BK7251
)

ChipStrList = (
    "Generic Flash",            # EXTERN_FLASH
    "BK7231",		            # CHIP_TYPE_BK7231
    "BK7231U",		            # CHIP_TYPE_BK7231U
    "BK7221U",		            # CHIP_TYPE_BK7221U
    "BK7251",		            # CHIP_TYPE_BK7251
)

Reset = (
    CHIP_EXTERN_Reset,			# EXTERN_FLASH
    CHIP_EXTERN_Reset,			# CHIP_TYPE_BK7231
    CHIP_BK3435_Reset,			# CHIP_TYPE_BK7231U
    CHIP_BK3435_Reset,			# CHIP_TYPE_BK7221U
    CHIP_BK3435_Reset,			# CHIP_TYPE_BK7251
)

Erase = (
    CHIP_EXTERN_Erase,			# EXTERN_FLASH
    CHIP_EXTERN_Erase,			# CHIP_TYPE_BK7231
    CHIP_EXTERN_Erase,			# CHIP_TYPE_BK7231U
    CHIP_EXTERN_Erase,			# CHIP_TYPE_BK7221U
    CHIP_EXTERN_Erase,			# CHIP_TYPE_BK7251
)

Start = (
    None,						# EXTERN_FLASH
    None,						# CHIP_TYPE_BK7231
    CHIP_BK3435_Start,			# CHIP_TYPE_BK7231U
    CHIP_BK3435_Start,			# CHIP_TYPE_BK7221U
    CHIP_BK3435_Start,			# CHIP_TYPE_BK7251
)

End = (
    CHIP_EXTERN_End,			# EXTERN_FLASH
    CHIP_EXTERN_End,			# CHIP_TYPE_BK7231
    CHIP_BK3435_End,			# CHIP_TYPE_BK7231U
    CHIP_BK3435_End,			# CHIP_TYPE_BK7221U
    CHIP_BK3435_End,			# CHIP_TYPE_BK7251
)

writeDbug = (
    None, #CHIP_EXTERN_WriteDebug,		# EXTERN_FLASH
    None,			                    # CHIP_TYPE_BK7231
    None, #CHIP_BK3435_WriteDebug,		# CHIP_TYPE_BK7231U
    None, #CHIP_BK3435_WriteDebug,		# CHIP_TYPE_BK7221U
    None, #CHIP_BK3435_WriteDebug,		# CHIP_TYPE_BK7251
)

ReadDbug = (
    None, #CHIP_EXTERN_ReadDebug,		# EXTERN_FLASH
    None,			                    # CHIP_TYPE_BK7231
    None, #CHIP_BK3435_ReadDebug,		# CHIP_TYPE_BK7231U
    None, #CHIP_BK3435_ReadDebug,		# CHIP_TYPE_BK7221U
    None, #CHIP_BK3435_ReadDebug,		# CHIP_TYPE_BK7251
)

ConfigWrite = (
    None,			                    # EXTERN_FLASH
    None,			                    # CHIP_TYPE_BK7231
    None,			                    # CHIP_TYPE_BK7231U  //ex val = CHIP_BK3435_Config
    None,			                    # CHIP_TYPE_BK7221U  //ex val = CHIP_BK3435_Config
    None,			                    # CHIP_TYPE_BK7251  //ex val = CHIP_BK3435_Config
)

ConfigAnalyze = (
    None,			                    # EXTERN_FLASH
    None, #CHIP_BK3431s_Config,		    # CHIP_TYPE_BK7231
    None, #CHIP_BK3431s_Config,    	    # CHIP_TYPE_BK7231U 
    None, #CHIP_BK3431s_Config,		    # CHIP_TYPE_BK7221U
    None, #CHIP_BK3431s_Config,		    # CHIP_TYPE_BK7251
)

ConfigLoad = (
    None,			                    # EXTERN_FLASH
    None, #CHIP_BK7231_LoadConfig,		# CHIP_TYPE_BK7231
    None, #CHIP_BK7231_LoadConfig,		# CHIP_TYPE_BK7231U
    None,			                    # CHIP_TYPE_BK7221U
    None,			                    # CHIP_TYPE_BK7251
)

AddrCheck = (
    None,			                    # EXTERN_FLASH
    CHIP_BK7231_AddrCheck,		        # CHIP_TYPE_BK7231
    None,			                    # CHIP_TYPE_BK7231U
    None,			                    # CHIP_TYPE_BK7221U
    None,			                    # CHIP_TYPE_BK7251
)

def FlashSectorLengthBufGet(SelectChipNumb):
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
