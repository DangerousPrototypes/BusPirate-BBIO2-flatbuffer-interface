# BPIO2 Python Library

A Python library for interfacing with the Bus Pirate using the binary mode flat buffer interface (BPIO2).

Full documentation is available at [BPIO2 Documentation](https://docs.buspirate.com/docs/binmode-reference/protocol-bpio2/#python-library).
## Installation

Clone this repository:
```bash
git clone <repository-url>
cd bpio2/python
```

Install required dependencies:
```bash
pip3 install -r requirements.txt
```

## Setup

Ensure you have the latest Bus Pirate firmware with BPIO2 support.
In the Bus Pirate terminal enable the BPIO2 binary mode:
```bash
>binmode
```
Choose **BBIO2** as the binary mode, optionally save it as the default mode.

## Examples and Scripts

### hello_world

BPIO2 Hello World Example

**File:** `hello_world.py`

```
usage: hello_world.py [-h] -p PORT

BPIO2 I2C Example - Basic configuration and status display

options:
  -h, --help       show this help message and exit
  -p, --port PORT  Serial port (e.g., COM3, /dev/ttyUSB0)

Examples:
  hello_world.py -p COM3 # Enter I2C mode, configure settings, display status
```

### i2c_example

BPIO2 I2C Example - Read from 24x02 EEPROM

**File:** `i2c_example.py`

```
usage: i2c_example.py [-h] -p PORT [--device DEVICE] [--register REGISTER]
                      [--bytes BYTES] [--dump]

BPIO2 I2C Example -Read from 24x02 EEPROM

options:
  -h, --help           show this help message and exit
  -p, --port PORT      Serial port (e.g., COM3, /dev/ttyUSB0)
  --device DEVICE      I2C device address (default: 0xA0)
  --register REGISTER  Register address to read from (default: 0x00)
  --bytes BYTES        Number of bytes to read (default: 8)
  --dump               Dump entire EEPROM contents

Examples:
  i2c_example.py -p COM3                           # Basic read from default EEPROM
  i2c_example.py -p COM3 --device 0x50             # Read from device at 0x50
  i2c_example.py -p COM3 --register 0x10 --bytes 4 # Read 4 bytes from register 0x10
```

### onewire_example

BPIO2 1-Wire Example - Read temperature from DS18B20 sensor

**File:** `onewire_example.py`

```
usage: onewire_example.py [-h] -p PORT [--voltage VOLTAGE] [--search]

BPIO2 1-Wire Example - Communicate with 1-Wire devices

options:
  -h, --help         show this help message and exit
  -p, --port PORT    Serial port (e.g., COM3, /dev/ttyUSB0)
  --voltage VOLTAGE  Supply voltage in mV (default: 5000)
  --search           Search for devices instead of reading temperature

Examples:
  onewire_example.py -p COM3                    # Read temperature from DS18B20
  onewire_example.py -p COM3 --voltage 3300     # Use 3.3V supply voltage
  onewire_example.py -p COM3 --search           # Search for devices on bus
```

### spi_example

BPIO2 SPI Example - Read flash memory JEDEC ID

**File:** `spi_example.py`

```
usage: spi_example.py [-h] -p PORT [--speed SPEED] [--status]

BPIO2 SPI Example - Communicate with SPI flash memory

options:
  -h, --help       show this help message and exit
  -p, --port PORT  Serial port (e.g., COM3, /dev/ttyUSB0)
  --speed SPEED    SPI clock speed in Hz (default: 1000000)
  --status         Read status register instead of JEDEC ID

Examples:
  spi_example.py -p COM3                    # Read JEDEC ID at 1MHz
  spi_example.py -p COM3 --speed 10000000   # Read JEDEC ID at 10MHz
  spi_example.py -p COM3 --status           # Read status register
```

### spi_flash_read

BPIO2 SPI Flash Reader - Read SPI flash memory to file

**File:** `spi_flash_read.py`

```
usage: spi_flash_read.py [-h] -p PORT -o OUTPUT [--size SIZE] [--speed SPEED]
                         [--chunk CHUNK]

BPIO2 SPI Flash Reader - Read flash memory to file

options:
  -h, --help           show this help message and exit
  -p, --port PORT      Serial port (e.g., COM3, /dev/ttyUSB0)
  -o, --output OUTPUT  Output filename for flash dump
  --size SIZE          Flash size in bytes (default: 16777216 = 16MB)
  --speed SPEED        SPI clock speed in Hz (default: 12000000 = 12MHz)
  --chunk CHUNK        Read chunk size in bytes (default: 512)

Flash Size Examples:
  1MB   = 1048576      8MB  = 8388608
  2MB   = 2097152      16MB = 16777216
  4MB   = 4194304      32MB = 33554432

Examples:
  spi_flash_read.py -p COM3 -o flash.bin                    # Read 16MB flash (default)
  spi_flash_read.py -p COM3 -o flash.bin --size 4194304     # Read 4MB flash
  spi_flash_read.py -p COM3 -o flash.bin --speed 12000000   # Read at 12MHz
  spi_flash_read.py -p COM3 -o flash.bin --chunk 1024       # Use 1KB chunks
```

### spi_flash_write

BPIO2 SPI Flash Writer - Write file to SPI flash memory

**File:** `spi_flash_write.py`

```
usage: spi_flash_write.py [-h] -p PORT -i INPUT [--size SIZE] [--speed SPEED]
                          [--no-erase] [--no-verify]

BPIO2 SPI Flash Writer - Write file to flash memory

options:
  -h, --help         show this help message and exit
  -p, --port PORT    Serial port (e.g., COM3, /dev/ttyUSB0)
  -i, --input INPUT  Input filename to write to flash
  --size SIZE        Flash capacity in bytes (default: 16777216 = 16MB)
  --speed SPEED      SPI clock speed in Hz (default: 12000000 = 12MHz)
  --no-erase         Skip chip erase (faster but may have old data)
  --no-verify        Skip verification after writing (faster)

Examples:
  spi_flash_write.py -p COM3 -i firmware.bin                    # Write with chip erase
  spi_flash_write.py -p COM3 -i data.bin --no-erase             # Write without erase
  spi_flash_write.py -p COM3 -i data.bin --no-verify            # Write without verify
  spi_flash_write.py -p COM3 -i data.bin --size 4194304         # 4MB flash capacity
```

### status_example

BPIO2 Status Example - Display Bus Pirate status information

**File:** `status_example.py`

```
usage: status_example.py [-h] -p PORT [--simple]

BPIO2 Status Example - Display Bus Pirate status

options:
  -h, --help       show this help message and exit
  -p, --port PORT  Serial port (e.g., COM3, /dev/ttyUSB0)
  --simple         Show simple status output

Examples:
  status_example.py -p COM3              # Show detailed status
  status_example.py -p COM3 --simple     # Show simple status (same as client.show_status())
```

## Library Structure

- `pybpio/` - Main library package
  - `bpio_client.py` - Core Bus Pirate client
  - `bpio_1wire.py` - I2C protocol implementation
  - `bpio_i2c.py` - I2C protocol implementation
  - `bpio_spi.py` - SPI protocol implementation
  - `bpio_base.py` - Base class for protocol implementations
- `tooling/` - Flat buffer generated tooling files
- `flatbuffers/` - Flat buffer Python library

## Basic Usage

```python
from pybpio.bpio_client import BPIOClient
from pybpio.bpio_i2c import BPIOI2C

# Connect to Bus Pirate
client = BPIOClient('COM3')  # Use appropriate port

# Initialize I2C interface
i2c = BPIOI2C(client)
i2c.configure(speed=400000)

# Your operations here...

# Always close the connection
client.close()
```

## Requirements

- Python 3.6+
- pyserial library
- COBS library for COBS encoding/decoding
- Bus Pirate with BPIO2 firmware

## Error Handling

Always wrap Bus Pirate operations in try-catch blocks:

```python
try:
    client = BPIOClient('COM3')
    # Your operations here
    client.close()
except Exception as e:
    print(f'Error: {e}')
```
