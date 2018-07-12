"""
Implementation of the Gimli permutation.

"""
from cipher_description import CipherDescription

def decompose_permutation(perm):
    cycles = []

    d = dict((i, int(x)) for i, x in enumerate(perm))

    while d:
        x = list(d)[0]
        cycle = []
        while x in d:
            cycle.append(x)
            x = d.pop(x)
        cycles.append(cycle)
    return cycles

def rotate(cipher, bit, rot):
    rot_perm = [(i + rot) % wordsize for i in range(wordsize)]
    for cycle in decompose_permutation(rot_perm):
        cycle_bits = []
        for v in cycle:
            cycle_bits.append("s{}".format(v + bit))
        cipher.apply_permutation(cycle_bits)

gimli = CipherDescription(96)
wordsize = 32

a = 2
b = 1
c = 3
d = 26
e = 9
f = 0

# newz = rotate(x ^ (z << 1) ^ ((y&z) << a),d);
# newy = rotate(y ^ x        ^ ((x|z) << b),e);
# newx = rotate(z ^ y        ^ ((x&y) << c),f);

# new z
for bit in range(32):
    gimli.apply_and("s{}".format(wordsize + bit), "s{}".format(2*wordsize + bit), "tand0{}".format(bit))

for bit in range(a, 32):
    gimli.apply_xor("s{}".format(0 + bit), "tand0{}".format(bit - a), "txor{}".format(bit))
for bit in range(0, a):
    gimli.apply_and("s{}".format(0 + bit), "s{}".format(0 + bit), "txor{}".format(bit))

for bit in range(0, 1):
    gimli.apply_and("txor{}".format(bit), "txor{}".format(bit), "tnewz{}".format(bit))
for bit in range(1, 32):
    gimli.apply_xor("txor{}".format(bit), "s{}".format(2*wordsize + bit - 1), "tnewz{}".format(bit))



# new z
for bit in range(32):
    gimli.apply_and("s{}".format(0 + bit), "s{}".format(2*wordsize + bit), "tor{}".format(bit)) # TODO: Replace with or?

for bit in range(b, 32):
    gimli.apply_xor("s{}".format(0 + bit), "tor{}".format(bit - b), "txor{}".format(bit))

for bit in range(0, b):
    gimli.apply_and("s{}".format(wordsize + bit), "s{}".format(wordsize + bit), "tnewy{}".format(bit))
for bit in range(b, 32):
    gimli.apply_xor("txor{}".format(bit), "s{}".format(wordsize + bit), "tnewy{}".format(bit))



# new z
for bit in range(32):
    gimli.apply_and("s{}".format(0 + bit), "s{}".format(wordsize + bit), "tand{}".format(bit))

for bit in range(c, 32):
    gimli.apply_xor("s{}".format(wordsize + bit), "tor{}".format(bit - c), "txor{}".format(bit))

for bit in range(0, c):
    gimli.apply_and("s{}".format(2*wordsize + bit), "s{}".format(2*wordsize + bit), "tnewx{}".format(bit))
for bit in range(c, 32):
    gimli.apply_xor("txor{}".format(bit), "s{}".format(2*wordsize + bit), "tnewx{}".format(bit))

# Assign values
for bit in range(wordsize):
    gimli.apply_and("tnewx{}".format(bit), "tnewx{}".format(bit), "s{}".format(bit))
    gimli.apply_and("tnewy{}".format(bit), "tnewy{}".format(bit), "s{}".format(wordsize + bit))
    gimli.apply_and("tnewz{}".format(bit), "tnewz{}".format(bit), "s{}".format(2*wordsize + bit))

# Rotate
rotate(gimli, 2*wordsize, d)
rotate(gimli, wordsize, e)
rotate(gimli, 0, f)
