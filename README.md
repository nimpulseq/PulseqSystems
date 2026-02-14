# PulseqSystems

PulseqSystems provides a bundled collection of MR system specifications (e.g. gradient configurations) intended to be used with pulse sequence tooling such as pypulseq.

This repository packages MRSystems.json and utilities to load/query the available manufacturers, models and gradient configurations. The primary target is pypulseq (https://github.com/imr-framework/pypulseq), but the data and utilities can be consumed from both Python and Nim projects.

## Features

- Packaged MR system specifications (JSON) for common scanner models.
- Helpers to list manufacturers, models, gradients and to retrieve pulseq specs.
- Designed to be installed as a Python package and used together with pypulseq.
- Data is plain JSON and can be parsed from other languages (Nim, etc.).

## Usage

### Raw specifications in JSON format
- The MRSystems.json file contains the specifications. You can parse this file directly in any language that supports JSON to access the data.
- The file is located under src/pulseq_systems/MRSystems.json in the repository.

### Python
- Import the package and use the provided helpers to list systems and obtain pulseq-compatible parameters.
- Typical workflow: install the package, then call functions to get gradient limits and slew rate for use with pypulseq.

### Nim
- The JSON file(s) are distributed with the package. After installation or by copying the JSON, Nim programs can parse MRSystems.json with any JSON library to obtain the same system specifications.

## Python API

The package ships a small helper module (src/pulseq_systems/get_systems.py) to load and query the bundled MRSystems.json. Main functions:

- list_manufacturers() -> list[str]
  - Return a list of manufacturer names present in MRSystems.json.
- list_models(manufacturer: str) -> list[str]
  - Return a list of model names for a given manufacturer.
- list_gradients(manufacturer: str, model: str) -> list[str]
  - Return available gradient configuration names for the given model.
- get_pulseq_specs(manufacturer: str, model: str, gradient: str = None) -> dict
  - Return pulseq-relevant parameters. The returned dict includes:
    - grad_unit (e.g. "mT/m")
    - max_grad (float)
    - slew_unit (e.g. "T/m/s")
    - max_slew (float)
    - B0 (float, field strength in T)
  - If gradient is omitted, the first available gradient configuration is used.
- get_metadata() -> dict
  - Return top-level metadata from MRSystems.json.

Example (after installing the package):
```python
from pulseq_systems import list_manufacturers, get_pulseq_specs

manufacturers = list_manufacturers()
specs = get_pulseq_specs("Siemens", "Prisma")
```

## Nim

A Nim module (src/pulseq_systems.nim) is provided so the same JSON data can be consumed from Nim code. The Nim module exposes:

- listManufacturers(): seq[string]
- listModels(manufacturer: string): seq[string]
- listGradients(manufacturer: string, model: string): seq[string]
- getPulseqSpecs(manufacturer: string, model: string, gradient: string = ""): SystemSpec

SystemSpec fields:
- B0: float64
- maxSlew: float64
- maxGrad: float64
- slewUnit: string
- gradUnit: string

Usage (Nim):
```nim
import pulseq_systems
echo listManufacturers()
let spec = getPulseqSpecs("Siemens", "Prisma")
```

Installation note:
- The JSON data is plain MRSystems.json bundled with the project. You can install the Nim module as a Nim package (nimble) or include the module and JSON in your Nim project. Ensure the JSON path is correct relative to your installed module or copy MRSystems.json alongside the Nim module when packaging.

## Credits and disclaimer 

The JSON file has been compiled with the help of a large language model (Claude Opus 4.6) from publicly available sources and may not be exhaustive or perfectly accurate. No warranty is implied or explicitly granted. Please verify the specifications with official sources if you intend to use them for critical applications.

## References

- pulseq - open format for MR sequences: https://github.com/pulseq/pulseq/
- pypulseq — pulse sequence toolbox for Python: https://github.com/imr-framework/pypulseq

## Contributing

Contributions (additional systems, corrections) are welcome. Please open an issue or a pull request with changes to the JSON or helper code.

## License

This package is released under a MIT license.
Please refer to the repository LICENSE file for licensing details.
