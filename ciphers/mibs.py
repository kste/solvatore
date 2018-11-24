# H. Hadipour 
# 10 Nov 2018
from cipher_description import CipherDescription

size = 64
wordsize = 4
mibs = CipherDescription(size)
s = ['s{}'.format(i) for i in range(size)]
t = ['t{}'.format(i) for i in range(size // 2)]
y = [['t{}'.format(i + wordsize * j) for i in range(wordsize)] for j in range(size // wordsize)]

s1 = [4, 15, 3, 8, 13, 10, 12, 0, 11, 5, 7, 14, 2, 6, 1, 9]
mibs.add_sbox('S1',s1)
shuffle1 = [1, 0]
shuffle2 = [1, 7, 0, 2, 5, 6, 3, 4]
shuffle2_inv = [2, 0, 3, 6, 7, 4, 5, 1]

# Copy of the left side pass through the round function
for i in range(32):
    mibs.apply_mov(s[i], t[i])

# Applying sboxes
for i in range(8):
    bits = t[4 * i:4 * (i + 1)]
    bits.reverse() 
    mibs.apply_sbox('S1', bits, bits)

# Applying mixing layer 
for bit in range(wordsize):
    y1 = "t{}".format(bit)
    y2 = "t{}".format(bit + wordsize)
    y3 = "t{}".format(bit + 2*wordsize)
    y4 = "t{}".format(bit + 3*wordsize)
    y5 = "t{}".format(bit + 4*wordsize)
    y6 = "t{}".format(bit + 5*wordsize)
    y7 = "t{}".format(bit + 6*wordsize)
    y8 = "t{}".format(bit + 7*wordsize)

    mibs.apply_xor(y4, y8, y8)
    mibs.apply_xor(y3, y7, y7)
    mibs.apply_xor(y2, y6, y6)
    mibs.apply_xor(y1, y5, y5)
    mibs.apply_xor(y8, y2, y2)
    mibs.apply_xor(y7, y1, y1)
    mibs.apply_xor(y6, y4, y4)
    mibs.apply_xor(y5, y3, y3)
    mibs.apply_xor(y4, y5, y5)
    mibs.apply_xor(y3, y8, y8)
    mibs.apply_xor(y2, y7, y7)
    mibs.apply_xor(y1, y6, y6)
    mibs.apply_xor(y8, y4, y4)
    mibs.apply_xor(y7, y3, y3)
    mibs.apply_xor(y6, y2, y2)
    mibs.apply_xor(y5, y1, y1)

# XOR of output of round functiond and right side of input
for nibble in range(8):
    for bit in range(4):        
        mibs.apply_xor(y[shuffle2_inv[nibble]][bit], s[4 * nibble + bit + 32], s[4 * nibble + bit + 32])

# Swap
mibs.shufflewords(shuffle1, 32, 0)
