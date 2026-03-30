## FPGA Assembly (FASM) Parser and Generation library

This repository documents the FASM file format and provides parsing libraries and simple tooling for working with FASM files.

It provides a pure Python parser based on `textx` for parsing and generating FASM files.

## Installation

    pip install fasm

## Development

    pip install -e ".[dev]"
    pytest tests/

## FPGA Assembly (FASM)

FPGA Assembly is a file format designed by the
[F4PGA Project](https://f4pga.org/) developers to provide a plain
text file format for configuring the internals of an FPGA.

It is designed to allow FPGA place and route to not care about the *actual*
bitstream format used on an FPGA.

![FASM Ecosystem Diagram](docs/_static/image/fasm-diagram.png)

### Properties

 * Removing a line from a FASM file leaves you with a valid FASM file.
 * Allow annotation with human readable comments.
 * Allow annotation with "computer readable" comments.
 * Has syntactic sugar for expressing memory / lut init bits / other large
   arrays of data.
 * Has a canonical form.
 * Does not require any specific bitstream format.

### Supported By

FASM is currently supported by the
[F4PGA Verilog to Routing fork](https://github.com/f4pga/vtr-verilog-to-routing),
but we hope to get it merged upstream sometime soon.

It is also used by [Project X-Ray](https://github.com/f4pga/prjxray).
