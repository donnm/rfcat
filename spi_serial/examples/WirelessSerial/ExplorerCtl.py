
import spi_serial
import time

# accept user input and send it to the CC1110
if __name__ == "__main__":
    ss = spi_serial.SpiSerial()

    while True:
        ss.reset()
        try:
            cmd = raw_input()
            cmd = [int(c) for c in cmd.split(',')]
            if cmd[0] != 0:
                ss.write(cmd)
            time.sleep(0.025)
            if ss.inWaiting() > 0:
                print(ss.read(0))
        except:
            break
