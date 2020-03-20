import time

def _Thread_programm_7231(startAddr, fileLen, pfile):
    # do_reset_signal()

    reboot = "reboot"

    Start_Cmd(reboot)
    time.sleep(0.1)

    # Link Check
    while True:
        r = LinkCheck()
        if r > 0:
            break
        Start_Cmd(reboot)
        time.sleep(0.1)

    print("Gotten Bus...")

    # Set baudrate
    SetBR(115200)

    # Erase
    eraseAddr = startAddr
    len0 = (eraseAddr + 0xffff) & 0xffff0000
    len1 = (eraseAddr + fileLen + 0xfff) & 0xfffff000
    s0 = eraseAddr & 0xfffff000
    ss = s0

    # 如果写入地址不是4K对齐的，则计算第一次写入的地址和写入长度
    if eraseAddr & 0xfff:
        print("Aligning Flash Address...")
        l = 0x1000 - (eraseAddr & 0xfff)
        buf = ReadSector(s0)
        fl = fileLen
        if l < fileLen:
            fl = l
        buf[eraseAddr&0xfff:] = pfile[:eraseAddr&0xfff]
        EraseBlock(0x20, s0)

        WriteSector(s0, buf)

        fileSPtr += fl
        filOLen -= fl

        s0 = s0 + 0x1000
        ss = s0

        if filOLen<=0:
            # TODO: goto crc check
            pass
        
    # 文件结束地址
    filEPtr = fileLen
    s1 = eraseAddr + fileLen
    if s1 & 0xfff:
        buf = bytearray(b'\xff'*4096)
        buf[:filEPtr-(s1&0xfff)] = pfile[filEPtr-(s1&0xfff):]  # copy s1&0xfff len
        EraseBlock(0x20, s1&0xfffff000)
        WriteSector(s1&0xfffff000, buf)
        filEPtr = filEPtr - (s1&0xfff) 
        filOLen = filOLen - (s1&0xfff) 
        if filOLen <= 0:
            # TODO: goto crc check
            pass

    len1 = s0 + filOLen #结束地址
    # 对齐64KB，如果擦除区域小于64KB
    len0 = s0 & 0xffff0000
    if s0 & 0xffff:
        len0 = len0 + 0x10000
    if filOLen > len0 - s0:
        while s0 < len0:
            rmn = len0 - s0
            EraseBlock(0x20, s0)
            s0 = s0 + 0x1000

    
    # 按照64KB block擦除
    len1 = ss + filOLen
    while s0 < len1:
        print("Erasing Flash {}".format(100*s0//len1))
        rmn = len1 - s0
        if rmn > 0x10000:
            EraseBlock(0xd8, s0)
            s0 = s0+0x10000
        else:
            EraseBlock(0x20, s0)
            s0 = s0 + 0x1000


    el = 0x10000*4
    i = 0
    while i < fileOLen:
        print("Writing Flash {}".format(100*i//fileOLen))
        WriteSector(ss+i, pfile[filSPtr+i:filSPtr+i+4*1024])
        i += 0x1000

    # CRC check
    print("Verifing Flash")
    crc = ReadCRC(startAddr, fileLen)

