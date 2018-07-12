from cipher_description import CipherDescription

def sparx_version(size,r,Ae):
    
    sparx = CipherDescription(size)
    s = ['s{}'.format(i) for i in range(size)]
    if size == 64:
        rs = 3
    elif size == 128:
        rs = 4
        
    def A(h):
        n = 16
        a = 7
        b = 2
        x = s[h+n:h+2*n]
        y = s[h:h+n]
        
        shift = ['s{}'.format(h+n+(i*(n-a))%n) for i in range(n)]
        sparx.apply_permutation(shift)
        
        sparx.add_mod(x,y,x,n,size+2*h)
    
        for j in range(b):
            shift = ['s{}'.format(h+j+i*b) for i in range(n/b)]
            sparx.apply_permutation(shift)
    
        for i in range(n):
            sparx.apply_xor(x[i],y[i],y[i])
    
    
    for rnd in range(r):
        for i in range(rs):
            for j in range(size/32):
                A(j*32)
    
    
            
        t = ['t{}'.format(i) for i in range(size)]
    
        for i in range(size/2):
            sparx.apply_mov(s[i+size/2],t[i])
    
        for i in range(size/4):
            sparx.apply_xor(t[i],t[i+16],t[i+size/2])
        
        if size == 128:
            for i in range(16):
                sparx.apply_xor(t[i+size/2],t[i+16+size/2],t[i+size/2])
    
    
        if size == 64:
            sw = [0,1]
        elif size == 128:
            sw = [0,3,2,1]
        for j in range(size/32):
            for i in range(16):
                sparx.apply_xor(t[size/2+(i+8)%16],t[i+16*sw[j]],t[i+16*sw[j]])
     
        
        for i in range(size/2):
            sparx.apply_xor(s[i],t[i],s[i])
        
    
        swap = [1,0]
   
        sparx.shufflewords(swap,size/2,0)
    
    for i in range(Ae):
        for j in range(size/32):
            A(j*32)
    return sparx
