from cipher_description import CipherDescription

rectangle_sbox = [0x6, 0x5, 0xC, 0xA, 0x1, 0xE, 0x7, 0x9,
                0xB, 0x0, 0x3, 0xD, 0x8, 0xF, 0x4, 0x2]
rectangle_permutations = [\
  ['s16', 's17', 's18','s19','s20','s21','s22','s23','s24','s25','s26','s27','s28','s29','s30','s31'],
  ['s32', 's44', 's40','s36'],
  ['s33', 's45', 's41','s37'],
  ['s34', 's46', 's42','s38'],
  ['s35', 's47', 's43','s39'],
  ['s48', 's61', 's58','s55','s52','s49','s62','s59','s56','s53','s50','s63','s60','s57','s54','s51'],
]

rectangle = CipherDescription(64)
rectangle.add_sbox('S-box', rectangle_sbox)
for i in range(16):
    bits = ["s{}".format(i + 0),
            "s{}".format(i + 16),
            "s{}".format(i + 32),
            "s{}".format(i + 48)]
    rectangle.apply_sbox('S-box', bits, bits)
for p in rectangle_permutations:
   rectangle.apply_permutation(p)
