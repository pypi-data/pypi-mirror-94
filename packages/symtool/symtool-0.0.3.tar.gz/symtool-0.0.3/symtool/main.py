'''symtool, a cli for your Synertek SYM-1

(c) 2021 Lars Kellogg-Stedman <lars@oddbit.com>
'''

import click
import functools
import hexdump
import logging
import sys

from dataclasses import dataclass, field

import symtool
import symtool.disasm
import symtool.symtool


@dataclass
class Config:
    retries: int = 0


@dataclass
class Context:
    sym: symtool.symtool.SYM1 = None
    config: Config = field(default_factory=Config)


def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except symtool.symtool.SYMError as err:
            raise click.ClickException(str(err))

    return wrapper


def needs_connect(func):
    @functools.wraps(func)
    def wrapper(ctx, *args, **kwargs):
        ctx.sym.connect(retries=ctx.config.retries)
        return func(ctx.sym, *args, **kwargs)

    return wrapper


def prefixed_int(v):
    '''Transform a string argument with a numeric prefix into an integer.

    Accepts both standard Python prefixes (0x, 0o, 0b) as well as
    conventional 6502 prefixes ($ for hex, % for binary).
    '''
    if isinstance(v, int):
        return v
    elif v.startswith('$'):
        return int(v[1:], 16)
    elif v.startswith('%'):
        return int(v[1:], 2)
    else:
        return int(v, 0)


@click.group(context_settings=dict(auto_envvar_prefix='SYMTOOL'))
@click.option('--device', '-d', default='/dev/ttyS0',
              help='set serial port (default=/dev/ttyS0)')
@click.option('--speed', '-s', default=4800, type=int,
              help='set port speed (default 4800)')
@click.option('--verbose', '-v', count=True,
              help='enable additional logging')
@click.option('--retries', '-r', type=int,
              help='number of times to retry connection before failing')
@click.pass_context
@handle_exceptions
def main(ctx, device, speed, retries, verbose):
    '''Symtool is a tool for interacting with a SYM-1 computer.

    The SYM-1 is a 6502 based single board computer produced by
    Synertek Systems Corp in 1975. Symtool lets you dump memory,
    load programs into memory, display register contents, and
    start executing code.

    The SYM-1 supports  baud rates from 110bps to 4800bps.
    '''

    try:
        loglevel = ['WARNING', 'INFO', 'DEBUG'][verbose]
    except IndexError:
        loglevel = 'DEBUG'

    logging.basicConfig(level=loglevel)

    config = Config(retries=retries)
    sym = symtool.symtool.SYM1(device, baudrate=speed, timeout=1, debug=(verbose > 2))
    ctx.obj = Context(
        sym=sym,
        config=config,
    )


@main.command()
def version():
    '''Show symtool version'''
    print(f'symtool {symtool.__version__}')


@main.command()
@click.option('--hex/--disassemble', '-h/-d', 'ascii_mode', default=None,
              help='output a hexdump (--hex) or disasssembly (--disassemble)')
@click.option('--output', '-o', type=click.File(mode='wb'), default=sys.stdout.buffer,
              help='output to file instead of stdout')
@click.argument('address', type=prefixed_int)
@click.argument('count', type=prefixed_int, default=1)
@click.pass_obj
@handle_exceptions
@needs_connect
def dump(sym, ascii_mode, output, address, count):
    '''Dump memory from the SYM-1 to stdout or a file.

    By default, the dump command will dump binary data to stdout. You can
    dump to a file instead with the '-o <filename>' option.

    You can request a hex dump with the --hex option, and a disassembly
    by passing --disasseble.
    '''

    if count < 1:
        raise ValueError('count must be >= 1')

    data = sym.dump(address, count)

    with output:
        if ascii_mode is True:
            output.write(hexdump.hexdump(data, result='return').encode('ascii'))
            output.write(b'\n')
        elif ascii_mode is False:
            output.write(symtool.disasm.format(symtool.disasm.disasm(data, base=address)).encode())
        else:
            output.write(data)


@main.command()
@click.option('--seek', '-s', type=prefixed_int,
              help='seek this many bytes into input before reading')
@click.option('--count', '-c', type=prefixed_int,
              help='number of bytes to read')
@click.option('--go', '-g', is_flag=True,
              help='jump to address after loading')
@click.argument('address', type=prefixed_int)
@click.argument('input', type=click.File(mode='rb'), default=sys.stdin.buffer)
@click.pass_obj
@handle_exceptions
@needs_connect
def load(sym, seek, address, count, go, input):
    '''Load binary data from stdin or a file.

    The load command will read bytes from stdin (or an input file, if
    provided) and write them to the SYM-1 starting at <address>. If you
    specify the --go option, symtool will ask the SYM-1 to jump to <address>
    after loading the file.
    '''

    with input:
        if seek:
            input.seek(seek)
        data = input.read(count)
        sym.load(address, data)

        if go:
            sym.go(address)


@main.command()
@click.argument('address', type=prefixed_int)
@click.argument('fillbyte', type=prefixed_int)
@click.argument('count', type=prefixed_int, default=1)
@click.pass_obj
@handle_exceptions
@needs_connect
def fill(sym, address, fillbyte, count):
    '''Fill memory in the SYM-1 with the given byte value.

    The value should be specified as an integer with an optional
    base prefix.  For example, '$FF' or '0xFF' to fill memory with
    the value 255.
    '''

    sym.fill(address, fillbyte=fillbyte, count=count)


@main.command()
@click.pass_obj
@handle_exceptions
@needs_connect
def registers(sym):
    '''Dump 6502 registers'''
    flags = [
        'carry',
        'zero',
        'intr',
        'dec',
        None,
        None,
        'oflow',
        'neg',
    ]

    data = sym.registers()

    for reg, val in data.items():
        print(reg, f'{val:02x} ({val:08b})', end='')
        if reg == 'f':
            for i in range(8):
                if not flags[i]:
                    continue

                print(' {}{}'.format(
                    '+' if val & (1 << i) else '-', flags[i]
                ), end='')
        print()


@main.command()
@click.argument('address', type=prefixed_int)
@click.pass_obj
@handle_exceptions
@needs_connect
def go(sym, address):
    '''Start executing at the given address.

    This calls the monitor's "g" command.
    '''

    sym.go(address)
