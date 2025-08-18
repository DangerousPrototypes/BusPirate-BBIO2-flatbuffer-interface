#!/usr/bin/env python3
"""
FlatBuffer Tooling Generator for BPIO2
Generates FlatBuffer tooling for all supported languages using flatc and flatcc compilers.
"""

import os
import subprocess
import sys
import argparse
from pathlib import Path

# Language configurations for flatc
FLATC_LANGUAGES = {
    'cpp': '--cpp',
    'csharp': '--csharp', 
    'dart': '--dart',
    'go': '--go',
    'java': '--java',
    #'javascript': '--js',
    'kotlin': '--kotlin',
    'lobster': '--lobster',
    'lua': '--lua',
    'nim': '--nim',
    'php': '--php',
    'python': '--python',
    'rust': '--rust',
    'swift': '--swift',
    'typescript': '--ts'
}

# Special case languages that need different handling
FLATCC_LANGUAGES = {
    'c': ['-a']  # flatcc uses -a flag for all C files
}

def check_compiler_availability():
    """Check if flatc and flatcc compilers are available."""
    compilers = {}
    
    # Check flatc
    try:
        result = subprocess.run(['flatc', '--version'], 
                              capture_output=True, text=True, check=True)
        compilers['flatc'] = result.stdout.strip()
        print(f"Found flatc: {compilers['flatc']}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: flatc compiler not found. Install from https://github.com/google/flatbuffers")
        compilers['flatc'] = None
    
    # Check flatcc
    try:
        result = subprocess.run(['flatcc', '--help'], 
                              capture_output=True, text=True)
        if result.returncode == 0 or 'flatcc' in result.stderr.lower():
            compilers['flatcc'] = "Available"
            print("Found flatcc compiler")
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print("Warning: flatcc compiler not found. Install from https://github.com/dvidelabs/flatcc")
        compilers['flatcc'] = None
    
    return compilers

def find_schema_file(search_paths):
    """Find the BPIO2 schema file."""
    possible_names = ['bpio2.fbs', 'bpio.fbs']
    
    for search_path in search_paths:
        path = Path(search_path)
        if path.is_file() and path.suffix == '.fbs':
            print(f"Found schema file: {path}")
            return path
        
        for name in possible_names:
            schema_file = path / name
            if schema_file.exists():
                print(f"Found schema file: {schema_file}")
                return schema_file
    
    return None

def generate_flatc_tooling(schema_file, output_dir, languages):
    """Generate tooling for flatc-supported languages."""
    if not languages:
        return True
    
    success_count = 0
    total_count = len(languages)
    
    for lang, flag in languages.items():
        lang_dir = output_dir / lang / 'tooling'
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Generating {lang} tooling...")
        
        try:
            cmd = ['flatc', flag, '-o', str(lang_dir), str(schema_file)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Check if files were generated
            generated_files = list(lang_dir.glob('*'))
            if generated_files:
                print(f"  ✓ Generated {len(generated_files)} files in {lang_dir}")
                success_count += 1
            else:
                print(f"  ⚠ No files generated for {lang}")
                
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Failed to generate {lang} tooling: {e.stderr}")
        except Exception as e:
            print(f"  ✗ Error generating {lang} tooling: {e}")
    
    print(f"flatc: {success_count}/{total_count} languages successful")
    return success_count == total_count

def generate_flatcc_tooling(schema_file, output_dir):
    """Generate C tooling using flatcc."""
    lang_dir = output_dir / 'c' / 'tooling'
    lang_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating C tooling with flatcc...")
    
    try:
        cmd = ['flatcc', '-a', '-o', str(lang_dir), str(schema_file)]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Check if files were generated
        generated_files = list(lang_dir.glob('*'))
        if generated_files:
            print(f"  ✓ Generated {len(generated_files)} C files in {lang_dir}")
            return True
        else:
            print(f"  ⚠ No C files generated")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Failed to generate C tooling: {e.stderr}")
        return False
    except Exception as e:
        print(f"  ✗ Error generating C tooling: {e}")
        return False

def create_readme(output_dir, schema_file, successful_languages):
    """Create a README file documenting the generated tooling."""
    readme_content = f"""# BPIO2 FlatBuffer Tooling

This directory contains auto-generated FlatBuffer tooling for the BPIO2 protocol.

## Source Schema
- Schema file: {schema_file.name}
- Generated on: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip() if os.name != 'nt' else 'Windows'}

## Generated Languages

"""
    
    for lang in sorted(successful_languages):
        readme_content += f"- **{lang.title()}**: `{lang}/tooling/`\n"
    
    readme_content += f"""
## Usage

Each language directory contains the generated FlatBuffer code for that language.
Include the appropriate files in your project according to your language's conventions.

See [flatc](https://flatbuffers.dev/quick_start/) for language-specific usage instructions.

## Flat Buffer Includes

In addition to the generated tooling, you will need to include the flat buffer support library for your language in the /include/ folder.

### Compilers Used
- **flatc**: For C++, C#, Dart, Go, Java, JavaScript, Kotlin, Lobster, Lua, PHP, Python, Rust, Swift, TypeScript
- **flatcc**: For C 

Javascript is deprecated in the latest flatc. Instead transpile from TypeScript to JavaScript if needed.

### Example Usage

#### Python
```python
# Add the python/tooling directory to your Python path
import sys
sys.path.append('python/tooling')

# Import generated modules
from StatusRequest import StatusRequest
from StatusResponse import StatusResponse
```

#### C
```c
// Include the generated headers
#include "bpio2_reader.h"
#include "bpio2_builder.h"
```

## Documentation

See the main [BPIO2 documentation](https://docs.buspirate.com/docs/binmode-reference/protocol-bpio2) for protocol details and usage examples.
"""
    
    readme_path = output_dir / 'README.md'
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"Created documentation: {readme_path}")

def main():
    parser = argparse.ArgumentParser(
        description='Generate FlatBuffer tooling for BPIO2 protocol',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Generate all languages
  %(prog)s --schema bpio2.fbs                 # Use specific schema file
  %(prog)s --output ./generated               # Custom output directory
  %(prog)s --languages python go rust        # Generate only specific languages
  %(prog)s --skip-flatcc                      # Skip C tooling generation
        """
    )
    
    parser.add_argument('--schema', type=Path,
                       help='Path to schema file (auto-detected if not specified)')
    parser.add_argument('--output', type=Path, default='./',
                       help='Output directory (default: ./)')
    parser.add_argument('--languages', nargs='*', 
                       choices=list(FLATC_LANGUAGES.keys()),
                       help='Specific languages to generate (default: all)')
    parser.add_argument('--skip-flatcc', action='store_true',
                       help='Skip C tooling generation with flatcc')
    parser.add_argument('--force', action='store_true',
                       help='Overwrite existing tooling directories')
    
    args = parser.parse_args()
    
    # Check compiler availability
    compilers = check_compiler_availability()
    
    # Find schema file
    if args.schema:
        schema_file = args.schema
        if not schema_file.exists():
            print(f"Error: Schema file not found: {schema_file}")
            return 1
    else:
        # Auto-detect schema file
        search_paths = ['.', './src', '../src', './flatbuffers', '../flatbuffers']
        schema_file = find_schema_file(search_paths)
        if not schema_file:
            print("Error: Could not find BPIO2 schema file (.fbs)")
            print("Searched in:", search_paths)
            print("Use --schema to specify the file location")
            return 1
    
    # Prepare output directory
    output_dir = args.output
    if output_dir.exists() and not args.force:
        response = input(f"Output directory {output_dir} exists. Continue? [y/N]: ")
        if response.lower() != 'y':
            print("Aborted")
            return 1
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    successful_languages = []
    
    # Generate flatc tooling
    if compilers['flatc']:
        languages_to_generate = FLATC_LANGUAGES
        if args.languages:
            languages_to_generate = {k: v for k, v in FLATC_LANGUAGES.items() 
                                   if k in args.languages}
        
        if generate_flatc_tooling(schema_file, output_dir, languages_to_generate):
            successful_languages.extend(languages_to_generate.keys())
        else:
            successful_languages.extend([lang for lang in languages_to_generate.keys()
                                       if (output_dir / lang / 'tooling').exists() and 
                                       list((output_dir / lang / 'tooling').glob('*'))])
    else:
        print("Skipping flatc languages (compiler not available)")
    
    # Generate flatcc tooling
    if not args.skip_flatcc and compilers['flatcc']:
        if generate_flatcc_tooling(schema_file, output_dir):
            successful_languages.append('c')
    elif args.skip_flatcc:
        print("Skipping C tooling (--skip-flatcc specified)")
    else:
        print("Skipping C tooling (flatcc not available)")
    
    # Create documentation
    if successful_languages:
        create_readme(output_dir, schema_file, successful_languages)
    
    # Summary
    print(f"\n=== Generation Summary ===")
    print(f"Schema file: {schema_file}")
    print(f"Output directory: {output_dir}")
    print(f"Successful languages: {len(successful_languages)}")
    
    if successful_languages:
        print("Generated tooling for:")
        for lang in sorted(successful_languages):
            lang_dir = output_dir / lang / 'tooling'
            file_count = len(list(lang_dir.glob('*'))) if lang_dir.exists() else 0
            print(f"  - {lang.ljust(12)} ({file_count} files)")
    else:
        print("No tooling was generated successfully")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())