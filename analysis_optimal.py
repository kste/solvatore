from solvatore import Solvatore
from cipher_description import CipherDescription
from itertools import combinations, groupby
from ciphers import RoadRunnerR, speck, LEA, spongent, HIGHT, GIFT, skipjack
#import ciphers

# # # Cipher Definition
# cipher = speck.generate_speck_version(64,8,3)
# rounds = 6
# solver = Solvatore()
# solver.load_cipher(cipher)
# solver.set_rounds(rounds)
# statesize = 128

# # LEA
# cipher = LEA.LEA
# rounds = 8
# solver = Solvatore()
# solver.load_cipher(cipher)
# solver.set_rounds(rounds)
# statesize = 128


# # Simon
# cipher = simon.simon32_64
# rounds = 13
# solver = Solvatore()
# solver.load_cipher(cipher)
# solver.set_rounds(rounds)
# statesize = 32

# # Roadrunner
# cipher = RoadRunnerR.RoadRunnerR
# rounds = 5
# solver = Solvatore()
# solver.load_cipher(cipher)
# solver.set_rounds(rounds)
# statesize = 64

# Hight
cipher = HIGHT.HIGHT
rounds = 18
solver = Solvatore()
solver.load_cipher(cipher)
solver.set_rounds(rounds)
statesize = 64

# # # GIFT
# cipher = GIFT.GIFT64
# rounds = 9
# solver = Solvatore()
# solver.load_cipher(cipher)
# solver.set_rounds(rounds)
# statesize = 64

# cipher = spongent.generate_spongent_version(88)
# rounds = 9
# solver = Solvatore()
# solver.load_cipher(cipher)
# solver.set_rounds(rounds)
# statesize = 88

# cipher = skipjack.skipjack
# rounds = 1
# solver = Solvatore()
# solver.load_cipher(cipher)
# solver.set_rounds(rounds)
# statesize = 64



def getSetOfBalancedBits(constant_bits, bits_to_test):
    active_bits = [i for i in range(statesize) if i not in constant_bits]
    # Compute Set of balanced bits
    B = []
    for i in bits_to_test:
        if solver.is_bit_balanced(i, rounds, active_bits):
            B.append(i)
    return B

# Find best distinguisher with single active bit
good_indices = []
for b in range(statesize):
    #print(b)
    constant_bits = [b]
    B = getSetOfBalancedBits(constant_bits, range(statesize))
    if len(B) > 0:
        good_indices.append(constant_bits + [B])

if len(good_indices) == 0:
    print("No distinguisher exists.")
    exit(1)

# Check all combination of good indices and reduce
while True:    
    # Only get the combinations which share balanced bits between
    # the two sets.
    combination_indices = []
    balanced_sets = []
    for comb in combinations(good_indices, 2):
        intersection = set(comb[0][-1]).intersection(set(comb[1][-1]))
        if len(intersection) > 0:
            new_index_set = set(comb[0][:-1] + comb[1][:-1])
            new_balanced_set = set(comb[0][-1:][0] + comb[1][-1:][0])
            if new_index_set not in combination_indices:
                combination_indices.append(new_index_set)
                balanced_sets.append(new_balanced_set)

    # Find Largest balanced set
    max_set = [[]]
    for G in good_indices:
        if len(G[-1]) > len(max_set[-1]):
            max_set = G

    # Filter duplicates
    print("Constant bits:", len(good_indices), len(combination_indices), len(good_indices[0][:-1]), max_set)
    good_indices = []
    for i, new_index in enumerate(combination_indices):
        constant_bits = list(set([item for item in new_index]))
        B = getSetOfBalancedBits(constant_bits, balanced_sets[i])
        solution = constant_bits + [B]
        if len(B) > 0 and solution not in good_indices:
            good_indices.append(solution)
    if len(good_indices) == 0:
        print("Finished Search.")
        break
