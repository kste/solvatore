from cipher_description import CipherDescription

def generate_test_version(wordsize):
    # State
    # 0 4  8 12
    # 1 5  9 13
    # 2 6 10 14
    # 3 7 11 15
    test = CipherDescription(16*wordsize)
    

    midori_sbox = [0xC, 0xA, 0xD, 0x3, 0xE, 0xB, 0xF, 0x7,
                   0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6]
                       
    shuffle = [0,10,5,15, 14,4,11,1, 9,3,12,6, 7,13,2,8]
    MC = [[0, 1, 1, 1],
          [1, 0, 1, 1],
          [1, 1, 0, 1],
          [1, 1, 1, 0]]
    Rp = 0
    test.add_sbox('S-box', midori_sbox)
    for i in range(16):
        bits = []
        for j in range(wordsize):
            bits.append("s{}".format(wordsize*i + wordsize - 1 - j))
        test.apply_sbox('S-box', bits, bits)
    
    
    test.shufflewords(shuffle,wordsize)
    
    
    # MixColumn
    test.apply_MC(wordsize, MC, Rp, 4, 4)
  
    return test


    
test = generate_test_version(4)
