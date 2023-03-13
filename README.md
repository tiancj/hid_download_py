# What is this?

This repo is a fork of a Beken repo which can program BK7321 series devices over serial using the serial bootloader.

It is mostly used to flash our Tasmota replacement on BK7231T/BK7231N, for details see here:

https://github.com/openshwprojects/OpenBK7231T_App

HID has been disabled so that you don't need to find the relevant libraries, to enable easy windows use.

It has been modified to

1/ Read flash

2/ unPackage and 'decrypt' a flash image

3/ spiprogram has been added - this works on a Raspberry pi using it's native SPI - see SPIFlash.md and rpi3install.md

# [Youtube guide for flashing BK7231N with hid_download_py](https://www.youtube.com/watch?v=2e1SUQNMrgY&ab_channel=Elektrodacom)
You can also check our other videos related to flashing IoT devices.

# Blog post about BK7231N flashing by Zorruno

https://zorruno.com/2022/zemismart-ks-811-with-openbk7231n-openbeken/

# Detailed examples of flashing Beken chips

Please see our detailed step by step guides for more information:

https://www.elektroda.com/rtvforum/topic3880540.html

https://www.elektroda.com/rtvforum/topic3875654.html

https://www.elektroda.com/rtvforum/topic3874289.html

# Install for Debian/Ubuntu/Linux Mint

## Installation

```shell
$ apt install python3-hid python3-serial python3-tqdm
$ python3 setup.py install --user
```

Or use `requirements.txt` with `pip`:

```shell
# If you use mkvenv, it will pick up the requirements.txt for you
$ mkvenv
Creating hid_download_py-master-uD7eej0e virtualenv
created virtual environment CPython3.10.8.final.0-64 in 86ms
<...>
Found a requirements.txt file. Install? [y/N]: Y
Collecting hid
  Using cached hid-1.0.5-py3-none-any.whl
Collecting pyserial
  Using cached pyserial-3.5-py2.py3-none-any.whl (90 kB)
Collecting tqdm
  Using cached tqdm-4.64.1-py2.py3-none-any.whl (78 kB)
Installing collected packages: pyserial, hid, tqdm
Successfully installed hid-1.0.5 pyserial-3.5 tqdm-4.64.1
# Or with regular `pip`
$ pip3 install -r requirements.txt
Collecting hid
  Using cached hid-1.0.5-py3-none-any.whl
Collecting pyserial
  Using cached pyserial-3.5-py2.py3-none-any.whl (90 kB)
Collecting tqdm
  Using cached tqdm-4.64.1-py2.py3-none-any.whl (78 kB)
Installing collected packages: pyserial, hid, tqdm
Successfully installed hid-1.0.5 pyserial-3.5 tqdm-4.64.1
```

## Windows

* Download hidapi from https://github.com/libusb/hidapi/releases, extrat it to somewhere in windows %PATH%
* Create a python virtual environment

* run `install.bat` to install the needed packages


## SPI Usage

see SPIFlash.md for instructions on how to unbrick devices using a raspberry pi...


## HID Usage

(disabled in this repo)

```
hidprogram -h
usage: hidprogram [-h] [-c {bk7231,bk7231s,bk7231u,bk7221u,bk7251}] [-m {soft,hard}] filename

Beken HID Downloader.

positional arguments:
  filename              specify file_crc.bin

optional arguments:
  -h, --help            show this help message and exit
  -c {bk7231,bk7231s,bk7231u,bk7221u,bk7251}, --chip {bk7231,bk7231s,bk7231u,bk7221u,bk7251}
                        chip type
  -m {soft,hard}, --mode {soft,hard}
```



## Uart downloader Usage

```
usage: uartprogram [-h] [-d DEVICE] [-s STARTADDR] [-l LENGTH] [-b BAUDRATE]
                   [-u] [-r] [-w] [-p]
                   filename

Beken Uart Downloader.

positional arguments:
  filename              specify file_crc.bin

optional arguments:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
                        Uart device, default /dev/ttyUSB0
  -s STARTADDR, --startaddr STARTADDR
                        burn flash address, defaults to 0x11000
  -l LENGTH, --length LENGTH
                        length to read, defaults to 0x1000
  -b BAUDRATE, --baudrate BAUDRATE
                        burn uart baudrate, defaults to 921600
  -u, --unprotect       unprotect flash first, used by BK7231N
  -r, --read            read flash
  -w, --write           write flash
  -p, --unpackage       unPackage firmware
```

* For chips exclude `BK7231N`, download address defaults to `0x11000`, **don't** set `-u` option.

* For `BK7231N`, set download address to `0x0`, and **set** `-u` option.

* note that the default baud rate is 921600 - it connects first at 115200, then sends a command to change the baudrate.  So if you get a connection, but then 'Set Baudrate Failed', it could be that your connections/uart are not capable of the default 921600 baud, so try a lower one.  If you get 'write sector failed', this can also be a mis-communication, so lower the baud rate.  Common 'faster' baud rates are 115200, 230400, 460800, 576000, 921600, 1500000.  uartprogram's default used to be 1.5Mbit, but we reduced it to 921600 for better reliability - but this may still be too high for some USB devices & connections.

## examples:

* baud rate can be modified for faster/slower, e.g. -b 115200 for more reliable with dodgy connections

# flash

run this, then re-power the unit, repeating until the flashing starts

`python uartprogram C:\DataNoBackup\tuya\tuya-iotos-embeded-sdk-wifi-ble-bk7231t\apps\simon_light_pwm_demo\output\1.0.0\simon_light_pwm_demo_UA_1.0.0.bin -d com4 -w`

# read

`python uartprogram firmware.bin -d com4 -r`

# unpackage

`python uartprogram firmware.bin -p`

