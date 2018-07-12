from cipher_description import CipherDescription

#Bit numbering
#s128..s0

LEA = CipherDescription(128)
wordsize = 32
s = ['s{}'.format(i) for i in range(128)]

for i in range(3):
    x = s[wordsize*(2-i):wordsize*(3-i)]
    y = s[wordsize*(3-i):wordsize*(4-i)]

    LEA.add_mod(x,y,y,wordsize,128)

shuffle = [1,2,3,0]
LEA.shufflewords(shuffle,wordsize,1)
for i in range(wordsize):
    LEA.apply_mov(s[i], 't{}'.format(i))
    LEA.apply_mov(s[i+32], 't{}'.format(i+32))
    LEA.apply_mov(s[i+64], 't{}'.format(i+64))
    

for i in range(wordsize):
    LEA.apply_mov('t{}'.format(i),s[(i+9)%wordsize])
    LEA.apply_mov('t{}'.format(32+i),s[32+(i-5)%wordsize])
    LEA.apply_mov('t{}'.format(64+i),s[64+(i-3)%wordsize])
