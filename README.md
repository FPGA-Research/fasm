## FPGA Assembly (FASM) Parser and Generation library

This is a fork of [chipsalliance/fasm](https://github.com/chipsalliance/fasm), adapted for use in the [FABulous](https://github.com/FPGA-Research/FABulous) flow. The original repository is no longer actively maintained.

This fork removes the ANTLR-based C++ parser that was present in the original. The original library shipped two parsers — a fast C++/ANTLR parser and a pure Python textX fallback — and would print a confusing runtime warning whenever ANTLR was not installed. Since FABulous only needs the textX parser and the ANTLR build required cmake, Java, and native libraries, the C++ parser has been removed entirely to keep installation simple and warning-free.

This repository documents the FASM file format and provides parsing libraries and simple tooling for working with FASM files using a pure Python parser based on `textx`.

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
