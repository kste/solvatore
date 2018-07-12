import sys
from math import log
from itertools import combinations

class CipherDescription:
    def __init__(self, state_size):
        '''
        Create an empty instance of a cipher of given state size
        '''
        self.state_size = state_size
        self.temporaries = set()
        self.rounds = 1
        self.transition = []
        self.sboxes = dict()
        self.description = ''

    def apply_permutation(self, permutation):
        '''
        Extend current round transition by a permutation

        A permutation must be given as a list of state variables.
        '''
        self.check_permutation(permutation)
        self.transition.append((permutation, 'PERM'))
        self.description += permutation[-1] + ' -> '
        self.description += ' -> '.join(var for var in permutation) + '\n'

    def add_sbox(self, sbox_name, sbox):
        '''
        Add an S-box definition to the available S-boxes

        The S-box must be given as a list of integers. It is then
        available under the supplied name.
        '''
        if not log(len(sbox), 2).is_integer():
            print("Invalid S-box size: needs to be power of two.")
            exit()
        self.sboxes[sbox_name] = sbox

    def apply_sbox(self, sbox_name, input_bits, output_bits):
        '''
        Extend current round transition by application of an S-box
        '''
        if sbox_name not in self.sboxes:
            raise KeyError('{} not in self.sboxes'.format(sbox_name))
        if len(self.sboxes[sbox_name]) != 2**len(input_bits):
            print('Size of S-box "{}" incompatible with number of bits'
                  '({})'.format(sbox_name, len(input_bits)))
            sys.exit(1)
        self.transition.append((sbox_name, input_bits, output_bits, 'SBOX'))
        self.description += ', '.join(input_bits)
        self.description += ' -> [' + sbox_name + '] -> '
        self.description += ', '.join(output_bits) + '\n'

    def apply_xor(self, source_1, source_2, target, description=True):
        '''
        Extend current round transition by application of an XOR
        '''
        self.check_source(source_1)
        self.check_source(source_2)
        self.check_target(target)
        self.transition.append((target, source_1, source_2, 'XOR'))
        if description:
            self.description += '{} = {} + {}\n'.format(target, source_1, source_2)

    def apply_and(self, source_1, source_2, target, description=True):
        '''
        Extend current round transition by application of an AND
        '''
        self.check_source(source_1)
        self.check_source(source_2)
        self.check_target(target)
        self.transition.append((target, source_1, source_2, 'AND'))
        if description:
            self.description += '{} = {} & {}\n'.format(target, source_1, source_2)

    def apply_mov(self, source, target, description=True):
        '''
        Extend current round transition by application of an MOV 
        '''
        self.check_source(source)
        self.check_target(target)
        self.transition.append((target, source, 'MOV'))
        if description:
            self.description += '{} = {}\n'.format(target, source)


    def set_rounds(self, rounds):
        '''
        Set the number of transitions used in the cipher
        '''
        self.rounds = rounds

    def print_description(self):
        '''
        Print the description of the round transition
        '''
        print(self.description[:-1])

    def check_source(self, source):
        '''
        Check that a given source variable is valid and available
        '''
        if source[0] == 's':
            number = int(source[1:])
            if number >= self.state_size:
                raise ValueError("There are only {} state bits."\
                                 .format(self.state_size))
        elif source[0] == 't':
            if source not in self.temporaries:
                raise ValueError("There is no temporary bit named '{}' "
                                 "at this point.".format(source))
        else:
            raise ValueError("Only 's' and 't' are allowed in variables.")

    def check_target(self, target):
        '''
        Check that a given target variable is valid and potentially add it
        '''
        if target[0] == 's':
            number = int(target[1:])
            if number >= self.state_size:
                raise ValueError("There are only {} state bits."\
                                 .format(self.state_size))
        elif target[0] == 't' or target[0] == 'b':
            self.temporaries.add(target)
        else:
            raise ValueError("Only 's' and 't' are allowed in variables.")

    def check_permutation(self, permutation):
        '''
        Check that permutation is correctly specified
        '''
        for var in permutation:
            if var[0] != 's':
                raise ValueError("Only 's' variables are allowed "
                                 "in permutations.")
            number = int(var[1:])
            if number >= self.state_size:
                raise ValueError("There are only {} state bits."\
                                 .format(self.state_size))

    def apply_MC(self,wordsize,MC,Rp,nc,nr):
        '''
        Apply MixColumns.
        Assumes state bits are numbered columnwise and that MC is stored row-wise
        '''
        #Get bits of the irreducible polynomial
        Rpb = list(format(Rp,'0{}b'.format(wordsize)))

        #Create a basis using the powers of 2
        basis = []
        bm = []
        for i in range(wordsize):
            bm.append([])
            for j in range(wordsize):
                if i==j:
                    bm[i].append(1)
                else:
                    bm[i].append(0)

        basis.append(bm)
        bm = []
        for i in range(wordsize):

            bm.append([int(Rpb[i])])

            for j in range(wordsize-1):
                if i==j:
                    bm[i].append(1)
                else:
                    bm[i].append(0)

        basis.append(bm)
        for i in range(wordsize-2):
            bmtemp = bm
            bm = []
            for a in range(wordsize):
                bm.append([])
                for b in range(wordsize):
                    bm[a].append(0)
                    for j in range(wordsize):
                        bm[a][b] ^= bmtemp[a][j]*basis[1][j][b]
            basis.append(bm)


        BM = []
        for i in range(len(MC)*wordsize):
            BM.append([])
            for j in range(len(MC)*wordsize):
                BM[i].append(0)

        #Use the basis to create a binary representation of the MC
        for i in range(len(MC)):
            for j in range(len(MC)):
                e = MC[i][j]
                for a in range(wordsize):
                    for b in range(wordsize):
                        for c in range(wordsize):
                            BM[i*wordsize+b][j*wordsize+c] ^= (basis[a][b][c]&(e>>a)&1)

        

        #Create temp variables for a column
        for i in range(nc*nr*wordsize):
            self.apply_mov("s{}".format(i),"t{}".format(i))

        #Apply the binary MC
        for c in range(nc):
            for i in range(wordsize*nr):
                k = BM[i].index(1)
                self.apply_mov("t{}".format(nr*wordsize*c+k),"s{}".format(nr*wordsize*c+i))
                for j in range(k+1,len(BM[i])):
                    if BM[i][j]==1:
                        self.apply_xor("s{}".format(nr*wordsize*c+i),'t{}'.format(nr*wordsize*c+j),"s{}".format(nr*wordsize*c+i))
    
    
    def apply_MC_serial(self,wordsize,Z,Rp):
        #NOT FINISHED
        #STILL NEEDS TESTING
        '''
        Apply MixColumns for serial matrices. Z is the last row.
        Assumes state bits are numbered columnwise and that MC is stored row-wise
        '''
        #Get dimension of the matrix
        d = len(Z) 
        
        #Get bits of the irreducible polynomial
        Rpb = list(format(Rp,'0{}b'.format(wordsize)))

        #Create a basis using the powers of 2
        basis = []
        bm = []
        for i in range(wordsize):
            bm.append([])
            for j in range(wordsize):
                if i==j:
                    bm[i].append(1)
                else:
                    bm[i].append(0)

        basis.append(bm)
        bm = []
        for i in range(wordsize):
            bm.append([int(Rpb[i])])
            for j in range(wordsize-1):
                if i==j:
                    bm[i].append(1)
                else:
                    bm[i].append(0)

        basis.append(bm)
        for i in range(wordsize-2):
            bmtemp = bm
            bm = []
            for a in range(wordsize):
                bm.append([])
                for b in range(wordsize):
                    bm[a].append(0)
                    for j in range(wordsize):
                        bm[a][b] ^= bmtemp[a][j]*basis[1][j][b]
            basis.append(bm)
                    
        BZ = []
        for i in range(wordsize):
            BZ.append([])
            for j in range(d*wordsize):
                BZ[i].append(0)

        
        #Use the basis to create a binary representation of the MC
        for i in range(d):
            e = Z[i]
            for a in range(wordsize):
                for b in range(wordsize):
                    for c in range(wordsize):
                        BZ[b][i*wordsize+c] ^= (basis[a][b][c]&(e>>a)&1)
        
        shuffle = []
        for i in range(d):
            shuffle.extend([d*i+(j+1)%d for j in range(d)])
        
        for q in range(d):
            for c in range(d):
                for i in range(wordsize):
                    k = BZ[i].index(1)
                    self.apply_mov("s{}".format(d*wordsize*c+k),"t{}".format(wordsize*c+i))
                    for j in range(k+1,len(BZ[i])):
                        if BZ[i][j]==1:
                            self.apply_xor("t{}".format(wordsize*c+i),'s{}'.format(d*wordsize*c+j),"t{}".format(wordsize*c+i))
            
            self.shufflewords(shuffle,wordsize,1)
            for i in range(d*wordsize):
                #print (d-1)*wordsize*(i/wordsize+1)+i
                self.apply_mov("t{}".format(i),"s{}".format((d-1)*wordsize*(i/wordsize+1)+i))
                

    def shufflewords(self,shuffle,wordsize,rev):
        '''
        Apply shuffle to the words of the state.
        If rev == 1 
        updates word i with word shuffle[i]
        else 
        updates word shuffle[i] with word i
        '''
        #Decompose cycles
        cycles = []
        for i in range(len(shuffle)):
            cycles.append([i,shuffle[i]])

            while cycles[len(cycles)-1][0] != cycles[len(cycles)-1][len(cycles[len(cycles)-1])-1]:
                cycles[len(cycles)-1].append(shuffle[cycles[len(cycles)-1][len(cycles[len(cycles)-1])-1]])

        #Remove duplicate cycles and cycles of length 1
        for c in cycles:
            if len(c)==2:
                cycles.remove(c)
        for c in cycles:
            for cp in cycles[cycles.index(c)+1:]:
                if c[0] in cp:
                    cycles.remove(cp)

        #Last entry is equal to first so first is removed
        for c in cycles:
            c.pop(0)

        #Reverse cycles 
        if rev == 1:
            for c in cycles:
                c = c.reverse()
        
        #Apply the cycles to the bits
        bitshuffle = []
        for bit in range(wordsize):

            for c in cycles:
                t = []
                for i in c:
                    t.append("s{}".format(i*wordsize+bit))
                bitshuffle.append(t)

        for b in bitshuffle:
            self.apply_permutation(b)
    
    
    def add_mod(self,x,y,z,n,toffset):
        '''
        Calculates z = x+y mod 2^n
        where n is the lenght of x, y, and z
        x,y are list of state variables with x[0] and y[0] as the LSB
        '''
        #Make copies
        for i in range(n):
            self.apply_mov(x[i],'t{}'.format(toffset+i))
            self.apply_mov(y[i],'t{}'.format(toffset+i+n))
        
        #Set z to x
        for i in range(n):
            self.apply_mov(x[i],z[i])
        
        #Carry bit
        self.apply_and('t{}'.format(toffset),'t{}'.format(toffset+n),'t{}'.format(toffset+2*n))
        
        self.apply_xor(z[0],'t{}'.format(toffset+n),z[0])
        for i in range(1,n):
            self.apply_xor(z[i],'t{}'.format(toffset+n+i),z[i])
            self.apply_xor(z[i],'t{}'.format(toffset+2*n),z[i])
            #Update carry bit
            self.apply_xor('t{}'.format(toffset+i),'t{}'.format(toffset+i+n),'t{}'.format(toffset+2*n+1))
            self.apply_and('t{}'.format(toffset+i),'t{}'.format(toffset+i+n),'t{}'.format(toffset+2*n+2))
            self.apply_and('t{}'.format(toffset+2*n+1),'t{}'.format(toffset+2*n),'t{}'.format(toffset+2*n))
            self.apply_xor('t{}'.format(toffset+2*n+2),'t{}'.format(toffset+2*n),'t{}'.format(toffset+2*n))
    
    def addconstant_mod(self,x,z,n,toffset):
        '''
        Calculates z = x+k mod 2^n
        where n is the lenght of x and z
        x is a list of state variables with x[0] as the LSB
        k is a constant
        '''
        #Make copies
        for i in range(n):
            self.apply_mov(x[i],'t{}'.format(toffset+i))
        
        #Carry bit
        self.apply_mov(x[0],'t{}'.format(toffset+n))
        
        self.apply_mov(x[0],z[0])
        for i in range(1,n):
            self.apply_xor('t{}'.format(toffset+i),'t{}'.format(toffset+n),z[i])
            #Update carry bit
            self.apply_and('t{}'.format(toffset+i),'t{}'.format(toffset+n),'t{}'.format(toffset+n))
            self.apply_xor('t{}'.format(toffset+i),'t{}'.format(toffset+n),'t{}'.format(toffset+n))
