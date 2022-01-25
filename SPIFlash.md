# BK7231S Flash via SPI

This is useful if you accidentally overwrite the bootloader.

This procedure was tested on an RPI3b having enabled SPI in raspi-config.

Connections:

```
CEN - Chip enable (reset) -> GPIO22
P20 - SCLK -> SCLK
P21 - FLASH CSN -> SPI CE0
P22 - FLASH SI -> SPI MOSI
P23 - FLASH SO -> SPI MISO
SPI Mode 3
SPI Rate 50000
```

## Enabling SPI Flash

set GPIO22 (CEN) to low.

Wait 1s.

set GPIO22 (CEN) to high.

Send 250 'D2'

Expected response:

First byte D2, 249 x 00


The MCU is now in SPI flashing mode, and will remain in this state (until power off, or maybe toggle of CEN?).

Test by sending

`9F 00 00 00`
->
`00 15 70 1C`

This is the ID of an EN25QH16B - data sheet here: https://datasheetspdf.com/datasheet/EN25QH16B.html


## Reading the flash

data may be read in chunks of 256 bytes using cmd 03:

`03 (addr>>16 & 0xFF) (addr>>8 & 0xFF) (addr & 0xFF) <256 x 00>`

The data read in this way is from the raw flash.  Executable partitions on the BK7231 may/will be both packaged and encrypted.


## writing the flash

Writing consists of erasing sectors and then writing data.

As it is writing the faw flash, executable partitions must be encrypted and packaged (32->34 bytes with CRC).

From the Tuya SDK, the firmware file tagged '_QIO_' is suitable.  e.g. to replace the bootloader, flash the first 0xf000 bytes from that firmware file.

Each command must raise CSN at the end to take effect, so all commands must be sent separately over SPI.

A sector is 0x1000 bytes, writing is max 256 bytes per page.

Procedure:

Enable write (must be done before each erase or write):

`06`

Erase sector:

`20 (addr>>16 & 0xFF) (addr>>8 & 0xFF) (addr & 0xFF)`

Wait for Erase to complete:

`05 00`

Repeat until bit 0 of the second byte returns clear.

Enable write (must be done before each erase or write):

`06`

Write data:

`03 (addr>>16 & 0xFF) (addr>>8 & 0xFF) (addr & 0xFF) <up to 256 bytes of data>`

Note that there are 4 writes to each erase.  If you call erase with a write addr not on a 0x1000 boundary, it will erase the sector starting on the relevant 0x1000 boundary.



## Additional notes:

At first, I attempted this from Espruino on ESP32.  That was not successful, and I'm still not sure why.
