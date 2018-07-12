from cipher_description import CipherDescription

size = 64
LBlock = CipherDescription(size)
s = ['s{}'.format(i) for i in range(size)]
t = ['t{}'.format(i) for i in range(size/2)]

s0 = [14, 9, 15, 0, 13, 4, 10, 11, 1, 2, 8, 3, 7, 6, 12, 5]
s1 = [4, 11, 14, 9, 15, 13, 0, 10, 7, 12, 5, 6, 2, 8, 1, 3]
s2 = [1, 14, 7, 12, 15, 13, 0, 6, 11, 5, 9, 3, 2, 4, 8, 10]
s3 = [7, 6, 8, 11, 0, 15, 3, 14, 9, 10, 12, 13, 5, 2, 4, 1]
s4 = [14, 5, 15, 0, 7, 2, 12, 13, 1, 8, 4, 9, 11, 10, 6, 3]
s5 = [2, 13, 11, 12, 15, 14, 0, 9, 7, 10, 6, 3, 1, 8, 4, 5]
s6 = [11, 9, 4, 14, 0, 15, 10, 13, 6, 12, 5, 7, 3, 8, 1, 2]
s7 = [13, 10, 15, 0, 14, 4, 9, 11, 2, 1, 8, 3, 7, 5, 12, 6]
LBlock.add_sbox('S0',s0)
LBlock.add_sbox('S1',s1)
LBlock.add_sbox('S2',s2)
LBlock.add_sbox('S3',s3)
LBlock.add_sbox('S4',s4)
LBlock.add_sbox('S5',s5)
LBlock.add_sbox('S6',s6)
LBlock.add_sbox('S7',s7)

shuffle1 = [1,0] 
shuffle2 = [1,2,3,0]
shuffle3 = [4,12,0,8, 20,28,16,24]  

LBlock.shufflewords(shuffle2,8,0)
for i in range(size/2):
    LBlock.apply_mov(s[i+32],t[i])
for i in range(8):
    bits = t[4*i:4*(i+1)]
    bits.reverse()
    LBlock.apply_sbox('S{}'.format(i), bits,bits)

for i in range(size/2):
    LBlock.apply_xor(t[shuffle3[i/4]+i%4],s[i],s[i])
    
LBlock.shufflewords(shuffle1,32,0)




