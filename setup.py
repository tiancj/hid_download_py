from distutils.core import setup

setup(name="hid_downloader",
    version="1.0",
    description="HID Download tool",
    author="tiancj",
    author_email="cj.tian.seu@gmail.com",
    maintainer="tiancj",
    maintainer_email="cj.tian.seu@gmail.com",
    url="https://github.com/tiancj",
    license="MIT",
    requires=["hid", "pyserial", "tqdm"],
    platforms=["Windows", "GNU/Linux", "Darwin"],
    packages=['bkutils', 'bkutils/chip'],
    scripts=['hidprogram', 'uartprogram'])

