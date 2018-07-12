from cipher_description import CipherDescription

# Cipher Definition
def generate_simeck_version(n, rounds):
    simeck = CipherDescription(2*n)
    for i in range(n):
        input_1 = "s{}".format((i-5)%n+n)
        input_2 = "s{}".format((i-0)%n+n)
        product =  "t{}".format(2*i)
        simeck.apply_and(input_1, input_2, product)
        input_3 = "s{}".format((i-1)%n+n)
        xor = "t{}".format(2*i+1)
        simeck.apply_xor(product, input_3, xor)
        right_side = "s{}".format(i)
        simeck.apply_xor(xor, right_side, right_side)
    for i in range(n):
        right_side = "s{}".format(i)
        left_side = "s{}".format(i+n)
        simeck.apply_permutation( (right_side, left_side) )
    simeck.set_rounds(rounds)
    return simeck

simeck32_64 = generate_simeck_version(16, 32)
simeck48_96 = generate_simeck_version(24, 36)
simeck64_128 = generate_simeck_version(32, 44)
