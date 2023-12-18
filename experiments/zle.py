#from https://github.com/ethereum/pyethereum/blob/develop-snapshot/ethereum/compress.py

from eth_utils import int_to_big_endian
from rlp.utils import decode_hex, ascii_chr


NULLSHA3 = decode_hex('c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470')

def int_to_bytes(value):
    if isinstance(value, bytes):
        return value
    return int_to_big_endian(value)

def safe_ord(value):
    if isinstance(value, int):
        return value
    else:
        return ord(value)

def compress(data):
    o = b''
    i = 0
    while i < len(data):
        if int_to_bytes(data[i]) == b'\xfe':
            o += b'\xfe\x00'
        elif data[i:i + 32] == NULLSHA3:
            o += b'\xfe\x01'
            i += 31
        elif data[i:i + 2] == b'\x00\x00':
            p = 2
            while p < 255 and i + p < len(data) and int_to_bytes(data[i + p]) == b'\x00':
                p += 1
            o += b'\xfe' + ascii_chr(p)
            i += p - 1
        else:
            o += int_to_bytes(data[i])
        i += 1
    return o


def decompress(data):
    o = b''
    i = 0
    while i < len(data):
        if data[i: i + 1] == b'\xfe':
            if i == len(data) - 1:
                raise Exception("Invalid encoding, \\xfe at end")
            elif data[i + 1: i + 2] == b'\x00':
                o += b'\xfe'
            elif data[i + 1: i + 2] == b'\x01':
                o += NULLSHA3
            else:
                o += b'\x00' * safe_ord(data[i + 1])
            i += 1
        else:
            o += data[i: i + 1]
        i += 1
    return o

