from dataclasses import dataclass, field
from functools import reduce


@dataclass
class MODE:
    size: int = 0
    fmt: str = '{mnemonic:7}'


@dataclass
class INSTRUCTION:
    addr: int = 0
    src: list[int] = field(default_factory=list)
    mode: MODE = field(default_factory=MODE)
    mnemonic: str = '???'
    operand: int = 0

    @property
    def asm(self):
        return self.mode.fmt.format(**vars(self))

    @property
    def hex(self):
        return ' '.join(f'{x:02x}' for x in self.src)

    def __str__(self):
        return f'${self.addr:04x}   {self.hex:12}{self.asm}'


address_modes = {
    'imp': MODE(0, '{mnemonic:7}'),
    'acc': MODE(0, '{mnemonic:7}'),

    'zpy': MODE(1, '{mnemonic:7} ${operand:02X},Y'),
    'zpx': MODE(1, '{mnemonic:7} ${operand:02X},X'),
    'rel': MODE(1, '{mnemonic:7} ${operand:02X}'),
    'zpg': MODE(1, '{mnemonic:7} ${operand:02X}'),
    'imm': MODE(1, '{mnemonic:7} #${operand:02X}'),
    'inx': MODE(1, '{mnemonic:7} (${operand:02X},X)'),
    'iny': MODE(1, '{mnemonic:7} (${operand:02X}),Y'),

    'ind': MODE(2, '{mnemonic:7} (${operand:04X})'),
    'aby': MODE(2, '{mnemonic:7} ${operand:04X},Y'),
    'abx': MODE(2, '{mnemonic:7} ${operand:04X},X'),
    'abs': MODE(2, '{mnemonic:7} ${operand:04X}'),

    'byte': MODE(0, '{mnemonic:7} ${operand:02X}'),
}

mnemonics = [
  'BRK', 'ORA', '???', '???', '???', 'ORA', 'ASL', '???', 'PHP', 'ORA', 'ASL', '???', '???', 'ORA', 'ASL', '???',
  'BPL', 'ORA', '???', '???', '???', 'ORA', 'ASL', '???', 'CLC', 'ORA', '???', '???', '???', 'ORA', 'ASL', '???',
  'JSR', 'AND', '???', '???', 'BIT', 'AND', 'ROL', '???', 'PLP', 'AND', 'ROL', '???', 'BIT', 'AND', 'ROL', '???',
  'BMI', 'AND', '???', '???', '???', 'AND', 'ROL', '???', 'SEC', 'AND', '???', '???', '???', 'AND', 'ROL', '???',
  'RTI', 'EOR', '???', '???', '???', 'EOR', 'LSR', '???', 'PHA', 'EOR', 'LSR', '???', 'JMP', 'EOR', 'LSR', '???',
  'BVC', 'EOR', '???', '???', '???', 'EOR', 'LSR', '???', 'CLI', 'EOR', '???', '???', '???', 'EOR', 'LSR', '???',
  'RTS', 'ADC', '???', '???', '???', 'ADC', 'ROR', '???', 'PLA', 'ADC', 'ROR', '???', 'JMP', 'ADC', 'ROR', '???',
  'BVS', 'ADC', '???', '???', '???', 'ADC', 'ROR', '???', 'SEI', 'ADC', '???', '???', '???', 'ADC', 'ROR', '???',
  '???', 'STA', '???', '???', 'STY', 'STA', 'STX', '???', 'DEY', '???', 'TXA', '???', 'STY', 'STA', 'STX', '???',
  'BCC', 'STA', '???', '???', 'STY', 'STA', 'STX', '???', 'TYA', 'STA', 'TXS', '???', '???', 'STA', '???', '???',
  'LDY', 'LDA', 'LDX', '???', 'LDY', 'LDA', 'LDX', '???', 'TAY', 'LDA', 'TAX', '???', 'LDY', 'LDA', 'LDX', '???',
  'BCS', 'LDA', '???', '???', 'LDY', 'LDA', 'LDX', '???', 'CLV', 'LDA', 'TSX', '???', 'LDY', 'LDA', 'LDX', '???',
  'CPY', 'CMP', '???', '???', 'CPY', 'CMP', 'DEC', '???', 'INY', 'CMP', 'DEX', '???', 'CPY', 'CMP', 'DEC', '???',
  'bNE', 'CMP', '???', '???', '???', 'CMP', 'DEC', '???', 'CLD', 'CMP', '???', '???', '???', 'CMP', 'DEC', '???',
  'CPX', 'SBC', '???', '???', 'CPX', 'SBC', 'INC', '???', 'INX', 'SBC', 'NOP', '???', 'CPX', 'SBC', 'INC', '???',
  'BEQ', 'SBC', '???', '???', '???', 'SBC', 'INC', '???', 'SED', 'SBC', '???', '???', '???', 'SBC', 'INC', '???'
]

addressing = [
  'imp', 'inx', 'imp', 'imp', 'imp', 'zpg', 'zpg', 'imp', 'imp', 'imm', 'acc', 'imp', 'imp', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'imp', 'zpx', 'zpx', 'imp', 'imp', 'aby', 'imp', 'imp', 'imp', 'abx', 'abx', 'imp',
  'abs', 'inx', 'imp', 'imp', 'zpg', 'zpg', 'zpg', 'imp', 'imp', 'imm', 'acc', 'imp', 'abs', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'imp', 'zpx', 'zpx', 'imp', 'imp', 'aby', 'imp', 'imp', 'imp', 'abx', 'abx', 'imp',
  'imp', 'inx', 'imp', 'imp', 'imp', 'zpg', 'zpg', 'imp', 'imp', 'imm', 'acc', 'imp', 'abs', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'imp', 'zpx', 'zpx', 'imp', 'imp', 'aby', 'imp', 'imp', 'imp', 'abx', 'abx', 'imp',
  'imp', 'inx', 'imp', 'imp', 'imp', 'zpg', 'zpg', 'imp', 'imp', 'imm', 'acc', 'imp', 'ind', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'imp', 'zpx', 'zpx', 'imp', 'imp', 'aby', 'imp', 'imp', 'imp', 'abx', 'abx', 'imp',
  'imp', 'inx', 'imp', 'imp', 'zpg', 'zpg', 'zpg', 'imp', 'imp', 'imp', 'imp', 'imp', 'abs', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'zpx', 'zpx', 'zpy', 'imp', 'imp', 'aby', 'imp', 'imp', 'imp', 'abx', 'imp', 'imp',
  'imm', 'inx', 'imm', 'imp', 'zpg', 'zpg', 'zpg', 'imp', 'imp', 'imm', 'imp', 'imp', 'abs', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'zpx', 'zpx', 'zpy', 'imp', 'imp', 'aby', 'imp', 'imp', 'abx', 'abx', 'aby', 'imp',
  'imm', 'inx', 'imp', 'imp', 'zpg', 'zpg', 'zpg', 'imp', 'imp', 'imm', 'imp', 'imp', 'abs', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'imp', 'zpx', 'zpx', 'imp', 'imp', 'aby', 'imp', 'imp', 'imp', 'abx', 'abx', 'imp',
  'imm', 'inx', 'imp', 'imp', 'zpg', 'zpg', 'zpg', 'imp', 'imp', 'imm', 'imp', 'imp', 'abs', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'imp', 'zpx', 'zpx', 'imp', 'imp', 'aby', 'imp', 'imp', 'imp', 'abx', 'abx', 'imp'
]


def disasm(data, base=0):
    instructions = []
    addr = base

    while data:
        opcode = data[0]
        src = [data[0]]
        operand = None

        mnemonic = mnemonics[opcode]
        mode = address_modes[addressing[opcode]]

        if mode.size:
            # XXX: note to self, slicing can extend beyond the end of
            # a sequence without an error.
            operands = data[1:mode.size + 1]
            if len(operands) < mode.size:
                break
            src.extend(operands)
            operand = reduce(lambda x, y: x + (y << 8), operands)

        inst = INSTRUCTION(
            addr=addr,
            src=src,
            mode=mode,
            mnemonic=mnemonic,
            operand=operand,
        )
        addr += mode.size + 1
        data = data[mode.size + 1:]
        instructions.append(inst)

    if data:
        for i, val in enumerate(data):
            instructions.append(INSTRUCTION(
                addr=addr + i,
                src=[val],
                mode=address_modes['byte'],
                mnemonic='.byte',
                operand=val,
            ))

    return instructions


def format(instructions):
    return '\n'.join(str(inst) for inst in instructions) + '\n'
