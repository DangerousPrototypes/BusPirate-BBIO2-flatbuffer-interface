#!/usr/bin/env python3
"""
BPIO2 SPI Flash Writer - Write file to SPI flash memory
Demonstrates writing files to flash with erase and verification.
"""

import argparse
import sys
import os
import time

# Import BPIO client and SPI interface
from pybpio.bpio_client import BPIOClient
from pybpio.bpio_spi import BPIOSPI
from inc.progress_indicator import show_progress

def erase_flash(spi):
    """Erase entire flash chip."""
    print("Erasing flash chip (this may take several minutes)...")
    start_time = time.time()
    
    # Write enable
    spi.transfer(write_data=[0x06])
    
    # Chip erase
    spi.transfer(write_data=[0xC7])
    
    # Wait for erase completion
    while True:
        status_data = spi.transfer(write_data=[0x05], read_bytes=1)
        if status_data and len(status_data) == 1:
            if (status_data[0] & 0x01) == 0:  # WIP bit cleared
                break
        time.sleep(0.5)
        
        elapsed = time.time() - start_time
        print(f'\rErasing... {elapsed:.1f}s elapsed', end='', flush=True)
    
    total_time = time.time() - start_time
    print(f"\nErase completed in {total_time:.1f}s")
    return True

def write_flash(spi, filename, verify=True):
    """Write file to flash with optional verification."""
    file_size = os.path.getsize(filename)
    page_size = 256  # Standard SPI flash page size
    
    print(f"Writing {file_size//(1024*1024):.1f}MB from '{filename}' to flash...")
    
    with open(filename, 'rb') as f:
        address = 0
        start_time = time.time()
        total_pages = (file_size + page_size - 1) // page_size
        page_count = 0
        
        while address < file_size:
            # Read page from file
            page_data = f.read(page_size)
            if not page_data:
                break
            
            # Write enable
            spi.transfer(write_data=[0x06])
            
            # Page program: 0x02 + 24-bit address + data
            cmd = [0x02, (address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]
            cmd.extend(page_data)
            spi.transfer(write_data=cmd)
            
            # Wait for write completion
            while True:
                status_data = spi.transfer(write_data=[0x05], read_bytes=1)
                if status_data and len(status_data) == 1:
                    if (status_data[0] & 0x01) == 0:  # WIP bit cleared
                        break
                time.sleep(0.001)
            
            address += len(page_data)
            page_count += 1
            
            # Update progress every 64 pages or at end
            if page_count == 1 or page_count % 64 == 0 or page_count == total_pages:
                show_progress(address, file_size, start_time, "Writing")
        
        write_time = time.time() - start_time
        print(f"\nWrite completed in {write_time:.1f}s")
    
    # Verification
    if verify:
        print("Verifying written data...")
        verify_start = time.time()
        
        with open(filename, 'rb') as f:
            address = 0
            verify_chunk = 512
            
            while address < file_size:
                expected_data = f.read(verify_chunk)
                if not expected_data:
                    break
                
                # Read from flash
                cmd = [0x03, (address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]
                actual_data = spi.transfer(write_data=cmd, read_bytes=len(expected_data))
                
                if actual_data != expected_data:
                    print(f"\nVerification failed at address 0x{address:06X}")
                    return False
                
                address += len(expected_data)
                
                # Show progress every 64KB
                if address % (64 * 1024) == 0 or address >= file_size:
                    show_progress(address, file_size, verify_start, "Verifying")
        
        verify_time = time.time() - verify_start
        print(f"\nVerification completed successfully in {verify_time:.1f}s")
    
    return True

def write_spi_flash(client, filename, flash_size, speed, erase_chip, verify):
    """Main flash writing function."""
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found")
        return False
    
    file_size = os.path.getsize(filename)
    
    if file_size > flash_size:
        print(f"Error: File size ({file_size} bytes) exceeds flash capacity ({flash_size} bytes)")
        return False
    
    spi = BPIOSPI(client)
    
    if spi.configure(speed=speed, clock_polarity=False, clock_phase=False,
                    chip_select_idle=True, psu_enable=True, psu_set_mv=3300,
                    psu_set_ma=0, pullup_enable=True):
        
        print(f"SPI configured at {speed/1000000:.1f}MHz")
        
        if erase_chip:
            if not erase_flash(spi):
                return False
        
        return write_flash(spi, filename, verify)
    else:
        print("Failed to configure SPI interface")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='BPIO2 SPI Flash Writer - Write file to flash memory',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -p COM3 -i firmware.bin                    # Write with chip erase
  %(prog)s -p COM3 -i data.bin --no-erase             # Write without erase  
  %(prog)s -p COM3 -i data.bin --no-verify            # Write without verify
  %(prog)s -p COM3 -i data.bin --size 4194304         # 4MB flash capacity
        """
    )
    
    parser.add_argument('-p', '--port', required=True,
                       help='Serial port (e.g., COM3, /dev/ttyUSB0)')
    parser.add_argument('-i', '--input', required=True,
                       help='Input filename to write to flash')
    parser.add_argument('--size', type=int, default=16*1024*1024,
                       help='Flash capacity in bytes (default: 16777216 = 16MB)')
    parser.add_argument('--speed', type=int, default=12*1000*1000,
                       help='SPI clock speed in Hz (default: 12000000 = 12MHz)')
    parser.add_argument('--no-erase', action='store_true',
                       help='Skip chip erase (faster but may have old data)')
    parser.add_argument('--no-verify', action='store_true',
                       help='Skip verification after writing (faster)')
    
    args = parser.parse_args()
    
    try:
        client = BPIOClient(args.port)
        print(f"Connected to Bus Pirate on {args.port}")
        
        success = write_spi_flash(client, args.input, args.size, args.speed,
                                 not args.no_erase, not args.no_verify)
        
        client.close()
        return 0 if success else 1
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())