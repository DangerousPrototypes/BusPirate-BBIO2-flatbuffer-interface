#!/usr/bin/env python3
"""
Generate README.md by running all Python scripts with -h flag
"""

import os
import subprocess
import sys
from pathlib import Path

def run_script_help(script_path):
    """Run a Python script with -h flag and capture output."""
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), '-h'],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout expired", 1
    except Exception as e:
        return "", f"Error: {e}", 1

def get_script_description(script_path):
    """Extract description from script docstring."""
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Look for module docstring
        lines = content.split('\n')
        in_docstring = False
        docstring_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('"""') or line.startswith("'''"):
                if in_docstring:
                    break
                in_docstring = True
                # Handle single-line docstring
                if line.count('"""') >= 2 or line.count("'''") >= 2:
                    desc = line.replace('"""', '').replace("'''", '').strip()
                    return desc if desc else "Python script"
                continue
            elif in_docstring:
                if line and not line.startswith('#'):
                    docstring_lines.append(line)
        
        if docstring_lines:
            return docstring_lines[0]
        return "Python script"
    except:
        return "Python script"

def generate_readme(directory_path, output_file='README.md'):
    """Generate README.md from all Python scripts in directory."""
    
    directory = Path(directory_path)
    if not directory.exists():
        print(f"Directory {directory_path} does not exist")
        return
    
    # Find all Python files in current directory only (no recursion)
    python_files = []
    for file_path in directory.glob('*.py'):
        if file_path.name not in ['__init__.py', 'generate_readme.py']:
            python_files.append(file_path)
    
    python_files.sort()
    
    # Generate README content
    readme_content = []
    readme_content.append("# BPIO2 Python Library")
    readme_content.append("")
    readme_content.append("A Python library for interfacing with the Bus Pirate using the binary mode flat buffer interface (BPIO2).")
    readme_content.append("")
    readme_content.append("Full documentation is available at [BPIO2 Documentation](https://docs.buspirate.com/docs/binmode-reference/protocol-bpio2/#python-library).")
    
    readme_content.append("## Installation")
    readme_content.append("")
    readme_content.append("Clone this repository:")
    readme_content.append("```bash")
    readme_content.append("git clone <repository-url>")
    readme_content.append("cd bpio2/python")
    readme_content.append("```")
    readme_content.append("")
    readme_content.append("Install required dependencies:")
    readme_content.append("```bash")
    readme_content.append("pip3 install -r requirements.txt")
    readme_content.append("```")
    readme_content.append("")

    readme_content.append("## Setup")
    readme_content.append("")
    readme_content.append("Ensure you have the latest Bus Pirate firmware with BPIO2 support.")
    readme_content.append("In the Bus Pirate terminal enable the BPIO2 binary mode:")
    readme_content.append("```bash")
    readme_content.append(">binmode")
    readme_content.append("```")
    readme_content.append("Choose **BBIO2** as the binary mode, optionally save it as the default mode.")
    readme_content.append("")
    
    readme_content.append("## Examples and Scripts")
    readme_content.append("")
    
    for script_path in python_files:
        script_name = script_path.stem
        description = get_script_description(script_path)
        
        readme_content.append(f"### {script_name}")
        readme_content.append("")
        readme_content.append(f"{description}")
        readme_content.append("")
        readme_content.append(f"**File:** `{script_path.name}`")
        readme_content.append("")
        
        # Get help output
        stdout, stderr, returncode = run_script_help(script_path)
        
        if returncode == 0 and stdout:
            readme_content.append("```")
            # Clean up the help output
            help_lines = stdout.strip().split('\n')
            for line in help_lines:
                readme_content.append(line.rstrip())
            readme_content.append("```")
        else:
            readme_content.append("```bash")
            readme_content.append(f"python {script_path.name} [options]")
            readme_content.append("```")
            if stderr:
                readme_content.append("")
                readme_content.append(f"*Note: {stderr.strip()}*")
        
        readme_content.append("")
    
    # Add library information
    readme_content.append("## Library Structure")
    readme_content.append("")
    readme_content.append("- `pybpio/` - Main library package")
    readme_content.append("  - `bpio_client.py` - Core Bus Pirate client")
    readme_content.append("  - `bpio_1wire.py` - I2C protocol implementation")
    readme_content.append("  - `bpio_i2c.py` - I2C protocol implementation")
    readme_content.append("  - `bpio_spi.py` - SPI protocol implementation")
    readme_content.append("  - `bpio_base.py` - Base class for protocol implementations")
    readme_content.append("- `tooling/` - Flat buffer generated tooling files")
    readme_content.append("- `flatbuffers/` - Flat buffer Python library")
    readme_content.append("")
    
    readme_content.append("## Basic Usage")
    readme_content.append("")
    readme_content.append("```python")
    readme_content.append("from pybpio.bpio_client import BPIOClient")
    readme_content.append("from pybpio.bpio_i2c import BPIOI2C")
    readme_content.append("")
    readme_content.append("# Connect to Bus Pirate")
    readme_content.append("client = BPIOClient('COM3')  # Use appropriate port")
    readme_content.append("")
    readme_content.append("# Initialize I2C interface")
    readme_content.append("i2c = BPIOI2C(client)")
    readme_content.append("i2c.configure(speed=400000)")
    readme_content.append("")
    readme_content.append("# Your operations here...")
    readme_content.append("")
    readme_content.append("# Always close the connection")
    readme_content.append("client.close()")
    readme_content.append("```")
    readme_content.append("")
    
    readme_content.append("## Requirements")
    readme_content.append("")
    readme_content.append("- Python 3.6+")
    readme_content.append("- pyserial library")
    readme_content.append("- COBS library for COBS encoding/decoding")
    readme_content.append("- Bus Pirate with BPIO2 firmware")
    readme_content.append("")
    
    readme_content.append("## Error Handling")
    readme_content.append("")
    readme_content.append("Always wrap Bus Pirate operations in try-catch blocks:")
    readme_content.append("")
    readme_content.append("```python")
    readme_content.append("try:")
    readme_content.append("    client = BPIOClient('COM3')")
    readme_content.append("    # Your operations here")
    readme_content.append("    client.close()")
    readme_content.append("except Exception as e:")
    readme_content.append("    print(f'Error: {e}')")
    readme_content.append("```")
    readme_content.append("")
    
    # Write to file
    output_path = directory / output_file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(readme_content))
    
    print(f"README.md generated: {output_path}")
    print(f"Processed {len(python_files)} Python scripts")

def main():
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = '.'
    
    generate_readme(directory)

if __name__ == '__main__':
    main()