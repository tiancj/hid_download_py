# What is this?

This repo is a fork of a Beken repo which can program BK7321 series devices over serial using the serial bootloader.

HID has been disabled so that you don't need to find the relevant libraries, to enable easy windows use.

It has been modified to

1/ Read flash

2/ unPackage and 'decrypt' a flash image

3/ spiprogram has been added - this works on a Raspberry pi using it's native SPI - see SPIFlash.md and rpi3install.md

* pairs with https://github.com/btsimonh/tuya-iotos-embeded-sdk-wifi-ble-bk7231t


# Install for Debian/Ubuntu/Linux Mint

## Installation

```
$ apt install python3-hid python3-serial python3-tqdm
$ python3 setup.py install --user
```

## Windows

Create a python virtual environment

run install.bat to install the needed packages


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
  -w, --write           read flash
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

