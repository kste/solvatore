from cipher_description import CipherDescription

def maj(cipher, a, b, c, out):
    cipher.apply_and(a, b, "t1")
    cipher.apply_and(a, c, "t2")
    cipher.apply_and(b, c, "t3")
    cipher.apply_xor("t1", "t2", "t4")
    cipher.apply_xor("t3", "t4", out)

def ch(cipher, a, b, c, out):
    cipher.apply_and(a, b, "t1")
    cipher.apply_and(a, c, "t2") # TODO: Add not to first parameter
    cipher.apply_xor("t1", "t2", out)

acorn = CipherDescription(293)

# Compute Keystream Bit
# k = s12 + s154 + maj(s256, s61, s193)

# Majority
maj(acorn, "s256", "s61", "s193", "tmaj1")
acorn.apply_xor("s12", "s154", "t1")
acorn.apply_xor("t1", "tmaj1", "tk")

# Update State
acorn.apply_xor("s289", "s235", "t1")
acorn.apply_xor("t1", "s230", "s289")
acorn.apply_xor("s230", "s196", "t1")
acorn.apply_xor("t1", "s193", "s230")
acorn.apply_xor("s193", "s160", "t1")
acorn.apply_xor("t1", "s154", "s193")
acorn.apply_xor("s154", "s111", "t1")
acorn.apply_xor("t1", "s107", "s154")
acorn.apply_xor("s107", "s66", "t1")
acorn.apply_xor("t1", "s61", "s107")
acorn.apply_xor("s61", "s23", "t1")
acorn.apply_xor("t1", "s0", "s61")

# Compute Feedback Bit
# f = s0 + ~s107 + maj(s244, s23, s160) + ch(s230, s111, s66) + s196 + k
maj(acorn, "s244", "s23", "s160", "tmaj2")
ch(acorn, "s230", "s111", "s66", "tch")
acorn.apply_xor("s0", "s107", "t1") # TODO: Add not to second parameter
acorn.apply_xor("t1", "tmaj2", "t2")
acorn.apply_xor("t2", "tch", "t3")
acorn.apply_xor("t3", "s196", "t4")
acorn.apply_xor("t4", "tk", "s0") # s0 gets feedback bit

# Shift everything
permutation = tuple("s{}".format(i) for i in range(292, -1, -1))
acorn.apply_permutation(permutation)

acorn.set_rounds(1536)
