# Easy Serial 😎

## What is this?

This is a thread safe Python3 implementation of an high level serial protocol currently used in the Forecast project.

This package core functionality is to grant ease of use to end users unfamiliar with the protocol through different layers of abstraction. It is currently built on top of the more known library PySerial, which offers an easy interface to compliant posix/win32 serials.

A simple logger script is also included, which is callable from console:
```
easyserial-logger
```
or
```
easyserial-logger -p <PORT> -b <BAUDRATE>
```

## Installation

### From pypi

```
pip install easyserial
```

### From source

- Clone the repository
- Run the following commands
```bash
cd easy-serial

# Using pipenv
pipenv install

# or just using pip
pip install -e .
```

## Example

```python
import easyserial

port = "/dev/ttyACM0"
baudrate = 115200

with easyserial.Serial(port=port, baud=baudrate) as serial:

    # Read package example
    # tries specifies the number of attempts to read from serial a full package (default: infinite)
    package_type, payload = serial.read_package(tries=1)

    # In case you want to skip unescaping and checksum checks
    package = serial.read(tries=1)

    # In order to write to serial
    serial.write(package)

```