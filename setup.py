from distutils.core import setup

setup(name="hid_downloader",
    version="0.99",
    description="HID Download tool",
    author="tiancj",
    author_email="cj.tian.seu@gmail.com",
    maintainer="tiancj",
    maintainer_email="cj.tian.seu@gmail.com",
    url="https://github.com/tiancj",
    license="MIT",
    requires=["hid"],
    platforms=["Windows", "GNU/Linux", "Darwin"],
    packages=['bkutils', 'bkutils/chip'],
    scripts=['bekenprogram'])

