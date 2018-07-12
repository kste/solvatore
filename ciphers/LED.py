from cipher_description import CipherDescription



  
LED = CipherDescription(64)
s = 4 
d = 4
IP = 3
Z = [4,1,2,2]
    
#Add the appropriate sbox
sbox = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
        0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]
LED.add_sbox('S-box',sbox)
    
    
#Apply the sbox to all cells
for i in range(d*d):
    bits = []
    for j in range(s):
        bits.append("s{}".format(s*i + s - 1 - j))
    LED.apply_sbox('S-box', bits, bits)

#Define and apply shiftrows
tshuffle = []
for i in range(d):
    tshuffle.append([((j+i)%d)*d+i for j in range(d)])

shuffle = []
for i in range(d):
    for j in range(d):
        shuffle.append(tshuffle[j][i])

LED.shufflewords(shuffle,s,1)


#Apply MixColumns
LED.apply_MC_serial(s,Z,IP)

'''
MC = []
for i in range(d-1):
    temp = [0]
    for j in range(d-1):
        if i==j:
            temp.append(1)
        else: 
            temp.append(0)
    MC.append(temp)
MC.append(Z)

for i in range(d):
    LED.apply_MC(s,MC,IP,d,d)

'''
