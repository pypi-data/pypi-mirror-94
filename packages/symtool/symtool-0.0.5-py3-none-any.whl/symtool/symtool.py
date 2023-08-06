import functools
import logging
import serial
import time

LOG = logging.getLogger(__name__)


class SYMError(Exception):
    '''Parent class for exceptions raised by this module.'''

    def __init__(self, *args):
        if not args:
            args = self.__doc__.splitlines()[0]

        super().__init__(args)


class TimeoutError(SYMError):
    '''Timeout waiting for data

    Note that this may simply mean that we're out of sync with the
    monitor (e.g., code has called read_until('.') but the monitor
    is waiting for input).
    '''


class CommandError(SYMError):
    '''Received error response from monitor

    This exception is raised when we receive an 'ER xx' response
    from the monitor.'''

    def __init__(self, code):
        self.code = code
        super().__init__(f'Received error {code} from monitor')


class DisconnectedError(SYMError):
    '''Attempt to communicate with SYM-1 before calling connect'''


def stripped(i):
    return (x.strip() for x in i)


def connected(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._connected:
            raise DisconnectedError()

        return func(self, *args, **kwargs)

    return wrapper


class DelayedSerial(serial.Serial):
    def __init__(self, port, debug=False, character_interval=None,
                 baudrate=None, timeout=None, **kwargs):
        baudrate = 4800 if baudrate is None else baudrate
        timeout = 1 if timeout is None else timeout
        character_interval = 0.05 if character_interval is None else character_interval

        if baudrate > 4800:
            LOG.warning('SYM-1 max baud rate is 4800bps')

        self._debug = debug
        self._character_interval = character_interval

        super().__init__(baudrate=baudrate, timeout=timeout, **kwargs)
        self.port = port
        LOG.info('using port %s @ %sbps', self.port, self.baudrate)

    def open(self):
        LOG.info('connecting to port %s @ %sbps', self.port, self.baudrate)
        super().open()

    def read(self, count):
        '''Read bytes from the SYM-1.'''

        data = super().read(count)
        if data == b'':
            raise TimeoutError()
        if self._debug:
            print('R', repr(data))
        return data

    def write(self, data):
        '''Write data to the SYM-1.

        This will convert any string data to bytes by calling
        data.encode(). If you don't want that, just call it with
        bytes instead.
        '''

        if isinstance(data, str):
            data = data.encode()

        if self._debug:
            print('W', repr(data))

        nbytes = 0
        for ch in data:
            nbytes += super().write(bytes([ch]))
            time.sleep(self._character_interval)

        return nbytes

    def read_until(self, data):
        if isinstance(data, str):
            data = data.encode()

        return super().read_until(data)


class SYM1:
    def __init__(self, port, *args, **kwargs):
        self._last_err = None
        self._last_command = None
        self._connected = False
        self._dev = DelayedSerial(port, **kwargs)

    def send_command(self, cmd, *args):
        '''Send a command and parameters to the monitor.'''

        LOG.debug('send command: %s %s', cmd, args)
        self._last_command = (cmd, args)
        self._dev.write(cmd)

        for i, arg in enumerate(args):
            if i != 0:
                self._dev.write(',')
            self._dev.write(arg)

        self._dev.write('\r')
        self._dev.read_until(b'\r\n')

    def return_to_prompt(self, send_cr=False):
        '''Cancel command and return to monitor prompt.

        This send a <cr>, then reads everything until the
        monitor prompt. Returns a list of response lines.
        '''

        LOG.debug('waiting for prompt')

        if send_cr:
            self._dev.write('\r')

        # XXX: single character markers make me nervous. Previously this
        # was read_until(b'\r\n.'), but changed because the 'f' (fill)
        # command returns directly to the prompt, and the '\r\n'
        # is consumed by send_command().
        res = self._dev.read_until(b'.')
        lines = [line for line in stripped(res.splitlines()) if line]
        for line in lines:
            if line.startswith(b'ER '):
                code = int(line.strip().split()[1], 16)
                self._last_err = code
                raise CommandError(code)

        # return everything but the prompt
        return lines[:-1]

    def connect(self, retries=None):
        '''Intiailize connection to the SYM-1.

        Send a 'q' character out the serial port to trigger the SYM-1
        auto baud detection. Handle any error response if the SYM-1
        serial prompt was already active.
        '''

        self._dev.open()

        while True:
            self._dev.write('q')
            try:
                self._dev.read(1)
                break
            except TimeoutError:
                if retries is not None:
                    if retries == 0:
                        raise
                    retries -= 1

            LOG.warning('failed to connect on %s; retrying...', self._dev.port)
            time.sleep(1)

        LOG.info('connected')

        self._dev.write('\r')

        # We expect a CommandError here, since if the SYM-1 was
        # already connected we just send the invalid "q" command.
        try:
            self.return_to_prompt()
        except CommandError as err:
            if err.code != 0x51:
                raise

        # Flush input buffer. This takes care of any extra output caused
        # by the monitor being in an unknown state when we started.
        try:
            self._dev.read_all()
        except TimeoutError:
            pass

        self._connected = True

    @connected
    def registers(self):
        '''Read register contents.'''

        self.send_command('r')
        self._dev.read_until(b',')

        reg = {}
        for regname in ['s', 'f', 'a', 'x', 'y', 'p']:
            self._dev.write('>')
            self._dev.read_until(b'>')
            res = self._dev.read_until(b',')
            data = res.strip().split(b',')[0]
            _regname, val = data.split()
            if _regname.decode().lower() != regname:
                raise KeyError(f'unexpected register name ({_regname} != {regname}')
            reg[regname] = int(val, 16)

        self.return_to_prompt(True)
        return reg

    @connected
    def dump(self, addr, count=1):
        '''Read bytes from memory.'''

        LOG.info('reading %d bytes of data from $%X', count, addr)
        self.send_command('m', f'{addr:x}'.encode())
        data = []
        for i in range(count):
            addr = self._dev.read_until(b',')
            val = self._dev.read_until(b',')
            data.append(int(val[:-1], 16))
            self._dev.write('>')
            self._dev.read_until(b'\r\n')

        self.return_to_prompt(True)
        return bytes(data)

    @connected
    def load(self, addr, data):
        '''Write bytes to memory'''

        LOG.info('loading %d bytes of data at $%X', len(data), addr)
        self.send_command('d', f'{addr:x}'.encode())
        for val in data:
            self._dev.write(f'{val:02x}'.encode())
            self._dev.read_until(b' ')

        self.return_to_prompt(True)

    @connected
    def go(self, addr):
        '''Start executing at addr.'''

        LOG.info('jump to subroutine at %X', addr)
        self.send_command('g', f'{addr:x}'.encode())

    @connected
    def fill(self, addr, fillbyte=0, count=1):
        '''Fill memory with the specified fillbyte (default 0).'''

        LOG.info('fill %d bytes of memory at $%X with %r',
                 count, addr, fillbyte)
        end = addr + (count-1)
        self.send_command('f', f'{fillbyte:x}', f'{addr:x}', f'{end:x}')
        self.return_to_prompt()
