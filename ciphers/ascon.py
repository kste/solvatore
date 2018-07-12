"""
Implementation of the ASCON permutation.

http://ascon.iaik.tugraz.at/
"""
from cipher_description import CipherDescription

def apply_sigma(cipher, bit, rot_a, rot_b):
    '''
    Sigma Function used in ASCON
    '''
    cipher.apply_xor("s{}".format((bit - rot_a) % 64),
                     "s{}".format((bit - rot_b) % 64),
                     "tmp")
    cipher.apply_xor("s{}".format(bit), "tmp", "s{}".format(bit))


ascon_sbox = [4,11,31,20,26,21,9,2,27,5,8,18,29,3,6,28,
              30,19,7,14,0,13,17,24,16,12,1,25,22,10,15,23]

ascon = CipherDescription(320)
ascon.add_sbox('S-box', ascon_sbox)

# Substitution Layer
for i in range(64):
    bits = ["s{}".format(i + 0),
            "s{}".format(i + 64),
            "s{}".format(i + 128),
            "s{}".format(i + 192),
            "s{}".format(i + 256)]
    ascon.apply_sbox('S-box', bits, bits)

# Linear Layer
for i in range(64):
    apply_sigma(ascon, i,       19, 28)
    apply_sigma(ascon, i + 64,  61, 39)
    apply_sigma(ascon, i + 128,  1,  6)
    apply_sigma(ascon, i + 192, 10, 17)
    apply_sigma(ascon, i + 256,  7, 41)
