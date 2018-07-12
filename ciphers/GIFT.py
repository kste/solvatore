from cipher_description import CipherDescription

def generate_GIFT_version(size): 
    GIFT = CipherDescription(size)
    s = ['s{}'.format(i) for i in range(size)]
    
    #Sbox layer
    sbox = [1, 0xa, 4, 0xc, 6, 0xf, 3, 9, 2, 0xd, 0xb, 7, 5, 0, 8, 0xe]
    GIFT.add_sbox('S_box',sbox)
    for i in range(size/4): 
        bits = s[i*4:(i+1)*4]
        bits.reverse()
        GIFT.apply_sbox('S_box',bits,bits)
    
    #Bit permutation
    if size == 64:
        P = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3,
             4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7,
             8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11,
             12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]
    else:
        P = [0, 33, 66, 99, 96, 1, 34, 67, 64, 97, 2, 35, 32, 65, 98, 3,
             4, 37, 70, 103, 100, 5, 38, 71, 68, 101, 6, 39, 36, 69, 102, 7,
             8, 41, 74, 107, 104, 9, 42, 75, 72, 105, 10, 43, 40, 73, 106, 11,
             12, 45, 78, 111, 108, 13, 46, 79, 76, 109, 14, 47, 44, 77, 110, 15,
             16, 49, 82, 115, 112, 17, 50, 83, 80, 113, 18, 51, 48, 81, 114, 19,
             20, 53, 86, 119, 116, 21, 54, 87, 84, 117, 22, 55, 52, 85, 118, 23,
             24, 57, 90, 123, 120, 25, 58, 91, 88, 121, 26, 59, 56, 89, 122, 27,
             28, 61, 94, 127, 124, 29, 62, 95, 92, 125, 30, 63, 60, 93, 126, 31]
    GIFT.shufflewords(P,1,1)
            
    return GIFT
    
    
    
GIFT64 = generate_GIFT_version(64)
GIFT128 = generate_GIFT_version(128)
