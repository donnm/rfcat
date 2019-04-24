import time
import spi_serial

if __name__ == "__main__":
    ss = spi_serial.SpiSerial()
    ss.reset()

    cmd = [1]
    ss.write(cmd)
    if ss.inWaiting() > 0:
        print(''.join(chr(k) for k in ss.read(0)))
    cmd = [2]
    ss.write(cmd)
    if ss.inWaiting() > 0:
        print(''.join(chr(k) for k in ss.read(0)))
    cmd = [8, 1, 1]
    ss.write(cmd)
    if ss.inWaiting() > 0:
        print(''.join(chr(k) for k in ss.read(0)))
