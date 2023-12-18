from sample_batch import x
from compression_algorithms import compress_with_zle, compress_with_rle
from bwt import bwt

x = compress_with_rle(x)
print(len(x)) # 144278

y = bwt(x) 
y = y.replace("\002", "")
y = y.replace("\003", "")

print("bwt length", len(y)) # 144278 -- sanity check

print("rle length", len(compress_with_rle(x)))

z = compress_with_rle(y) 
print("rle on bwt length", len(z)) # 98548

w = compress_with_zle(x)
print("zle length", len(w)) # 78878

print("zle on bwt length", len(compress_with_zle(y))) # 76920