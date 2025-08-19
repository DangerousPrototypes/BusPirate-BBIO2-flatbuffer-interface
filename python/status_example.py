#!/usr/bin/env python3
"""
BPIO2 Status Example - Display Bus Pirate status information
Demonstrates how to read and display various status information.
"""

import argparse
import sys

# Import BPIO client
from pybpio.bpio_client import BPIOClient

def show_detailed_status(client):
    """Display detailed status information."""
    print("=== Bus Pirate Status Information ===\n")
    
    # Get full status
    status = client.status_request()
    
    if status.get('error'):
        print(f"Error getting status: {status['error']}")
        return False
    
    # Hardware Information
    print("Hardware Information:")
    print(f"  Version: {status.get('version_hardware_major', 'Unknown')}.{status.get('version_hardware_minor', 'Unknown')}")
    
    # Firmware Information  
    print(f"\nFirmware Information:")
    print(f"  Version: {status.get('version_firmware_major', 'Unknown')}.{status.get('version_firmware_minor', 'Unknown')}")
    print(f"  Git Hash: {status.get('version_firmware_git_hash', 'Unknown')}")
    print(f"  Build Date: {status.get('version_firmware_date', 'Unknown')}")
    
    # Current Mode
    print(f"\nMode Information:")
    print(f"  Current Mode: {status.get('mode_current', 'Unknown')}")
    print(f"  Available Modes: {', '.join(status.get('modes_available', []))}")
    print(f"  Bit Order MSB: {status.get('mode_bitorder_msb', False)}")
    print(f"  Max Packet Size: {status.get('mode_max_packet_size', 'Unknown')} bytes")
    print(f"  Max Write Size: {status.get('mode_max_write', 'Unknown')} bytes")
    print(f"  Max Read Size: {status.get('mode_max_read', 'Unknown')} bytes")
    
    # Pin Labels
    pin_labels = status.get('mode_pin_labels', [])
    if pin_labels:
        print(f"  Pin Labels: {', '.join(pin_labels)}")
    
    # Power Supply
    print(f"\nPower Supply:")
    print(f"  Enabled: {status.get('psu_enabled', False)}")
    print(f"  Set Voltage: {status.get('psu_set_mv', 0)} mV")
    print(f"  Set Current: {status.get('psu_set_ma', 0)} mA")
    print(f"  Measured Voltage: {status.get('psu_measured_mv', 0)} mV")
    print(f"  Measured Current: {status.get('psu_measured_ma', 0)} mA")
    print(f"  Over Current Error: {status.get('psu_current_error', False)}")
    
    # Pull-up Resistors
    print(f"\nPull-up Resistors:")
    print(f"  Enabled: {status.get('pullup_enabled', False)}")
    
    # IO Pins
    io_direction = status.get('io_direction', 0)
    io_value = status.get('io_value', 0)
    print(f"\nIO Pins:")
    print(f"  Directions: 0x{io_direction:02X} ({io_direction:08b})")
    print(f"  Values: 0x{io_value:02X} ({io_value:08b})")
    
    # Individual pin status
    print("  Pin Status:")
    for i in range(8):
        direction = "OUT" if (io_direction >> i) & 1 else "IN"
        value = "HIGH" if (io_value >> i) & 1 else "LOW"
        print(f"    IO{i}: {direction}, {value}")
    
    # ADC Values
    adc_values = status.get('adc_mv', [])
    if adc_values:
        print(f"\nADC Values (mV):")
        for i, voltage in enumerate(adc_values):
            print(f"  IO{i}: {voltage} mV")
    
    # Storage
    disk_size = status.get('disk_size_mb')
    disk_used = status.get('disk_used_mb')
    if disk_size is not None:
        print(f"\nStorage:")
        print(f"  Total Size: {disk_size:.2f} MB")
        print(f"  Used Space: {disk_used:.2f} MB")
        print(f"  Free Space: {disk_size - disk_used:.2f} MB")
        print(f"  Used: {(disk_used/disk_size)*100:.1f}%")
    
    # LEDs
    led_count = status.get('led_count')
    if led_count is not None:
        print(f"\nLEDs:")
        print(f"  Count: {led_count}")
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description='BPIO2 Status Example - Display Bus Pirate status',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -p COM3              # Show detailed status
  %(prog)s -p COM3 --simple     # Show simple status (same as client.show_status())
        """
    )
    
    parser.add_argument('-p', '--port', required=True,
                       help='Serial port (e.g., COM3, /dev/ttyUSB0)')
    parser.add_argument('--simple', action='store_true',
                       help='Show simple status output')
    
    args = parser.parse_args()
    
    try:
        client = BPIOClient(args.port)
        print(f"Connected to Bus Pirate on {args.port}\n")
        
        if args.simple:
            # Use built-in status display
            client.show_status()
        else:
            # Show detailed custom status
            success = show_detailed_status(client)
            if not success:
                return 1
        
        client.close()
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())