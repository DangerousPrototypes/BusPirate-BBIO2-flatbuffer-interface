# BPIO2 FlatBuffer Tooling

This directory contains auto-generated FlatBuffer tooling for the BPIO2 protocol.

## Source Schema
- Schema file: bpio.fbs
- Generated on: Mon Aug 18 17:23:35 CEST 2025

## Generated Languages

- **C**: `c/tooling/`
- **Cpp**: `cpp/tooling/`
- **Csharp**: `csharp/tooling/`
- **Dart**: `dart/tooling/`
- **Go**: `go/tooling/`
- **Java**: `java/tooling/`
- **Kotlin**: `kotlin/tooling/`
- **Lobster**: `lobster/tooling/`
- **Php**: `php/tooling/`
- **Python**: `python/tooling/`
- **Rust**: `rust/tooling/`
- **Swift**: `swift/tooling/`
- **Typescript**: `typescript/tooling/`

## Usage

Each language directory contains the generated FlatBuffer code for that language.
Include the appropriate files in your project according to your language's conventions.

### Compilers Used
- **flatc**: For C++, C#, Dart, Go, Java, JavaScript, Kotlin, Lobster, Lua, PHP, Python, Rust, Swift, TypeScript
- **flatcc**: For C (recommended for embedded/firmware use)

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
