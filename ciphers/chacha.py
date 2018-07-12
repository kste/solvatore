from cipher_description import CipherDescription


def generate_chacha(r):
    size = 512
    chacha = CipherDescription(size)
    n = 32

    s = ['s{}'.format(i) for i in range(size)]
    t = ['t{}'.format(i) for i in range(size)]

    v = []
    for i in range(16):
        v.append(s[i*n:(i+1)*n])

    for j in range(r):
        for i in range(4):
            a,b,c,d = v[0+i], v[4+(i+(j&1)*1)%4], v[8+(i+(j&1)*2)%4], v[12+(i+(j&1)*3)%4]
            
            chacha.add_mod(a,b,a,n,size)
            for l in range(n):
                chacha.apply_xor(d[l],a[l],t[l])
            for l in range(n):
                chacha.apply_mov(t[(l-16)%n],d[l])
            
            chacha.add_mod(c,d,c,n,size)
            for l in range(n):
                chacha.apply_xor(b[l],c[l],t[l])
            for l in range(n):
                chacha.apply_mov(t[(l-12)%n],b[l])
            
            chacha.add_mod(a,b,a,n,size)
            for l in range(n):
                chacha.apply_xor(d[l],a[l],t[l])
            for l in range(n):
                chacha.apply_mov(t[(l-8)%n],d[l])
            
            chacha.add_mod(c,d,c,n,size)
            for l in range(n):
                chacha.apply_xor(b[l],c[l],t[l])
            for l in range(n):
                chacha.apply_mov(t[(l-7)%n],b[l])
        
    return chacha
