from cipher_description import CipherDescription

def generate_QARMA_version(wordsize,sigma,f,b):
    QARMA = CipherDescription(16*wordsize)

    # State
    # 0 4  8 12
    # 1 5  9 13
    # 2 6 10 14
    # 3 7 11 15

    s0 = [ 0, 14, 2, 10, 9, 15, 8, 11, 6, 4, 3, 7, 13, 12, 1, 5 ]
    s1 = [ 10, 13, 14, 6, 15, 7, 3, 5, 9, 8, 0, 12, 11, 1, 2, 4 ]
    s2 = [ 11, 6, 8, 15, 12, 0, 9, 14, 3, 7, 4, 5, 13, 2, 1, 10 ]
    s2i = [ 5, 14, 13, 8, 10, 11, 1, 9, 2, 6, 15, 0, 4, 12, 7, 3 ]

    IP = 1

    if sigma == 0:
        QARMA.add_sbox("S-box", s0)
        QARMA.add_sbox("S-boxinverse", s0)
    elif sigma == 1:
        QARMA.add_sbox("S-box", s1)
        QARMA.add_sbox("S-boxinverse", s1)
    else:
        QARMA.add_sbox("S-box", s2)
        QARMA.add_sbox("S-boxinverse", s2i)

    def S():
        if wordsize == 4:
            for i in range(16):
                bits = []
                for j in range(4):
                    bits.append("s{}".format(4*i + 3 - j))
                QARMA.apply_sbox('S-box', bits, bits)
        else:
            for i in range(32):
                bits = []
                for j in range(4):
                    bits.append("s{}".format(4*i + 3 - j))
                QARMA.apply_sbox('S-box', bits, bits)
                # Permute output bits

            for i in range(16):
                shuffle_bits_first_sbox = ["s{}".format(8*i + j) for j in [1, 2, 4]]
                shuffle_bits_secnd_sbox = ["s{}".format(8*i + j) for j in [3, 6, 5]]
                QARMA.apply_permutation(shuffle_bits_first_sbox)
                QARMA.apply_permutation(shuffle_bits_secnd_sbox)
            #     for j in range(8):
            #         QARMA.apply_mov("s{}".format(8*i+j),"t{}".format(j))
            #
            #     for j in range(4):
            #         QARMA.apply_mov("t{}".format(2*j),"s{}".format(8*i+j))
            #     for j in range(4):
            #         QARMA.apply_mov("t{}".format(2*j+1),"s{}".format(8*i+j+4))

    def Si():
        if wordsize == 4:
            for i in range(16):
                bits = []
                for j in range(4):
                    bits.append("s{}".format(4*i + 3 - j))
                QARMA.apply_sbox('S-boxinverse', bits, bits)
        else:
            for i in range(16):
                shuffle_bits_first_sbox = ["s{}".format(8*i + j) for j in [4, 2, 1]]
                shuffle_bits_secnd_sbox = ["s{}".format(8*i + j) for j in [5, 6, 3]]
                QARMA.apply_permutation(shuffle_bits_first_sbox)
                QARMA.apply_permutation(shuffle_bits_secnd_sbox)
            for i in range(32):
                bits = []
                for j in range(4):
                    bits.append("s{}".format(4*i + 3 - j))
                QARMA.apply_sbox('S-boxinverse', bits, bits)



    if wordsize == 4:
        MC = [[0,2,4,2],
              [2,0,2,4],
              [4,2,0,2],
              [2,4,2,0]]
    else:
        MC = [[0,2,16,32],
              [32,0,2,16],
              [16,32,0,2],
              [2,16,32,0]]

    shuffle = [0,10,5,15, 14,4,11,1, 9,3,12,6, 7,13,2,8]
    shufflei = [0,7,14,9, 5,2,11,12, 15,8,1,6, 10,13,4,3]

    def R():
        QARMA.shufflewords(shuffle,wordsize,1)
        QARMA.apply_MC(wordsize,MC,IP,4,4)
        S()

    def Ri():
        Si()
        QARMA.apply_MC(wordsize,MC,IP,4,4)
        QARMA.shufflewords(shufflei,wordsize,1)

    #Forward rounds
    S()
    for r in range(f):
        R()
    #Middle round
    QARMA.shufflewords(shuffle,wordsize,1)
    QARMA.apply_MC(wordsize,MC,IP,4,4)
    QARMA.shufflewords(shufflei,wordsize,1)
    #Backwards rounds
    for r in range(b):
        Ri()
    Si()

    return QARMA

f = 3
b = 3
QARMA64S0 = generate_QARMA_version(4,0,f,b)
QARMA64S1 = generate_QARMA_version(4,1,f,b)
QARMA64S2 = generate_QARMA_version(4,2,f,b)


QARMA128S0 = generate_QARMA_version(8,0,f,b)
QARMA128S1 = generate_QARMA_version(8,1,f,b)
QARMA128S2 = generate_QARMA_version(8,2,f,b)
