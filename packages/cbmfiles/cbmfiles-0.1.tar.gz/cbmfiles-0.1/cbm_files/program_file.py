import struct

from .basic_file import BASICFile
from .binary_file import BinaryFile


def ProgramFile(fileh, token_set='basic-v2', encoding='petscii-c64en-uc'):
    # read start address from file
    start_addr, = struct.unpack('<H', fileh.read(2))

    if start_addr & 0xFF == 1:
        # BASIC starts at 0x..01
        return BASICFile(fileh, start_addr, token_set=token_set, encoding=encoding)

    return BinaryFile(fileh, start_addr)
