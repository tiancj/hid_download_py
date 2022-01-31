# NOTE- THIS REPO HAS MOVE TO https://github.com/OpenBekenIOT



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
                        burn uart baudrate, defaults to 1500000
  -u, --unprotect       unprotect flash first, used by BK7231N
  -r, --read            read flash
  -w, --write           read flash
  -p, --unpackage       unPackage firmware
```

* For chips exclude `BK7231N`, download address defaults to `0x11000`, **don't** set `-u` option.

* For `BK7231N`, set download address to `0x0`, and **set** `-u` option.


## examples:

* baud rate can be modified for faster/slower, e.g. -b 115200 for more reliable with dodgy connections

# flash

run this, then re-power the unit, repeating until the flashing starts

`python uartprogram C:\DataNoBackup\tuya\tuya-iotos-embeded-sdk-wifi-ble-bk7231t\apps\simon_light_pwm_demo\output\1.0.0\simon_light_pwm_demo_UA_1.0.0.bin -d com4 -w`

# read

`python uartprogram firmware.bin -d com4 -r`

# unpackage

`python uartprogram firmware.bin -p`

