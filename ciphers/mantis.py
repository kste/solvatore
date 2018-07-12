from cipher_description import CipherDescription

# State
# 0 4  8 12
# 1 5  9 13
# 2 6 10 14
# 3 7 11 15


midori_sbox = [0xC, 0xA, 0xD, 0x3, 0xE, 0xB, 0xF, 0x7,
               0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6]

shuffle = [0,10,5,15, 14,4,11,1, 9,3,12,6, 7,13,2,8]
shufflei = [0,7,14,9, 5,2,11,12, 15,8,1,6, 10,13,4,3]

MC = [[0, 1, 1, 1],
      [1, 0, 1, 1],
      [1, 1, 0, 1],
      [1, 1, 1, 0]]
Rp = 0


def generate_Mantis_version(forward, backward):
    mantis = CipherDescription(64)
    wordsize = 4
    mantis.add_sbox('S-box', midori_sbox)

    def S():
        for i in range(16):
            bits = []
            for j in range(wordsize):
                bits.append("s{}".format(wordsize*i + wordsize - 1 - j))
            mantis.apply_sbox('S-box', bits, bits)

    def R():
        S()
        mantis.shufflewords(shuffle,wordsize,1)
        mantis.apply_MC(wordsize, MC, Rp, 4, 4)

    def Ri():
        mantis.apply_MC(wordsize, MC, Rp, 4, 4)
        mantis.shufflewords(shufflei,wordsize,1)
        S()


    #Forward rounds
    for i in range(forward):
        R()
    #Middle
    S()
    mantis.apply_MC(wordsize, MC, Rp, 4, 4)
    S()
    #Inverse rounds
    for i in range(backward):
        Ri()

    return mantis
