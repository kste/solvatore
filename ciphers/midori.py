from cipher_description import CipherDescription

# Bit permutations for 8-bit S-box
sb_perm = [[4, 1, 6, 3, 0, 5, 2, 7],
           [1, 6, 7, 0, 5, 2, 3, 4],
           [2, 3, 4, 1, 6, 7, 0, 5],
           [7, 4, 1, 2, 3, 0, 5, 6]]

sb_perminv = [[4, 1, 6, 3, 0, 5, 2, 7],
              [3, 0, 5, 6, 7, 4, 1, 2],
              [6, 3, 0, 1, 2, 7, 4, 5],
              [5, 2, 3, 4, 1, 6, 7, 0]]


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

def generate_midori_version(wordsize, rounds):
    # State
    # 0 4  8 12
    # 1 5  9 13
    # 2 6 10 14
    # 3 7 11 15
    if wordsize == 4:
        midori_sbox = [0xC, 0xA, 0xD, 0x3, 0xE, 0xB, 0xF, 0x7,
                       0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6]
    elif wordsize == 8:
        midori_sbox = [0x1, 0x0, 0x5, 0x3, 0xe, 0x2, 0xf, 0x7,
                       0xd, 0xa, 0x9, 0xb, 0xc, 0x8, 0x4, 0x6]


    # Shuffle Cells
    shuffle_cells = []
    for bit in range(wordsize):
        shuffle_cells.append(["s{}".format(wordsize*10 + bit),
                              "s{}".format(wordsize*1 + bit),
                              "s{}".format(wordsize*7 + bit),
                              "s{}".format(wordsize*12 + bit)])
        shuffle_cells.append(["s{}".format(wordsize*5 + bit),
                              "s{}".format(wordsize*2 + bit),
                              "s{}".format(wordsize*14 + bit),
                              "s{}".format(wordsize*4 + bit)])
        shuffle_cells.append(["s{}".format(wordsize*15 + bit),
                              "s{}".format(wordsize*3 + bit),
                              "s{}".format(wordsize*9 + bit),
                              "s{}".format(wordsize*8 + bit)])
        shuffle_cells.append(["s{}".format(wordsize*11 + bit),
                              "s{}".format(wordsize*6 + bit)])

    midori = CipherDescription(wordsize * 16)
    midori.add_sbox('S-box', midori_sbox)

    # SubCell
    for i in range(16):
        if wordsize == 4:
            bits = ["s{}".format(4*i + 3),
                    "s{}".format(4*i + 2),
                    "s{}".format(4*i + 1),
                    "s{}".format(4*i + 0)]
            midori.apply_sbox('S-box', bits, bits)
        else:
            # Apply bit permutation
            bit_perm = [sb_perm[i % 4][j] for j in range(8)]
            for cycle in decompose_permutation(bit_perm):
                cycle_bits = []
                for v in cycle:
                    cycle_bits.append("s{}".format(8*i + v))
                midori.apply_permutation(cycle_bits)
            # Apply S-box
            bits = ["s{}".format(8*i + 0),
                    "s{}".format(8*i + 1),
                    "s{}".format(8*i + 2),
                    "s{}".format(8*i + 3)]
            midori.apply_sbox('S-box', bits, bits)
            bits = ["s{}".format(8*i + 4),
                    "s{}".format(8*i + 5),
                    "s{}".format(8*i + 6),
                    "s{}".format(8*i + 7)]
            midori.apply_sbox('S-box', bits, bits)
            # Apply bit permutation
            bit_perm = [8*i + sb_perminv[i % 4][j] for j in range(8)]
            for cycle in decompose_permutation(bit_perm):
                cycle_bits = []
                for v in cycle:
                    cycle_bits.append("s{}".format(8*i + v))
                midori.apply_permutation(cycle_bits)


    # ShuffleCell
    for shuffle in shuffle_cells:
        midori.apply_permutation(shuffle)

    # MixColumn
    for col in range(4):
        for bit in range(wordsize):
            x0 = "s{}".format(bit + col*wordsize*4)
            x1 = "s{}".format(bit + wordsize + col*wordsize*4)
            x2 = "s{}".format(bit + 2*wordsize + col*wordsize*4)
            x3 = "s{}".format(bit + 3*wordsize + col*wordsize*4)

            midori.apply_xor(x0, x1, "txor01")
            midori.apply_xor(x0, x2, "txor02")
            midori.apply_xor(x1, x2, "txor12")

            midori.apply_xor(x1, "txor12", "tx2")

            midori.apply_xor("txor12", x3, x0)
            midori.apply_xor("txor02", x3, x1)
            midori.apply_xor("txor01", x3, x2)
            midori.apply_xor("txor01", "tx2", x3)
            # midori.apply_xor(x0, x1, "txor01")
            # midori.apply_xor("txor01", x2, "tx3p")
            #
            # midori.apply_xor("txor01", x3, "tx2p")
            #
            # midori.apply_xor(x0, x2, "txor02")
            # midori.apply_xor("txor02", x3, "tx1p")
            #
            # midori.apply_xor(x1, x2, "txor12")
            # midori.apply_xor("txor12", x3, "tx0p")
            #
            # midori.apply_mov("tx0p", x0)
            # midori.apply_mov("tx1p", x1)
            # midori.apply_mov("tx2p", x2)
            # midori.apply_mov("tx3p", x3)


    return midori
midori64 = generate_midori_version(4, 16)
midori128 = generate_midori_version(8, 20)
