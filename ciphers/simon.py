from cipher_description import CipherDescription

# Cipher Definition
def generate_simon_version(n, rounds, a=8, b=1, c=2):
    simon = CipherDescription(2*n)
    for i in range(n):
        input_1 = "s{}".format((i-a)%n+n)
        input_2 = "s{}".format((i-b)%n+n)
        product =  "t{}".format(2*i)
        simon.apply_and(input_1, input_2, product)
        input_3 = "s{}".format((i-c)%n+n)
        xor = "t{}".format(2*i+1)
        simon.apply_xor(product, input_3, xor)
        right_side = "s{}".format(i)
        simon.apply_xor(xor, right_side, right_side)
    for i in range(n):
        right_side = "s{}".format(i)
        left_side = "s{}".format(i+n)
        simon.apply_permutation( (right_side, left_side) )
    simon.set_rounds(rounds)
    return simon

simon32_64 = generate_simon_version(16, 32)
simon48_72 = generate_simon_version(24, 36)
simon48_96 = generate_simon_version(24, 36)
simon64_96 = generate_simon_version(32, 42)
simon64_128 = generate_simon_version(32, 44)
simon96_96 = generate_simon_version(48, 52)
simon96_144 = generate_simon_version(48, 54)
simon128_128 = generate_simon_version(64, 68)
simon128_192 = generate_simon_version(64, 69)
simon128_256 = generate_simon_version(64, 72)
