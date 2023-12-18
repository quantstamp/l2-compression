import brotli
import zlib
import zstd
import lzma
import bz2
import zle
import rle
import bwt


def compress_with_brotli(batch):
    # batch = bytes(batch, encoding="utf-8")
    batch = bytes.fromhex(batch)
    compressed = brotli.compress(batch)
    return compressed.hex()


def compress_with_zlib(batch):
    # batch = bytes(batch, encoding="utf-8")
    batch = bytes.fromhex(batch)
    compressed_data = zlib.compress(batch, 9)
    return compressed_data.hex()


def compress_with_zstd(batch):
    # batch = bytes(batch, encoding="utf-8")
    batch = bytes.fromhex(batch)
    compressed = zstd.compress(batch, 22)
    return compressed.hex()

def compress_with_lzma(batch):
    # batch = bytes(batch, encoding='utf-8')
    batch = bytes.fromhex(batch)
    compressed = lzma.compress(batch, preset=9)
    return compressed.hex()

def compress_with_bz2(batch):
    # batch = bytes(batch, encoding="utf-8")
    batch = bytes.fromhex(batch)
    compressed = bz2.compress(batch, compresslevel = 9)
    return compressed.hex()

def compress_with_zle(batch, with_bwt = False):
    if with_bwt:
        batch=bwt.bwt(batch)
    batch = bytes.fromhex(batch)
    compressed = zle.compress(batch)
    return compressed.hex()

def compress_with_rle(batch, with_bwt = False):
    # batch = bytes.fromhex(batch)
    if with_bwt:
        batch = bwt.bwt(batch)
    compressed = rle.compress(batch)
    return compressed

def compress_with_zle_and_bwt(batch):
    return compress_with_zle(batch, with_bwt=True)

def compress_with_rle_and_bwt(batch):
    return compress_with_rle(batch, with_bwt=True)

def decompress_brotli(batch):
    batch = bytes(batch, encoding="utf-8")
    decompressed = brotli.decompress(batch)
    print(decompressed)