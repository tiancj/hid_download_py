# Install for Debian/Ubuntu/Linux Mint
```
apt install python3-hid
python3 setup.py install --user
```

# Usage

```
./bekenprogram.py -h
usage: bekenprogram.py [-h] [-c {bk7231,bk7231u,bk7221u,bk7251}] filename

Beken HID Downloader.

positional arguments:
  filename              specify file_crc.bin

optional arguments:
  -h, --help            show this help message and exit
  -c {bk7231,bk7231u,bk7221u,bk7251}, --chip {bk7231,bk7231u,bk7221u,bk7251}
                        chip type
```

