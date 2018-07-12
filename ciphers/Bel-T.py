from cipher_description import CipherDescription


#add s-box

BelT = CipherDescription(128)
n = 32

s = ['s{}'.format(i) for i in range(128)]


d = s[:n]
c = s[n:2*n]
b = s[2*n:3*n]
a = s[3*n:]


swap = [2,0,3,1]
BelT.shufflewords(swap,n,1)
