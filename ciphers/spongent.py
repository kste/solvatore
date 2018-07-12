from cipher_description import CipherDescription

def generate_spongent_version(b):
    spongent = CipherDescription(b)
    sbox = [0xE, 0xD, 0xB, 0, 2, 1, 4, 0xF, 7, 0xA, 8, 5, 9, 0xC, 3, 6]
    spongent.add_sbox('S-box', sbox)
    for i in range(b/4):
        bits = []
        for j in range(4):
            bits.append("s{}".format(4*i + 3-j))
        spongent.apply_sbox('S-box', bits, bits)
        
    shuffle = [(j*b/4)%(b-1) for j in range(b-1)]
    shuffle.append(b-1)
    spongent.shufflewords(shuffle,1,1)
    return spongent

P88 = generate_spongent_version(88)
