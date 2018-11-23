# H. Hadipour
# 10 Nov 2018
from itertools import combinations
from solvatore import Solvatore
from cipher_description import CipherDescription

from ciphers import mibs

cipher = mibs.mibs
rounds = 6

solver = Solvatore()
solver.load_cipher(cipher)
solver.set_rounds(rounds)

# Look over all combination for one non active bit
block_size = 64
for bits in combinations(range(block_size), 1):
    constant_bits = bits
    active_bits = {i for i in range(block_size) if i not in constant_bits}

    # Find all balanced bits
    balanced_bits = []
    for i in range(cipher.state_size):
        if solver.is_bit_balanced(i, rounds, active_bits):            
            balanced_bits.append(i)

    if len(balanced_bits) > 0:
        print("Found distinguisher!")
        print("Constant Bits: ", len(constant_bits),constant_bits)
        print("Balanced Bits: ", len(balanced_bits),balanced_bits)
    elif len(balanced_bits) == 0:
	print(bits)
        print("Distinguisher not found!")
