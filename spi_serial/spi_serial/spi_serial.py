import mraa as m
import time


class SpiSerial():
    def __init__(self):
        # read cpuinfo to determine hw
        f = file("/proc/cpuinfo")
        proc = ""
        for line in f:
            if "Intel" in line:
                proc = "Intel"
                break

        if "Intel" in proc:
            self.CS0 = 23
            self.SPI_FROM_DESC = "spi-raw-5-1"
            self.RST_PIN = 36
        else: # assume RPi
            self.CS0 = 24
            self.SPI_FROM_DESC = "spi-raw-0-0"
            self.RST_PIN = 7
        self.cs0 = m.Gpio(self.CS0)
        self.cs0.dir(m.DIR_OUT)
        self.cs0.write(1)

        self.dev = m.spiFromDesc(self.SPI_FROM_DESC)
        self.dev.frequency(62500)
        self.dev.mode(m.SPI_MODE0)
        self.dev.bitPerWord(8)
        self.timeout = 0
        self.rx_buf = []

    def spi_xfer(self, b):
        tx = bytearray(1)
        tx[0] = (int('{:08b}'.format(b)[::-1], 2))
        self.cs0.write(0)
        rxbuf = self.dev.write(tx)
        self.cs0.write(1)
        return (int('{:08b}'.format(rxbuf[0])[::-1], 2))

    def close(self):
        pass

    def write(self, tx_bytes):
        tx_bytes = bytearray(tx_bytes)
        self.spi_xfer(0x99)
        num_rxd = self.spi_xfer(len(tx_bytes))
        for y in range(0, len(tx_bytes)):
            rx = self.spi_xfer(tx_bytes[y])
            if num_rxd > 0:
                self.rx_buf.append(rx)
                num_rxd -= 1
        for y in range(0, num_rxd):
            rx = self.spi_xfer(0)
            self.rx_buf.append(rx)

    def read(self, num_bytes=0):
        if num_bytes == 0:
            num_bytes = len(self.rx_buf)
        ret_val = self.rx_buf[0:num_bytes]
        del(self.rx_buf[0:num_bytes])
        return ret_val

    def peek(self):
        return self.rx_buf[0]

    def pop(self):
        return self.read(1)

    def inWaiting(self):
        self.spi_xfer(0x99)
        num_rxd = self.spi_xfer(0)
        for y in range(0, num_rxd):
            rx = self.spi_xfer(0)
            self.rx_buf.append(rx)
        return len(self.rx_buf)

    def reset(self):
        self.RST = m.Gpio(self.RST_PIN)
        self.RST.dir(m.DIR_OUT)
        self.RST.write(0)   # reset the device
        time.sleep(0.01)
        self.RST.write(1)   # let the device out of reset
        time.sleep(2.01)    # wait for the CC1110 to come up
        # TODO: change the CC1110 code to not have a 2s delay
