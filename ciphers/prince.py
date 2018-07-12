from cipher_description import CipherDescription

# State
# 0 4  8 12
# 1 5  9 13
# 2 6 10 14
# 3 7 11 15


sbox = [0xB, 0xF, 3, 2, 0xA, 0xC, 9, 1, 6, 7, 8, 0, 0xE, 5, 0xD, 4]
invsbox = [11, 7, 3, 2, 15, 13, 8, 9, 10, 6, 4, 0, 5, 14, 12, 1]

shuffle = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
shufflei = range(16)
for i in range(16):
    shufflei[shuffle[i]] = i

m = [
    [[0,0,0,0],
     [0,1,0,0],
     [0,0,1,0],
     [0,0,0,1]],
    [[1,0,0,0],
     [0,0,0,0],
     [0,0,1,0],
     [0,0,0,1]],
    [[1,0,0,0],
     [0,1,0,0],
     [0,0,0,0],
     [0,0,0,1]],
    [[1,0,0,0],
     [0,1,0,0],
     [0,0,1,0],
     [0,0,0,0]]
     ]

def generate_Prince_version(forward,backward):
    prince = CipherDescription(64)
    wordsize = 4

    prince.add_sbox('S-box', sbox)
    prince.add_sbox('S-boxi', invsbox)

    M = []
    M.append([])
    for i in range(4):
        for j in range(4):
            M[0].append([])
            for c in range(16):
                M[0][i*4+j].append(m[(c/4+i)%4][j][c%4])

    M.append([])
    for i in range(4):
        for j in range(4):
            M[1].append([])
            for c in range(16):
                M[1][i*4+j].append(m[(c/4+i+1)%4][j][c%4])




    def S():
        for i in range(16):
            bits = []
            for j in range(wordsize):
                bits.append("s{}".format(wordsize*i + wordsize - 1 - j))
            prince.apply_sbox('S-box', bits, bits)

    def Si():
        for i in range(16):
            bits = []
            for j in range(wordsize):
                bits.append("s{}".format(wordsize*i + wordsize - 1 - j))
            prince.apply_sbox('S-boxi', bits, bits)

    def Mhat():
        #Create temp variables
        for i in range(64):
            prince.apply_mov("s{}".format(i),"t{}".format(i))

        #Apply the M hat matrix
        for c in range(4):
            if c%4 == 0:
                t = 0
            else:
                t = 1
            for i in range(16):
                k = M[t][i].index(1)
                prince.apply_mov("t{}".format(16*c+k),"s{}".format(16*c+i))
                for j in range(k+1,16):
                    if M[t][i][j]==1:
                        prince.apply_xor("t{}".format(16*c+j),"s{}".format(16*c+i),"s{}".format(16*c+i))


    def R():
        S()
        Mhat()
        prince.shufflewords(shuffle,4,1)



    def Ri():
        prince.shufflewords(shufflei,4,1)
        Mhat()
        Si()


    #Forward rounds
    for i in range(forward):
        R()

    #Middle
    S()
    Mhat()
    Si()

    #Inverse rounds
    for i in range(backward):
        Ri()

    return prince
