from cipher_description import CipherDescription

# State arranged as 25 lanes indexed as:
#  0  1  2  3  4
#  5  6  7  8  9
# 10 11 12 13 14
# 15 16 17 18 19
# 20 21 22 23 24

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

# State size
b = 200
lanesize = b // 25

keccak_sbox = [0x0,0x5,0xa,0xb,0x14,0x11,0x16,0x17,
               0x9,0xc,0x3,0x2,0xd,0x8,0xf,0xe,
               0x12,0x15,0x18,0x1b,0x6,0x1,0x4,0x7,
               0x1a,0x1d,0x10,0x13,0x1e,0x19,0x1c,0x1f]

rot_const = [[0,  36,  3, 41, 18],
             [1,  44, 10, 45,  2],
             [62,  6, 43, 15, 61],
             [28, 55, 25, 21, 56],
             [27, 20, 39, 8, 14]]


keccak = CipherDescription(b)
keccak.add_sbox('S-box', keccak_sbox)

# Theta
for col in range(5):
    for bit in range(lanesize):
        row_1 = "s{}".format(bit + col*lanesize)
        row_2 = "s{}".format(bit + 5*lanesize + col*lanesize)
        row_3 = "s{}".format(bit + 10*lanesize + col*lanesize)
        row_4 = "s{}".format(bit + 15*lanesize + col*lanesize)
        row_5 = "s{}".format(bit + 20*lanesize + col*lanesize)

        #TODO: Add XOR with multiple inputs?
        xor_1 = "tC0{}".format(bit + lanesize*col)
        xor_2 = "tC1{}".format(bit + lanesize*col)
        xor_3 = "tC2{}".format(bit + lanesize*col)
        xor_C = "tC_{}".format(bit + lanesize*col)

        keccak.apply_xor(row_1, row_2, xor_1)
        keccak.apply_xor(xor_1, row_3, xor_2)
        keccak.apply_xor(xor_2, row_4, xor_3)
        keccak.apply_xor(xor_3, row_5, xor_C)

for col in range(5):
    for bit in range(lanesize):
        C = "tC_{}".format(bit + lanesize*((col - 1) % 5)) # C[col-1]
        Crot = "tC_{}".format((bit - 1) % lanesize + lanesize*((col + 1) % 5)) # C[col+1] <<< 1
        xor_D = "tD{}".format(bit + lanesize*col)
        keccak.apply_xor(C, Crot, xor_D)

for row in range(5):
    for col in range(5):
        for bit in range(lanesize):
            x = "s{}".format(bit + lanesize*col + (5*row)*lanesize)
            D = "tD{}".format(bit + lanesize*col)
            keccak.apply_xor(x, D, x)

# Rho
for row in range(5):
    for col in range(5):
        bit = col*lanesize + (5*row*lanesize)
        rot_perm = [(i + rot_const[col][row]) % lanesize for i in range(lanesize)]
        for cycle in decompose_permutation(rot_perm):
            cycle_bits = []
            for v in cycle:
                cycle_bits.append("s{}".format(v + bit))
            keccak.apply_permutation(cycle_bits)

# Pi
pi_perm = [1, 15, 22, 16, 12,
           13, 3, 20, 11, 23,
           6, 9, 4, 10, 8,
           14, 18, 17, 2, 5,
           19, 7, 24, 21]

for bit in range(lanesize):
    perm = ['s{}'.format(i*lanesize + bit) for i in pi_perm]
    keccak.apply_permutation(perm)


for row in range(5):
    for bit in range(lanesize):
        bits = ["s{}".format(bit + (5*row)*lanesize),
                "s{}".format(bit + (5*row)*lanesize + lanesize),
                "s{}".format(bit + (5*row)*lanesize + 2*lanesize),
                "s{}".format(bit + (5*row)*lanesize + 3*lanesize),
                "s{}".format(bit + (5*row)*lanesize + 4*lanesize)]
        keccak.apply_sbox('S-box', bits, bits)
