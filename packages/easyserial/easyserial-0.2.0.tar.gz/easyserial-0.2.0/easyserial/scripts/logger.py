import easyserial
import serial
import argparse
import signal
from datetime import datetime
import csv
import struct
import itertools
import sys
import time
from threading import Thread

running = True

def spinner_loop():
    spinner = itertools.cycle(["-", "\\", "|", "/"])
    while running:
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')
        time.sleep(0.2)


spinner_thread = Thread(target=spinner_loop, daemon=True)

def stop(sig, frame):
    global running
    running = False
    if spinner_thread.is_alive():
        spinner_thread.join()
    print("")

def get_port():
    from serial.tools.list_ports import comports
    ports=[]
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
        print('- {:2}: {:20} {!r}'.format(n, port, desc))
        ports.append(port)

    if len(ports) == 0:
    	print("No serial device found!")
    	exit(0)

    while running:
        port = input("Enter port index: ")
        try:
            index = int(port) - 1
            if not 0 <= index < len(ports):
                print('--- Invalid index!')
                continue
        except ValueError:
            pass
        else:
            port = ports[index]
        return port

def get_baud():
    baud = None
    while running and baud is None:
        try:
            baud = int(input("Enter baudrate: "))
            if baud <= 0:
                baud = None
        except ValueError:
            print("--- Invalid value. Try again!")
    return baud


def main(port=None, baud=None):

    signal.signal(signal.SIGINT, stop)

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=str)
    parser.add_argument("-b", "--baud", type=int)
    args = parser.parse_args()

    port = args.port
    baud = args.baud

    if port is None:
        port = get_port()

    if baud is None:
        baud = get_baud()

    print("--- Logger on {} {} ---".format(port, baud))
    default_filename = "log" + datetime.now().strftime("-%Y-%m-%d-%H-%M-%S") + ".csv"
    filename = input("Enter a valid filename ({}): ".format(default_filename))
    if not filename.strip():
        filename = default_filename
    print("Saving logs to: {}".format(filename))

    global running
    with easyserial.Serial(port=port, baud=baud) as serial:
        with open(filename, mode='w', newline='\n', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            serial.handshake()
            print("Logging... press CTRL+C to stop at anytime ", end="")
            spinner_thread.start()
            while running:
                try:
                    ptype, payload = serial.read_package(tries=5)
                except easyserial.ChecksumError:
                    continue
                except easyserial.ReadError:
                    continue
                if ptype == 0x00:
                    try:
                        result = struct.unpack('<'+'f'*int(len(payload)/4), payload)
                    except struct.error:
                        continue
                    writer.writerow(result)


if __name__ == "__main__":

    main()
