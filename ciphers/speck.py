from cipher_description import CipherDescription

def generate_speck_version(n,a,b):
    speck = CipherDescription(2*n)
    s = ['s{}'.format(i) for i in range(2*n)]
  
    '''
    if n == 16:
        a = 7
        b = 2
    else:
        a = 8
        b = 3
    '''
    x = s[n:]
    y = s[:n]
    
    
    if n%a==0:
        for j in range(a):
            shift = ['s{}'.format(n+j+(i*(n-a))%n) for i in range(n/a)]
            speck.apply_permutation(shift)
    else:
        shift = ['s{}'.format(n+(i*(n-a))%n) for i in range(n)]
        speck.apply_permutation(shift)
    
        
        
    speck.add_mod(x,y,x,n,0)
    if n%b==0:
        for j in range(b):
            shift = ['s{}'.format(j+i*b) for i in range(n/b)]
            speck.apply_permutation(shift)
    else:
        shift = ['s{}'.format((i*b)%n) for i in range(n)]
        speck.apply_permutation(shift)
    
    
    for i in range(n):
        speck.apply_xor(x[i],y[i],y[i])
    return speck
