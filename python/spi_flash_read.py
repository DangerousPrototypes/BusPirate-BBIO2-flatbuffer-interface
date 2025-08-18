#!/usr/bin/env python3
"""
BPIO2 SPI Flash Reader - Read SPI flash memory to file
Demonstrates reading entire flash memory with progress indication.
"""

import argparse
import sys
import os
import time

# Import BPIO client and SPI interface
from pybpio.bpio_client import BPIOClient
from pybpio.bpio_spi import BPIOSPI
from inc.progress_indicator import show_progress

def read_spi_flash(client, filename, flash_size, speed, chunk_size):
    """Read SPI flash memory to file with progress indication."""
    spi = BPIOSPI(client)
    
    if spi.configure(speed=speed, clock_polarity=False, clock_phase=False,
                    chip_select_idle=True, psu_enable=True, psu_set_mv=3300,
                    psu_set_ma=0, pullup_enable=True):
        
        print(f"SPI configured at {speed/1000000:.1f}MHz")
        print(f"Reading {flash_size//(1024*1024)}MB flash to '{filename}'...")
        print(f"Chunk size: {chunk_size} bytes")
        
        with open(filename, 'wb') as f:
            address = 0
            chunk_count = 0
            start_time = time.time()
            total_chunks = flash_size // chunk_size
            
            while address < flash_size:
                # Prepare read command: 0x03 + 24-bit address
                cmd = [0x03, (address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]
                
                # Read chunk
                data = spi.transfer(write_data=cmd, read_bytes=chunk_size)
                
                if data and len(data) == chunk_size:
                    f.write(data)
                    address += chunk_size
                    chunk_count += 1
                    
                    # Update progress every 256 chunks or at end
                    if chunk_count == 1 or chunk_count % 256 == 0 or chunk_count == total_chunks:
                        show_progress(address, flash_size, start_time, "Reading")
                else:
                    print(f"\nError: Failed to read at address 0x{address:06X}")
                    return False
            
            total_time = time.time() - start_time
            total_time_str = f"{int(total_time//60):02d}:{int(total_time%60):02d}"
            average_speed = (address / (1024 * 1024)) / total_time
            
            print(f"\nSuccess! Read {address} bytes in {total_time_str}")
            print(f"Average speed: {average_speed:.1f}MB/s")
            
    else:
        print("Failed to configure SPI interface")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description='BPIO2 SPI Flash Reader - Read flash memory to file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Flash Size Examples:
  1MB   = 1048576      8MB  = 8388608
  2MB   = 2097152      16MB = 16777216  
  4MB   = 4194304      32MB = 33554432

Examples:
  %(prog)s -p COM3 -o flash.bin                    # Read 16MB flash (default)
  %(prog)s -p COM3 -o flash.bin --size 4194304     # Read 4MB flash
  %(prog)s -p COM3 -o flash.bin --speed 12000000   # Read at 12MHz
  %(prog)s -p COM3 -o flash.bin --chunk 1024       # Use 1KB chunks
        """
    )
    
    parser.add_argument('-p', '--port', required=True,
                       help='Serial port (e.g., COM3, /dev/ttyUSB0)')
    parser.add_argument('-o', '--output', required=True,
                       help='Output filename for flash dump')
    parser.add_argument('--size', type=int, default=16*1024*1024,
                       help='Flash size in bytes (default: 16777216 = 16MB)')
    parser.add_argument('--speed', type=int, default=12*1000*1000,
                       help='SPI clock speed in Hz (default: 12000000 = 12MHz)')
    parser.add_argument('--chunk', type=int, default=512,
                       help='Read chunk size in bytes (default: 512)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.size <= 0:
        print("Error: Flash size must be positive")
        return 1
    
    if args.chunk <= 0 or args.chunk > 4096:
        print("Error: Chunk size must be between 1 and 4096 bytes")
        return 1
    
    try:
        client = BPIOClient(args.port)
        print(f"Connected to Bus Pirate on {args.port}")
        
        success = read_spi_flash(client, args.output, args.size, args.speed, args.chunk)
        
        client.close()
        return 0 if success else 1
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())