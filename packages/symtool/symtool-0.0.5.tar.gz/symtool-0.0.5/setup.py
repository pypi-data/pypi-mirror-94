# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['symtool']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'hexdump>=3.3,<4.0', 'pyserial>=3.5,<4.0']

entry_points = \
{'console_scripts': ['symtool = symtool.main:main']}

setup_kwargs = {
    'name': 'symtool',
    'version': '0.0.5',
    'description': 'A tool for interacting with your SYM-1 microcomputer',
    'long_description': '# symtool\n\nSymtool is a tool for interacting with the `SUPERMON` monitor on a\n[SYM-1][] microcomputer.\n\n[sym-1]: https://en.wikipedia.org/wiki/SYM-1\n\n## Synopsis\n\n```\nUsage: symtool [OPTIONS] COMMAND [ARGS]...\n\n  Symtool is a tool for interacting with a SYM-1 computer.\n\n  The SYM-1 is a 6502 based single board computer produced by Synertek\n  Systems Corp in 1975. Symtool lets you dump memory, load programs into\n  memory, display register contents, and start executing code.\n\n  The SYM-1 supports  baud rates from 110bps to 4800bps.\n\nOptions:\n  -d, --device TEXT    set serial port (default=/dev/ttyS0)\n  -s, --speed INTEGER  set port speed (default 4800)\n  -v, --verbose        enable additional logging (-vv for debug)\n  --help               Show this message and exit.\n\nCommands:\n  dump       Dump memory from the SYM-1 to stdout or a file.\n  fill       Fill memory in the SYM-1 with the given byte value.\n  go         Start executing at the given address.\n  load       Load binary data from stdin or a file.\n  registers  Dump 6502 registers\n```\n\nNumbers (such as memory addresses, counts, etc) can be specified\nusing Python\'s numeric prefixes:\n\n- Decimal (no prefix): `8192`\n- Hexadecimal: `0x2000`\n- Octal: `0o20000`\n- Binary: `0b10000000000000`\n\nAnd in order to meet common 6502 conventions, you can also use `$` as\na prefix on hexadecimal numbers (`$2000`).\n\n## Installation\n\nSymtool is published on PyPi, so you can run:\n\n```\npip install symtool\n```\n\n## Configuration\n\nYou can set the device and speed on the command line using the\n`--device` and `--speed` options (aka `-d` and `-s`), or you can set\nthe `SYMTOOL_DEVICE` and `SYMTOOL_SPEED` variables in your\nenvironment.\n\nThe SYM_1 supports baud rates from 110bps to 4800bps.\n\n## Commands\n\n### Dump memory\n\n```\nUsage: symtool dump [OPTIONS] ADDRESS [COUNT]\n\n  Dump memory from the SYM-1 to stdout or a file.\n\n  By default, the dump command will dump binary data to stdout. You can dump\n  to a file instead with the \'-o <filename>\' option.\n\n  You can request a hex dump with the --hex option, and a disassembly by\n  passing --disasseble.\n\nOptions:\n  -h, --hex / -d, --disassemble  output a hexdump (--hex) or disasssembly\n                                 (--disassemble)\n\n  -o, --output FILENAME          output to file instead of stdout\n  --help                         Show this message and exit.\n```\n\nYou can dump binary output:\n\n```\n$ symtool dump 0x200 16 -o somefile.bin\n```\n\nYou can generate a hexdump:\n\n```\n$ symtool dump 0x200 16 -h\n00000000: A2 FF A0 FF CA D0 FD 88  D0 FA 20 72 89 4C 00 04  .......... r.L..\n```\n\nYou can disassemble the memory:\n\n```\n$ symtool dump 0x200 16 -d\n$0400   a2 ff       LDX #$FF\n$0402   a0 ff       LDY #$FF\n$0404   ca          DEX\n$0405   d0 fd       BNE $FD\n$0407   88          DEY\n$0408   d0 fa       BNE $FA\n$040a   20 72 89    JSR $8972\n$040d   4c 00 04    JMP $0400\n```\n\n### Load memory\n\n```\nUsage: symtool load [OPTIONS] ADDRESS [INPUT]\n\n  Load binary data from stdin or a file.\n\n  The load command will read bytes from stdin (or an input file, if\n  provided) and write them to the SYM-1 starting at <address>. If you\n  specify the --go option, symtool will ask the SYM-1 to jump to <address>\n  after loading the file.\n\nOptions:\n  -s, --seek PREFIXED_INT   seek this many bytes into input before reading\n  -c, --count PREFIXED_INT  number of bytes to read\n  -g, --go                  jump to address after loading\n  --help                    Show this message and exit.\n```\n\nTo load `asm/beeper.bin` into memory at location `$400`:\n\n```\n$ symtool -v load 0x200 asm/beeper.bin\nINFO:symtool.symtool:using port /dev/ttyUSB2\nINFO:symtool.symtool:connecting to sym1...\nINFO:symtool.symtool:connected\nINFO:symtool.symtool:loading 16 bytes of data at $400\n```\n\nSpecify `--go` to execute `g<address>` after loading the program.\n\n### Fill memory\n\n```\nUsage: symtool fill [OPTIONS] ADDRESS FILLBYTE [COUNT]\n\n  Fill memory in the SYM-1 with the given byte value.\n\n  The value should be specified as an integer with an optional base prefix.\n  For example, \'$FF\' or \'0xFF\' to fill memory with the value 255.\n\nOptions:\n  --help  Show this message and exit.\n```\n\nTo fill memory at `$400` with 16 zeros:\n\n```\n$ symtool fill 0x200 0 16\n$ symtool dump 0x200 16 -h\n00000000: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................\n```\n\n### Show registers\n\n```\nUsage: symtool registers [OPTIONS]\n\n  Dump 6502 registers\n\nOptions:\n  --help  Show this message and exit.\n```\n\nExample usage:\n\n\n```\n$ symtool registers\ns ff (11111111)\nf b1 (10110001) +carry -zero -intr -dec -oflow +neg\na 80 (10000000)\nx 00 (00000000)\ny 50 (01010000)\np b0ac (1011000010101100)\n```\n\n### Jump to address\n\n```\nUsage: symtool go [OPTIONS] ADDRESS\n\n  Start executing at the given address.\n\n  This calls the monitor\'s "g" command.\n\nOptions:\n  --help  Show this message and exit.\n```\n\nTo run a program at location `$400`:\n\n```\n$ symtool go 0x200\n```\n\n## Compiling assembly programs\n\nIn order to build the assembler code in the `asm` directory you will\nneed the [ca65][] assembler. The `Makefile` in that\ndirectory will compile the source to `.bin` files that can be loaded\nto your SYM-1 using the `symtool load` command.\n\n[ca65]: https://cc65.github.io/doc/ca65.html\n\nBy default, the generated code expects to be loaded at address\n`0x200`, so you would load it like this:\n\n```\nsymtool load 0x200 message.bin\n```\n\nIf you want to load the code at a different address, you can set an\nexplicit start address on the `make` command line:\n\n```\nmake LD65FLAGS="--start-addr 0x200"\n```\n\nOr  you can edit `sym1.cfg` to change the default start address. For\nexample:\n\n```\nFEATURES {\n    STARTADDRESS: default = $0400;\n}\n```\n',
    'author': 'Lars Kellogg-Stedman',
    'author_email': 'lars@oddbit.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/larsks/symtool',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
