"""
Implementation of the NORX permutation.

https://norx.io

"""
from cipher_description import CipherDescription

r = []

def apply_h(cipher, x, y, wordsize):
    """
    H(x, y) = (x + y) + ((x & y) << 1)

    Applies H on the whole word and assigns it to x.
    """

    for bit in range(wordsize):
        cipher.apply_xor("s{}".format(x + bit), "s{}".format(y + bit), "txor{}".format(bit))
        cipher.apply_and("s{}".format(x + bit), "s{}".format(y + bit), "tand{}".format(bit))

    cipher.apply_xor("s{}".format(x), "s{}".format(y), "s{}".format(x))
    for bit in range(1, wordsize):
        cipher.apply_xor("txor{}".format(bit), "tand{}".format(bit - 1), "s{}".format(x + bit))

def apply_g(cipher, a, b, c, d, wordsize):
    apply_h(cipher, a, b, wordsize)
    for bit in range(wordsize):
        cipher.apply_xor("s{}".format(a + bit),
                         "s{}".format(d + bit),
                         "t{}".format(bit))
    for bit in range(wordsize):
        cipher.apply_and("t{}".format(bit),
                         "t{}".format(bit),
                         "s{}".format(d + (bit - r[0]) % wordsize))
    apply_h(cipher, c, d, wordsize)
    for bit in range(wordsize):
        cipher.apply_xor("s{}".format(b + bit),
                         "s{}".format(c + bit),
                         "t{}".format(bit))
    for bit in range(wordsize):
        cipher.apply_and("t{}".format(bit),
                         "t{}".format(bit),
                         "s{}".format(b + (bit - r[1]) % wordsize))
    apply_h(cipher, a, b, wordsize)
    for bit in range(wordsize):
        cipher.apply_xor("s{}".format(a + bit),
                         "s{}".format(d + bit),
                         "t{}".format(bit))
    for bit in range(wordsize):
        cipher.apply_and("t{}".format(bit),
                         "t{}".format(bit),
                         "s{}".format(d + (bit - r[2]) % wordsize))
    apply_h(cipher, c, d, wordsize)
    for bit in range(wordsize):
        cipher.apply_xor("s{}".format(b + bit),
                         "s{}".format(c + bit),
                         "t{}".format(bit))
    for bit in range(wordsize):
        cipher.apply_and("t{}".format(bit),
                         "t{}".format(bit),
                         "s{}".format(b + (bit - r[3]) % wordsize))


def generate_norx_version(wordsize, rounds):
    global r
    norx = CipherDescription(16 * wordsize)
    s = [i*wordsize for i in range(16)]

    if wordsize == 32:
        r = [8, 11, 16, 31]
    elif wordsize == 64:
        r = [8, 19, 40, 63]

    # Column round
    apply_g(norx, s[0], s[4], s[8], s[12], wordsize)
    apply_g(norx, s[1], s[5], s[9], s[13], wordsize)
    apply_g(norx, s[2], s[6], s[10], s[14], wordsize)
    apply_g(norx, s[3], s[7], s[11], s[15], wordsize)

    # Diagonal round
    apply_g(norx, s[0], s[5], s[10], s[15], wordsize)
    apply_g(norx, s[1], s[6], s[11], s[12], wordsize)
    apply_g(norx, s[2], s[7], s[8], s[13], wordsize)
    apply_g(norx, s[3], s[4], s[9], s[14], wordsize)

    return norx

norx32 = generate_norx_version(32, 4)
norx64 = generate_norx_version(64, 4)
