# encoding: utf8
#
# Beken composite bin file parser
#
# Copyright (c) BekenCorp. (chunjian.tian@bekencorp.com).  All rights reserved.
#
# This software may be distributed under the terms of the BSD license.
# See README for more details.

from dataclasses import dataclass
from enum import Enum

from .crc32v2 import crc32_ver2


class BIN_TYPE(Enum):
    TYPE_NORMAL = 0
    TYPE_OTA = 1
    TYPE_BL1_ALL_BIN = 2
    TYPE_BL2_APP_BIN = 3
    TYPE_SECURE_FIX = 4
    TYPE_OUTTER_FLASH = 5
    TYPE_NORMAL_FIXED = 6


COMPOSITE_MAGICS = {
    b"beken...": BIN_TYPE.TYPE_OTA,
    b"BKDLV10.": BIN_TYPE.TYPE_BL2_APP_BIN,
    b"BL1DLV10": BIN_TYPE.TYPE_BL1_ALL_BIN,
    b"BLXDLV20": BIN_TYPE.TYPE_SECURE_FIX,
    b"QSPI_DL.": BIN_TYPE.TYPE_OUTTER_FLASH,
    b"BKFIXED.": BIN_TYPE.TYPE_NORMAL_FIXED,
    b"BL1DLV30": BIN_TYPE.TYPE_BL1_ALL_BIN,
}


@dataclass
class BinInfo:
    bCheck: bool = True
    bDataPort: bool = True
    sFilePath: str = ""
    iStartAddress: int = 0
    iFileCRC: int = 0
    iFileLength: int = 0
    iPartition_start: int = 0
    iPartition_size: int = 0
    pfile: bytes = b""


def _read_be32(buf, pos):
    return (
        (buf[pos] << 24)
        + (buf[pos + 1] << 16)
        + (buf[pos + 2] << 8)
        + buf[pos + 3]
    )


def _load_partition_bin(srcbuf, idx, link_bootrom=True):
    bin_info = BinInfo()
    bin_info.bCheck = True
    pos = 0x20 + 0x20 * idx
    bin_info.iPartition_start = _read_be32(srcbuf, pos)
    bin_info.iPartition_size = _read_be32(srcbuf, pos + 4)
    bin_info.iStartAddress = _read_be32(srcbuf, pos + 8)
    image_offset = _read_be32(srcbuf, pos + 12)
    file_len = _read_be32(srcbuf, pos + 16)
    port_type = (srcbuf[pos + 28] << 8) + srcbuf[pos + 29]
    bin_info.bDataPort = port_type == 0
    bin_info.pfile = srcbuf[image_offset : image_offset + file_len]
    padding_len = file_len % 0x100
    if padding_len:
        bin_info.pfile += b"\xff" * (0x100 - padding_len)
        file_len += 0x100 - padding_len
    bin_info.iFileLength = file_len
    bin_info.iFileCRC = crc32_ver2(0xFFFFFFFF, bin_info.pfile)
    return bin_info


def load_bl1_all_app_bin(srcbuf):
    bin_num = (srcbuf[18] << 8) + srcbuf[19]
    return [_load_partition_bin(srcbuf, idx) for idx in range(bin_num)]


def load_bl2_app_bin(srcbuf):
    bin_num = (srcbuf[18] << 8) + srcbuf[19]
    return [_load_partition_bin(srcbuf, idx, link_bootrom=False) for idx in range(bin_num)]


def load_secure_boot_bin(srcbuf):
    return load_bl1_all_app_bin(srcbuf)


def load_ota_bin(srcbuf):
    bin_list = []
    bin_num = (srcbuf[18] << 8) + srcbuf[19]
    for idx in range(bin_num):
        bin_info = BinInfo()
        bin_info.bCheck = True
        pos = 0x20 + 0x20 * idx
        file_len = _read_be32(srcbuf, pos)
        image_offset = _read_be32(srcbuf, pos + 4)
        bin_info.iStartAddress = _read_be32(srcbuf, pos + 8)
        bin_info.pfile = srcbuf[image_offset : image_offset + file_len]
        padding_len = file_len % 0x100
        if padding_len:
            bin_info.pfile += b"\xff" * (0x100 - padding_len)
            file_len += 0x100 - padding_len
        bin_info.iFileLength = file_len
        bin_info.iFileCRC = crc32_ver2(0xFFFFFFFF, bin_info.pfile)
        bin_list.append(bin_info)
    return bin_list


def load_normal_bin(srcbuf):
    bin_info = BinInfo()
    bin_info.bCheck = True
    bin_info.pfile = srcbuf
    buf_len = len(srcbuf)
    padding_len = buf_len % 0x100
    if padding_len:
        bin_info.pfile += b"\xff" * (0x100 - padding_len)
        buf_len += 0x100 - padding_len
    bin_info.iFileLength = buf_len
    bin_info.iFileCRC = crc32_ver2(0xFFFFFFFF, bin_info.pfile)
    return bin_info


def detect_bin_type(srcbuf):
    magic = srcbuf[:8]
    return COMPOSITE_MAGICS.get(magic, BIN_TYPE.TYPE_NORMAL)


def load_bin_file(path, startaddr=0, oplen=0):
    with open(path, "rb") as f:
        srcbuf = f.read()

    bin_type = detect_bin_type(srcbuf)
    if bin_type == BIN_TYPE.TYPE_OTA:
        bin_list = load_ota_bin(srcbuf)
    elif bin_type == BIN_TYPE.TYPE_BL2_APP_BIN:
        bin_list = load_bl2_app_bin(srcbuf)
    elif bin_type in (
        BIN_TYPE.TYPE_BL1_ALL_BIN,
        BIN_TYPE.TYPE_SECURE_FIX,
        BIN_TYPE.TYPE_OUTTER_FLASH,
        BIN_TYPE.TYPE_NORMAL_FIXED,
    ):
        bin_list = load_bl1_all_app_bin(srcbuf)
    else:
        bininfo = load_normal_bin(srcbuf)
        bininfo.iStartAddress = startaddr
        if 0 < oplen < len(srcbuf):
            bininfo.iFileLength = oplen
            bininfo.pfile = bininfo.pfile[:oplen]
        bininfo.sFilePath = path
        bin_list = [bininfo]

    for item in bin_list:
        if not item.sFilePath:
            item.sFilePath = path
    return bin_type, bin_list


def parse_binfile_info(main_bin, start_addr=0):
    bin_type, bin_list = load_bin_file(main_bin, start_addr)
    return bin_type, bin_list, [main_bin]


def format_bin_info(bin_type, bin_list):
    lines = []
    magic = bin_type.name if bin_type != BIN_TYPE.TYPE_NORMAL else "TYPE_NORMAL"
    lines.append(f"bin type: {magic}, partition count: {len(bin_list)}")
    for idx, item in enumerate(bin_list):
        port = "dbus" if item.bDataPort else "cbus"
        lines.append(
            f"[{idx}] partition: 0x{item.iPartition_start:x}/0x{item.iPartition_size:x}, "
            f"start: 0x{item.iStartAddress:x}, length: 0x{item.iFileLength:x}, port: {port}"
        )
    return lines


def select_partitions(bin_list, partition_spec):
    if partition_spec is None:
        return bin_list
    indices = []
    for part in partition_spec.split(","):
        part = part.strip()
        if not part:
            continue
        indices.append(int(part))
    selected = []
    for idx in indices:
        if idx < 0 or idx >= len(bin_list):
            raise ValueError(f"partition index {idx} out of range (0-{len(bin_list) - 1})")
        selected.append(bin_list[idx])
    return selected
