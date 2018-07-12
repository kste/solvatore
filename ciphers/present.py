from cipher_description import CipherDescription

present_sbox = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
                0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]
present_permutations = [\
  ['s1', 's16', 's4'],
  ['s2', 's32', 's8'],
  ['s3', 's48', 's12'],
  ['s5', 's17', 's20'],
  ['s6', 's33', 's24'],
  ['s7', 's49', 's28'],
  ['s9', 's18', 's36'],
  ['s10', 's34', 's40'],
  ['s11', 's50', 's44'],
  ['s13', 's19', 's52'],
  ['s14', 's35', 's56'],
  ['s15', 's51', 's60'],
  ['s22', 's37', 's25'],
  ['s23', 's53', 's29'],
  ['s26', 's38', 's41'],
  ['s27', 's54', 's45'],
  ['s30', 's39', 's57'],
  ['s31', 's55', 's61'],
  ['s43', 's58', 's46'],
  ['s47', 's59', 's62']]

present = CipherDescription(64)
present.add_sbox('S-box', present_sbox)
for i in range(16):
    bits = ["s{}".format(4*i + 0),
            "s{}".format(4*i + 1),
            "s{}".format(4*i + 2),
            "s{}".format(4*i + 3)]
    present.apply_sbox('S-box', bits, bits)
for p in present_permutations:
    present.apply_permutation(p)
