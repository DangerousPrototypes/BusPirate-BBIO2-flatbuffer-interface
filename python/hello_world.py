#!/usr/bin/env python3
"""
BPIO2 Hello World Example 
Enter I2C mode, perform some basic operations, and display status.
"""

import argparse
import sys
import os

# Import BPIO client and I2C interface
from pybpio.bpio_client import BPIOClient
from pybpio.bpio_i2c import BPIOI2C

def show_pin_voltages(i2c):
    # Show pin voltages
    print("Pin voltages:")
    pin_voltage = i2c.get_adc_mv()
    pin_labels = i2c.get_mode_pin_labels()
    # Print header (skip first and last labels)
    print(" ".join(f"{label:>8}" for label in pin_labels[1:-1]))
    # Print separator line
    print(" ".join("-" * 8 for _ in pin_labels[1:-1]))
    # Print values with consistent formatting
    print(" ".join(f"{pin_voltage[pin]:>6}mV" for pin in range(8)))

def basic_example(client):
    """Basic I2C example with status display."""
    i2c = BPIOI2C(client)
    
    # Configure I2C with all hardware settings
    print("Configuring I2C interface...\n")
    if i2c.configure(speed=400000, pullup_enable=True, psu_enable=True, 
                    psu_set_mv=3300, psu_set_ma=0):
        
        # Show configuration with individual setters (less efficient but demonstrates API)
        print("Setting additional configurations...")
        i2c.set_mode_bitorder_msb()
        
        # Set LED colors (rainbow pattern)
        print("Setting LED colors...")
        led_colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF] * 3
        i2c.set_led_color(led_colors)
        
        # Print a string to the terminal (if bpio debug enabled in config)
        # https://docs.buspirate.com/docs/binmode-reference/protocol-bpio2/#debugging
        i2c.set_print_string("Hello from BPIO2 I2C interface!\r\n")
        
        # Display status information
        print(f"Current mode: {i2c.get_mode_current()}")
        print(f"PSU enabled: {i2c.get_psu_enabled()}")
        print(f"PSU voltage: {i2c.get_psu_measured_mv()}mV")
        print(f"PSU current: {i2c.get_psu_measured_ma()}mA")
        print(f"Pull-up enabled: {i2c.get_pullup_enabled()}")

        # Show pin voltages
        show_pin_voltages(i2c)    

        print("Changing PSU settings...")
        # Change voltage and current settings
        i2c.set_psu_enable(2500, 100) # 2.5V, 100mA

        # Show new PSU settings
        print(f"New PSU voltage: {i2c.get_psu_measured_mv()}mV")
        print(f"New PSU max current: {i2c.get_psu_set_ma()}mA")

        # Show pin voltages
        show_pin_voltages(i2c)

        print("All operations completed successfully!")

    else:
        print("Failed to configure I2C interface")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description='BPIO2 I2C Example - Basic configuration and status display',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -p COM3 # Enter I2C mode, configure settings, display status
        """
    )
    
    parser.add_argument('-p', '--port', required=True,
                       help='Serial port (e.g., COM3, /dev/ttyUSB0)')    
    args = parser.parse_args()
    
    try:
        client = BPIOClient(args.port)
        print(f"Connected to Bus Pirate on {args.port}")      
        success = basic_example(client)
        client.close()
        return 0 if success else 1
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())