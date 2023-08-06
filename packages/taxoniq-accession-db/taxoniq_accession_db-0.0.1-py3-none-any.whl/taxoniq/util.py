def byte_to_bases(x):
    c = (x >> 4) & 0xf
    f = x & 0xf
    cc = (c >> 2) & 0x3
    cf = c & 0x3
    fc = (f >> 2) & 0x3
    ff = f & 0x3
    return ''.join(twobit2ascii[i] for i in (cc, cf, fc, ff))


twobit2ascii = {0: "A", 1: "C", 2: "G", 3: "T"}
twobit2ascii_byte_lut = {x: byte_to_bases(x) for x in range(256)}
