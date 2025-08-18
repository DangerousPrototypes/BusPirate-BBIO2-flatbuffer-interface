#!/usr/bin/env python3
"""
BPIO2 1-Wire Example - Read temperature from DS18B20 sensor
Demonstrates 1-Wire communication with temperature sensors.
"""

import argparse
import sys
import time

# Import BPIO client and 1-Wire interface
from pybpio.bpio_client import BPIOClient
from pybpio.bpio_1wire import BPIO1Wire

def onewire_read_temperature(client, voltage=5000):
    """Read temperature from DS18B20 sensor."""
    onewire = BPIO1Wire(client)
    
    if onewire.configure(pullup_enable=True, psu_enable=True, 
                        psu_set_mv=voltage, psu_set_ma=0):
        
        print(f"1-Wire configured with {voltage/1000:.1f}V supply")
        
        # Configure DS18B20 scratchpad (optional)
        print("Configuring DS18B20 sensor...")
        onewire.transfer(write_data=[0xCC, 0x4E, 0x00, 0x00, 0x7F])
        
        # Start temperature conversion
        print("Starting temperature conversion...")
        onewire.transfer(write_data=[0xCC, 0x44])
        
        # Wait for conversion (750ms for 12-bit resolution)
        print("Waiting for conversion (750ms)...")
        time.sleep(0.8)
        
        # Read scratchpad
        print("Reading temperature data...")
        data = onewire.transfer(write_data=[0xCC, 0xBE], read_bytes=9)
        
        if data and len(data) >= 2:
            # Convert temperature (first two bytes)
            temp_lsb = data[0]
            temp_msb = data[1]
            temp_raw = (temp_msb << 8) | temp_lsb
            
            # Handle negative temperatures (two's complement)
            if temp_raw & 0x8000:
                temp_raw = -((temp_raw ^ 0xFFFF) + 1)
            
            # Convert to Celsius (12-bit resolution = 0.0625°C per bit)
            temperature_c = temp_raw / 16.0
            temperature_f = (temperature_c * 9/5) + 32
            
            print(f"\nTemperature Results:")
            print(f"  Raw data: {' '.join(f'{b:02X}' for b in data[:2])}")
            print(f"  Raw value: {temp_raw}")
            print(f"  Temperature: {temperature_c:.4f}°C")
            print(f"  Temperature: {temperature_f:.4f}°F")
            
            # Additional scratchpad info
            if len(data) >= 9:
                print(f"\nScratchpad data: {' '.join(f'{b:02X}' for b in data)}")
                print(f"  TH register: {data[2]}")
                print(f"  TL register: {data[3]}")
                print(f"  Config register: 0x{data[4]:02X}")
                
        else:
            print("Failed to read temperature data")
            return False
    else:
        print("Failed to configure 1-Wire interface")
        return False
    
    return True

def onewire_search_devices(client, voltage=5000):
    """Search for 1-Wire devices on the bus."""
    onewire = BPIO1Wire(client)
    
    if onewire.configure(pullup_enable=True, psu_enable=True,
                        psu_set_mv=voltage, psu_set_ma=0):
        
        print("Searching for 1-Wire devices...")
        
        # Simple presence detection
        # False indicates no devices found
        # None indicates no data in response
        result = onewire.reset()
        if result is None:
            print("Device(s) detected on 1-Wire bus")
            
            # Try to read ROM (works only with single device)
            print("Attempting to read ROM code...")
            rom_data = onewire.transfer(write_data=[0x33], read_bytes=8)
            
            if rom_data and len(rom_data) == 8:
                family_code = rom_data[0]
                serial_number = rom_data[1:7]
                crc = rom_data[7]
                
                print(f"ROM Code: {' '.join(f'{b:02X}' for b in rom_data)}")
                print(f"  Family Code: 0x{family_code:02X}")
                print(f"  Serial Number: {' '.join(f'{b:02X}' for b in serial_number)}")
                print(f"  CRC: 0x{crc:02X}")
                
                # Decode family codes
                families = {
                    0x10: "DS18S20 (Temperature)",
                    0x28: "DS18B20 (Temperature)", 
                    0x22: "DS1822 (Temperature)",
                    0x26: "DS2438 (Smart Battery Monitor)",
                    0x3A: "DS2413 (Dual Channel Switch)"
                }
                
                if family_code in families:
                    print(f"  Device Type: {families[family_code]}")
                else:
                    print(f"  Device Type: Unknown family 0x{family_code:02X}")
                    
            else:
                print("Failed to read ROM (multiple devices on bus?)")
        else:
            print("No devices detected on 1-Wire bus")
            return False
    else:
        print("Failed to configure 1-Wire interface")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description='BPIO2 1-Wire Example - Communicate with 1-Wire devices',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -p COM3                    # Read temperature from DS18B20
  %(prog)s -p COM3 --voltage 3300     # Use 3.3V supply voltage
  %(prog)s -p COM3 --search           # Search for devices on bus
        """
    )
    
    parser.add_argument('-p', '--port', required=True,
                       help='Serial port (e.g., COM3, /dev/ttyUSB0)')
    parser.add_argument('--voltage', type=int, default=5000,
                       help='Supply voltage in mV (default: 5000)')
    parser.add_argument('--search', action='store_true',
                       help='Search for devices instead of reading temperature')
    
    args = parser.parse_args()
    
    try:
        client = BPIOClient(args.port)
        print(f"Connected to Bus Pirate on {args.port}")
        
        if args.search:
            success = onewire_search_devices(client, args.voltage)
        else:
            success = onewire_read_temperature(client, args.voltage)
        
        client.close()
        return 0 if success else 1
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())