from solvatore import Solvatore
from cipher_description import CipherDescription

from itertools import combinations

from ciphers import skinny

constant_sboxes = 1
wordsize = 4

cipher = skinny.skinny64
rounds = 10
solver = Solvatore()
solver.load_cipher(cipher)
solver.set_rounds(rounds)

# Skinny Paper Distinguisher
# integral_dist = [12, 13, 14, 15, 24, 25, 26, 27, 32, 33, 34, 35, 48, 49, 50, 51]
# nibbles = [2, 3, 9, 12]

found_distinguisher = False

print("Skinny Wordsize: {} Rounds: {}".format(wordsize, rounds))

#for constant_bit in range(16*wordsize):
#   constant_bits = [constant_bit]
for constant_sboxes in combinations(range(16), constant_sboxes):
    constant_bits = [24 + i for i in range(wordsize)]
    #for sbox in constant_sboxes:
    #    for i in range(wordsize):
    #        constant_bits.append(wordsize*sbox + i)

    active_bits = {i for i in range(16 * wordsize) if i not in constant_bits}

    balanced_bits = []

    for i in range(16 * wordsize):
        if solver.is_bit_balanced(i, rounds, active_bits):
            print("Balanced: {}".format(i))
            balanced_bits.append(i)
        else:
            print("Not Balanced: {}".format(i))

    if len(balanced_bits) > 0:
        found_distinguisher = True
        print("------------------------------")
        print("Found Distinguisher")
        print("Constant Bits: ", constant_bits)
        #print("Active Bits: ", list(active_bits))
        print("Balanced Bits: ", balanced_bits)
        break


if found_distinguisher == False:
    print("No Distinguisher found!")
