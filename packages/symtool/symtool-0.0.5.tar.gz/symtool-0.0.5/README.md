# symtool

Symtool is a tool for interacting with the `SUPERMON` monitor on a
[SYM-1][] microcomputer.

[sym-1]: https://en.wikipedia.org/wiki/SYM-1

## Synopsis

```
Usage: symtool [OPTIONS] COMMAND [ARGS]...

  Symtool is a tool for interacting with a SYM-1 computer.

  The SYM-1 is a 6502 based single board computer produced by Synertek
  Systems Corp in 1975. Symtool lets you dump memory, load programs into
  memory, display register contents, and start executing code.

  The SYM-1 supports  baud rates from 110bps to 4800bps.

Options:
  -d, --device TEXT    set serial port (default=/dev/ttyS0)
  -s, --speed INTEGER  set port speed (default 4800)
  -v, --verbose        enable additional logging (-vv for debug)
  --help               Show this message and exit.

Commands:
  dump       Dump memory from the SYM-1 to stdout or a file.
  fill       Fill memory in the SYM-1 with the given byte value.
  go         Start executing at the given address.
  load       Load binary data from stdin or a file.
  registers  Dump 6502 registers
```

Numbers (such as memory addresses, counts, etc) can be specified
using Python's numeric prefixes:

- Decimal (no prefix): `8192`
- Hexadecimal: `0x2000`
- Octal: `0o20000`
- Binary: `0b10000000000000`

And in order to meet common 6502 conventions, you can also use `$` as
a prefix on hexadecimal numbers (`$2000`).

## Installation

Symtool is published on PyPi, so you can run:

```
pip install symtool
```

## Configuration

You can set the device and speed on the command line using the
`--device` and `--speed` options (aka `-d` and `-s`), or you can set
the `SYMTOOL_DEVICE` and `SYMTOOL_SPEED` variables in your
environment.

The SYM_1 supports baud rates from 110bps to 4800bps.

## Commands

### Dump memory

```
Usage: symtool dump [OPTIONS] ADDRESS [COUNT]

  Dump memory from the SYM-1 to stdout or a file.

  By default, the dump command will dump binary data to stdout. You can dump
  to a file instead with the '-o <filename>' option.

  You can request a hex dump with the --hex option, and a disassembly by
  passing --disasseble.

Options:
  -h, --hex / -d, --disassemble  output a hexdump (--hex) or disasssembly
                                 (--disassemble)

  -o, --output FILENAME          output to file instead of stdout
  --help                         Show this message and exit.
```

You can dump binary output:

```
$ symtool dump 0x200 16 -o somefile.bin
```

You can generate a hexdump:

```
$ symtool dump 0x200 16 -h
00000000: A2 FF A0 FF CA D0 FD 88  D0 FA 20 72 89 4C 00 04  .......... r.L..
```

You can disassemble the memory:

```
$ symtool dump 0x200 16 -d
$0400   a2 ff       LDX #$FF
$0402   a0 ff       LDY #$FF
$0404   ca          DEX
$0405   d0 fd       BNE $FD
$0407   88          DEY
$0408   d0 fa       BNE $FA
$040a   20 72 89    JSR $8972
$040d   4c 00 04    JMP $0400
```

### Load memory

```
Usage: symtool load [OPTIONS] ADDRESS [INPUT]

  Load binary data from stdin or a file.

  The load command will read bytes from stdin (or an input file, if
  provided) and write them to the SYM-1 starting at <address>. If you
  specify the --go option, symtool will ask the SYM-1 to jump to <address>
  after loading the file.

Options:
  -s, --seek PREFIXED_INT   seek this many bytes into input before reading
  -c, --count PREFIXED_INT  number of bytes to read
  -g, --go                  jump to address after loading
  --help                    Show this message and exit.
```

To load `asm/beeper.bin` into memory at location `$400`:

```
$ symtool -v load 0x200 asm/beeper.bin
INFO:symtool.symtool:using port /dev/ttyUSB2
INFO:symtool.symtool:connecting to sym1...
INFO:symtool.symtool:connected
INFO:symtool.symtool:loading 16 bytes of data at $400
```

Specify `--go` to execute `g<address>` after loading the program.

### Fill memory

```
Usage: symtool fill [OPTIONS] ADDRESS FILLBYTE [COUNT]

  Fill memory in the SYM-1 with the given byte value.

  The value should be specified as an integer with an optional base prefix.
  For example, '$FF' or '0xFF' to fill memory with the value 255.

Options:
  --help  Show this message and exit.
```

To fill memory at `$400` with 16 zeros:

```
$ symtool fill 0x200 0 16
$ symtool dump 0x200 16 -h
00000000: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
```

### Show registers

```
Usage: symtool registers [OPTIONS]

  Dump 6502 registers

Options:
  --help  Show this message and exit.
```

Example usage:


```
$ symtool registers
s ff (11111111)
f b1 (10110001) +carry -zero -intr -dec -oflow +neg
a 80 (10000000)
x 00 (00000000)
y 50 (01010000)
p b0ac (1011000010101100)
```

### Jump to address

```
Usage: symtool go [OPTIONS] ADDRESS

  Start executing at the given address.

  This calls the monitor's "g" command.

Options:
  --help  Show this message and exit.
```

To run a program at location `$400`:

```
$ symtool go 0x200
```

## Compiling assembly programs

In order to build the assembler code in the `asm` directory you will
need the [ca65][] assembler. The `Makefile` in that
directory will compile the source to `.bin` files that can be loaded
to your SYM-1 using the `symtool load` command.

[ca65]: https://cc65.github.io/doc/ca65.html

By default, the generated code expects to be loaded at address
`0x200`, so you would load it like this:

```
symtool load 0x200 message.bin
```

If you want to load the code at a different address, you can set an
explicit start address on the `make` command line:

```
make LD65FLAGS="--start-addr 0x200"
```

Or  you can edit `sym1.cfg` to change the default start address. For
example:

```
FEATURES {
    STARTADDRESS: default = $0400;
}
```
