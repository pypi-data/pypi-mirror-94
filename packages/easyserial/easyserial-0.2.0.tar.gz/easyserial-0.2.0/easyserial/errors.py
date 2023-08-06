class SerialError(Exception):
    """Base class for exceptions"""

    def __init__(self):
        self.message = "Serial error"

    def __str__(self):
        return self.message


class ChecksumError(SerialError):

    def __init__(self):
        self.message = "Checksum error"


class ReadError(SerialError):

    def __init__(self):
        self.message = "Didn't retrieve any package from the serial"


class WriteError(SerialError):

    def __init__(self):
        self.message = "Didn't retrieve any package from the serial"
