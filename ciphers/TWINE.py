from cipher_description import CipherDescription

size = 64
TWINE = CipherDescription(size)
s = ['s{}'.format(i) for i in range(size)]
t = ['t{}'.format(i) for i in range(size)]

Sbox = [0xC, 0, 0xF, 0xA, 2, 0xB, 9, 5, 8, 3, 0xD, 7, 1, 0xE, 6, 4]
p = [5, 0, 1, 4, 7, 12, 3, 8, 13, 6, 9, 2, 15, 10, 11, 14]

TWINE.add_sbox('sbox',Sbox)

for i in range(8):
    for j in range(4):
        TWINE.apply_mov(s[8*i+j],t[4*i+j])
    bits = t[4*i:4*(i+1)]
    bits.reverse()
    TWINE.apply_sbox('sbox',bits,bits)

    for j in range(4):
        TWINE.apply_xor(t[4*i+j],s[8*i+4+j],s[8*i+4+j])

TWINE.shufflewords(p,4,0)
