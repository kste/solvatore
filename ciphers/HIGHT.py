from cipher_description import CipherDescription
#Bit numbering
#s63..s0
HIGHT = CipherDescription(64)
n = 8

s = ['s{}'.format(i) for i in range(64)]
t = ['t{}'.format(i) for i in range(64)]

for i in range(n):
    HIGHT.apply_xor(s[(i+3)%n],s[(i+4)%n],'t{}'.format(i))
    HIGHT.apply_xor(s[(i+6)%n],'t{}'.format(i),'t{}'.format(i))
    
    HIGHT.apply_xor(s[16+(i+1)%n],s[16+(i+2)%n],'t{}'.format(16+i))
    HIGHT.apply_xor(s[16+(i+7)%n],'t{}'.format(16+i),'t{}'.format(16+i))
    
    HIGHT.apply_xor(s[32+(i+3)%n],s[32+(i+4)%n],'t{}'.format(32+i))
    HIGHT.apply_xor(s[32+(i+6)%n],'t{}'.format(32+i),'t{}'.format(32+i))
    
    HIGHT.apply_xor(s[48+(i+1)%n],s[48+(i+2)%n],'t{}'.format(48+i))
    HIGHT.apply_xor(s[48+(i+7)%n],'t{}'.format(48+i),'t{}'.format(48+i))

HIGHT.add_mod(t[:8],s[8:16],s[8:16],n,64)
HIGHT.add_mod(t[32:40],s[40:48],s[40:48],n,128)

HIGHT.addconstant_mod(t[16:24],t[16:24],n,192)
HIGHT.addconstant_mod(t[48:56],t[48:56],n,256)

for i in range(n):
    HIGHT.apply_xor(t[16+i],s[24+i],s[24+i])
    HIGHT.apply_xor(t[48+i],s[56+i],s[56+i])
    
shuffle = [7] + range(7)
HIGHT.shufflewords(shuffle,n,1)
