# Pyserial based serial library
import serial
import struct
import logging
from threading import Lock
from enum import Enum

from .errors import ChecksumError, ReadError, WriteError


class Type(Enum):
    STX = 0x02
    ETX = 0x03
    HANDSHAKE_SYN = 0x04
    HANDSHAKE_ACK = 0x05
    ESC = 0x1b


class Serial:
    """ Serial made for humans 😎 """

    def __init__(self, port=None, baud=9600, timeout=2):
        # Let's setup the serial
        self._serial = serial.Serial()
        self.port = port
        self.baudrate = baud
        self.timeout = timeout
        # Mutex to handle concurrency during reads/closing serial
        self.__mutex = Lock()
        # Pyserial doesn't provide a buffered serial reader...
        # We need to do it ourselves
        self._buffer = bytearray()
        import sys
        self.__logger = logging.getLogger(__name__)

    def __del__(self):
        if self._serial.port is not None and self._serial.is_open:
            self._serial.reset_input_buffer()
            self._serial.reset_output_buffer()
        self.close()

    def __str__(self):
        return "EasySerial connected to port {} with baud {}" \
            .format(str(self._serial.port), str(self._serial.baudrate))

    def __repr__(self):
        return """EasySerial stats:
        Port {}
        Baud {}
        """.format(str(self._serial.port), str(self._serial.baudrate))

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *exc):
        self.close()

    @property
    def port(self):
        return self._serial.port

    @port.setter
    def port(self, value):
        self._serial.port = value

    @property
    def baudrate(self):
        return self._serial.baudrate

    @baudrate.setter
    def baudrate(self, value):
        self._serial.baudrate = value

    @property
    def timeout(self):
        return self._serial.timeout

    @timeout.setter
    def timeout(self, value):
        self._serial.timeout = value

    def open(self):
        """Tries to open the serial

        Returns:
            A tuple (isOpen, message/exception)
        """
        try:
            self._serial.open()
        except serial.SerialException as e:
            return (False, str(e))
        return (True, "Serial opened successfully")

    def close(self):
        "Gracefully closes the serial"
        self.__mutex.acquire(blocking=True)
        self._serial.close()
        self.__mutex.release()

    def flush(self, input=True, output=True):
        self.__mutex.acquire(blocking=True)
        try:
            if input:
                self._serial.reset_input_buffer()
                self._buffer.clear()
            if output:
                self._serial.reset_output_buffer()
        finally:
            self.__mutex.release()


    def read(self, tries=float('inf')):
        """Low level read from serial

        Args:
            tries: how many attempts to try to read from serial

        Returns:
            The read package
        """

        # The buffer may already contain a readable package
        # If so there is no need to read from the serial yet
        start = self._buffer.find(Type.STX.value)
        end = self._buffer.find(Type.ETX.value)

        # The package must be properly escaped
        if end > start and self.__checkETX(self._buffer[start:end+1]):
            r = self._buffer[start:end+1]
            self._buffer = self._buffer[end+1:]
            return r

        # Counter to keep track of how many times we attempt to read a full package from the serial
        read_attempts = 0
        # Since ETX is 0x03 it is quite common to find it in the payload.
        # Everytime we find a possible package we must check if it is correctly escaped
        # If it isn't we keep track of the last ETX index and skip to the next one
        end_index = -1

        while self._serial.is_open and read_attempts < tries:
            # Let's read 1 byte or more if there are several bytes pending
            read_attempts += 1
            self.__mutex.acquire(blocking=True)
            try:
                i = max(1, min(2048, self._serial.in_waiting))
                data = self._serial.read(i)
            except:
                continue
            finally:
                self.__mutex.release()
            self._buffer.extend(data)

            try:
                # Let's find the start and end indexes
                start = self._buffer.index(Type.STX.value)
                end = self._buffer.index(Type.ETX.value, max(start, end_index))
                end_index = end + 1
            except:
                # If the buffer doesn't contain a full package then let's read again
                continue

            # Let's check if the package is correctly escaped
            if self.__checkETX(self._buffer[start:end+1]):
                r = self._buffer[start:end+1]
                self._buffer = self._buffer[end+1:]
                return r

    def read_package(self, tries=float('inf')):
        """Easy wrapper for reading a full package from serial

        Args:
            tries: how many attempts to try to read from serial

        Returns:
            A tuple (package_type, payload)

        Raises:
            ReadError: max number of attempts reached
            ChecksumError: checksum error
        """

        data = self.read(tries=tries)

        if data is None:
            raise ReadError

        payload = self.__unescape(data[2:-1])

        # Let's check if the checksum is correct
        chs = self.__checksum(payload[:-1])
        if chs != payload[-1]:
            raise ChecksumError

        package_type = data[1]
        return (package_type, payload[:-1])

    def write_float(self, type, payload):
        """Writes the package to serial

        Args:
            package: a bytearray object
            toEscape: if True the package will be escaped

        Returns:
            The length of the written package

        Raises:
            TypeError: the package isn't a bytearray
        """

        package = bytearray()
        package.append(Type.STX.value)  # adding the STX byte
        package.append(type)            # adding the Type byte

        payload = struct.pack('<f', payload)
        payload = self.__escape(payload)
        for i in range(0, len(payload)):
            package.append(payload[i])

        package.append(Type.ETX.value)  # appending ETX
        return self.write_package(package)
    
    def write_package(self, package):
    
        if not isinstance(package, bytearray):
            raise TypeError

        return self._serial.write(package)

    def handshake(self):
        """Basic implementation of a two-way handshake
        """
        import time

        synPkg = bytearray([Type.STX.value, Type.HANDSHAKE_SYN.value, Type.ETX.value])
        while self._serial.is_open:
            self.__logger.debug("Trying handhsake... ")
            self.flush()
            self.write(synPkg, toEscape=False)

            time.sleep(1)

            data = self.read(tries=1)

            if data is None:
                self.__logger.debug("Read nothing.")
                continue

            if data[1] == Type.HANDSHAKE_ACK.value:
                self.__logger.info("Connection established!")
                break
            else:
                self.__logger.error("Received error, reset the board!")
                time.sleep(1)

    def __checkETX(self, bytes):
        if len(bytes) < 2 or bytes[-1] != Type.ETX.value:
            return False
        i = 2
        escaped = False
        while bytes[-i] == Type.ESC.value:
            escaped = not escaped
            i = i + 1
        return not escaped

    def __escape(self, data):
        b = bytearray()
        for i in range(len(data)):
            if data[i] == Type.STX.value or data[i] == Type.ETX.value or data[i] == Type.ESC.value:
                b.append(Type.ESC.value)
            b.append(data[i])
        return b

    def __checksum(self, data):
        """ Checksum: sum of payload % 255 """
        check = 0
        for b in data:
            check = check + b
        return check % 0xff

    def __unescape(self, b):
        data = bytearray()
        i = 0
        while i < len(b):
            if b[i] == Type.ESC.value and i+1 < len(b):
                data.append(b[i+1])
                i = i+2
            else:
                data.append(b[i])
                i = i+1

        return data
