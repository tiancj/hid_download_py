#!/usr/bin/env python3
import sys
import bkutils

if len(sys.argv) < 2:
    print('Usage: {} <filename>'.format(sys.argv[0]))
    sys.exit(-1)

downloader = bkutils.HidDownloader(bkutils.CHIP_TYPE_BK7231U, sys.argv[1])
downloader.DownloadProc()
