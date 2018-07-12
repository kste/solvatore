from cipher_description import CipherDescription

size = 64
RoadRunnerR = CipherDescription(size)
s = ['s{}'.format(i) for i in range(size)]
t = ['t{}'.format(i) for i in range(size)]
sbox = [0, 8, 6, 0xD, 5, 0xF, 7, 0xC, 4, 0xE, 2, 3, 9, 1, 0xB, 0xA]
RoadRunnerR.add_sbox('Sbox', sbox)

for i in range(size/2):
    RoadRunnerR.apply_mov(s[i], t[i])

def S(): 
    for i in range(8):
        bits = ['t{}'.format(i+8*j) for j in range(4)]
        bits.reverse()
        RoadRunnerR.apply_sbox('Sbox',bits,bits)

def L():
    for i in range(size/2):
        RoadRunnerR.apply_mov(t[i], t[size/2+i])
    for i in range(size/2):
        RoadRunnerR.apply_xor(t[i],t[size/2+8*(i/8)+(i+1)%8],t[i])
        RoadRunnerR.apply_xor(t[i],t[size/2+8*(i/8)+(i+2)%8],t[i])

S()
L()
S()
L()
S()
L()
S()

for i in range(size/2):
    RoadRunnerR.apply_xor(s[size/2+i], t[i], s[size/2+i])
swap = [1,0] 
RoadRunnerR.shufflewords(swap,size/2,1)
