# hid_download_py

Beken chip flash tools over UART and HID.

## Installation

### pipx (recommended, global CLI)

Best for installing command-line tools such as `uartprogram`, `hidprogram`, and `uartreader`. Each tool runs in its own virtual environment without polluting system Python.

```bash
# Install from source
pipx install .

# Or install from a wheel
uv build
pipx install dist/hid_downloader-1.0-py3-none-any.whl
```

Upgrade / uninstall:

```bash
pipx upgrade hid_downloader
pipx uninstall hid_downloader
```

### uv (project development)

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

### pip (traditional)

Debian/Ubuntu/Linux Mint:

```bash
apt install python3-hid python3-serial python3-tqdm
pip3 install . --user
```

Other systems:

```bash
pip3 install -r requirements.txt --user
pip3 install . --user
```

## Build

Build with [uv](https://github.com/astral-sh/uv):

```bash
uv build
```

Artifacts are written to `dist/`:

- `hid_downloader-1.0-py3-none-any.whl`
- `hid_downloader-1.0.tar.gz`

If fetching build dependencies times out, install `setuptools` first:

```bash
uv pip install setuptools
uv build --no-build-isolation
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
usage: uartprogram [-h] [-d DEVICE] [-s STARTADDR] [-b BAUDRATE] [-u] [-e]
                   [-i] [-p PARTITION] [-v] [filename]

Beken Uart Downloader.

positional arguments:
  filename              specify file_crc.bin or all-app.bin if -e is not provided

options:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
                        Uart device, default to /dev/ttyUSB0
  -s STARTADDR, --startaddr STARTADDR
                        burn flash address for normal bin, defaults to 0x11000
  -b BAUDRATE, --baudrate BAUDRATE
                        burn uart baudrate, defaults to 2000000
  -u, --unprotect       unprotect flash first, used by BK7231N
  -e, --erase           Erase chip
  -i, --info            Show partition info for composite bin such as all-app.bin
  -p PARTITION, --partition PARTITION
                        Flash selected partitions only, e.g. 0,2,4
  -v, --verbose         Print partition info while flashing
```

Examples:

```bash
# Show partition info for all-app.bin
uartprogram -i all-app.bin

# Flash a composite firmware (e.g. all-app.bin)
uartprogram -u all-app.bin

# Flash selected partitions only
uartprogram -u -p 0,2 all-app.bin
```

* For chips other than `BK7231N`, the default download address is `0x11000`. Do **not** use `-u`.

* For `BK7231N`, set the download address to `0x0` and use `-u`.

* Composite firmware (e.g. `all-app.bin` in `BL1DLV10` format) is flashed by partition address automatically; `-s` is ignored.

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
