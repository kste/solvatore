from cipher_description import CipherDescription

size = 512
salsa = CipherDescription(size)
n = 32

s = ['s{}'.format(i) for i in range(size)]
t = ['t{}'.format(i) for i in range(size)]

v = []
for i in range(16):
    v.append(s[i*n:(i+1)*n])

def R(a,b,c,k):
    salsa.add_mod(a,c,t[0:n],n,size)
    for i in range(n):
        salsa.apply_xor(b[i],t[(i-k)%n],b[i])
    
for i in range(4):
    R(v[0+i],v[4+i],v[12+i],7)
    R(v[0+i],v[8+i],v[4+i],9)
    R(v[8+i],v[12+i],v[4+i],13)
    R(v[8+i],v[0+i],v[12+i],18)

shuffle = [0,   4,  8,  12,
           1,   5,  9,  13,
           2,   6,  10, 14,
           3,   7,  11, 15]
salsa.shufflewords(shuffle,n,1)
