# Install for Debian/Ubuntu/Linux Mint

## Installation

```
$ apt install python3-hid python3-serial python3-tqdm
$ python3 setup.py install --user
```

For other OS, you may use pip to install the requirements.

```
$ pip3 install -r requirements.txt --user
```


## SPI Usage

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
usage: uartprogram [-h] [-d DEVICE] [-s STARTADDR] [-b BAUDRATE] [-u] filename

Beken Uart Downloader.

positional arguments:
  filename              specify file_crc.bin

optional arguments:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
                        Uart device, default /dev/ttyUSB0
  -s STARTADDR, --startaddr STARTADDR
                        burn flash address, defaults to 0x11000
  -b BAUDRATE, --baudrate BAUDRATE
                        burn uart baudrate, defaults to 115200
  -u, --unprotect       unprotect flash first, used by BK7231N
```

* For chips exclude `BK7231N`, download address defaults to `0x11000`, **don't** set `-u` option.

* For `BK7231N`, set download address to `0x0`, and **set** `-u` option.

## Uart reader Usage

```
usage: uartreader [-h] [-d DEVICE] [-s STARTADDR] [-l READLENGTH] [-b BAUDRATE] filename

Beken Uart Flash Reader.

positional arguments:
  filename              Specify file to dump flash into

options:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
                        Uart device, default /dev/ttyUSB0
  -s STARTADDR, --startaddr STARTADDR
                        read flash address, defaults to 0
  -l READLENGTH, --readlength READLENGTH
                        read flash count in bytes, defaults to 2M Bytes
  -b BAUDRATE, --baudrate BAUDRATE
                        uart baudrate, defaults to 1500000
```

