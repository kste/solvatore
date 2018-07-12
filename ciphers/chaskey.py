from cipher_description import CipherDescription

size = 128
n = 32
chaskey = CipherDescription(size)

s = ['s{}'.format(i) for i in range(size)]
t = ['t{}'.format(i) for i in range(size)]

v0 = s[0:32]
v1 = s[32:64]
v2 = s[64:96]
v3 = s[96:128]

chaskey.add_mod(v0,v1,v0,n,0)
chaskey.add_mod(v2,v3,v2,n,0)

shuffle = [i for i in range(size)]
for i in range(n):
    shuffle[n+i] = n+(i+5)%n
    shuffle[3*n+i] = 3*n+(i+8)%n
chaskey.shufflewords(shuffle,1,0)

for i in range(n):
    chaskey.apply_xor(v0[i],v1[i],v1[i])
    chaskey.apply_xor(v2[i],v3[i],v3[i])

shuffle = [i for i in range(size)]
for i in range(n):
    shuffle[i] = (i+16)%n
chaskey.shufflewords(shuffle,1,0)

chaskey.add_mod(v2,v1,v2,n,0)
chaskey.add_mod(v0,v3,v0,n,0)

shuffle = [i for i in range(size)]
for i in range(n):
    shuffle[n+i] = n+(i+7)%n
    shuffle[3*n+i] = 3*n+(i+13)%n
chaskey.shufflewords(shuffle,1,0)

for i in range(n):
    chaskey.apply_xor(v2[i],v1[i],v1[i])
    chaskey.apply_xor(v0[i],v3[i],v3[i])

shuffle = [i for i in range(size)]
for i in range(n):
    shuffle[2*n+i] = 2*n + (i+16)%n
chaskey.shufflewords(shuffle,1,0)
