# installing the spiprogram on RPI3b

My fresh install of Raspberry PI OS has Python 3.9.2

let's us a python environment and other deps:

```
sudo apt-get install python3-dev
sudo apt-get install python3-venv
python -m venv env
source env/bin/activate
```

now the dependencies into the environment.

Note: for RPi.GPIO, something special seems needed...

```
python3 -m pip install pyserial tqdm spidev
env CFLAGS="-fcommon" python3 -m pip install rpi.gpio
```

# example spiprogram usage:

python spiprogram -s 0x0 -w test.bin

python spiprogram -s 0x0 -l 0xf000 -r testreread.bin
