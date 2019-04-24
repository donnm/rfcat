# setup.py
from setuptools import setup

setup(name="spi_serial",
      version="0.0",
      description="Intel Edison SPI Serial",
      url="https://github.com/EnhancedRadioDevices/915MHzEdisonExplorer_SW",
      author="Morgan Redfield",
      author_email="morgan@enhancedradio.com",
      packages=["spi_serial"],
      scripts=['scripts/reset_spi_serial.py']
      )
