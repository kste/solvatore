# Solvatore

Solvatore is a tool to help with the cryptanalysis of cryptographic primitives and enables a simply way to find integral distinguishers (for more details on the theory and cryptanalytic results see our paper [1]). It is based on the bit-based division property introduced in [2] and makes the process of carrying out this type of analysis very simple for many commonly used design strategies.

The main goal of this analysis is to find a distinguisher, which allows us to distinguish the primitive from a random function which can often be used to further construct a key-recovery attack. For any good cryptographic primitive such distinguishers should not exist and it is therefore important to evaluate this property.

The idea behind these integral distinguishers is that we have a set of inputs to our function **a1, a2, ...** which are all different in some positions, which we refer to as *active* bits, and the property we are looking for is that some the output bits **f(a1), f(a2), ...** are *balanced*. What we mean by balanced here is that if we sum up (XOR) all the outputs then the *balanced* bits will sum to 0 with a probability of 1.

# Install

Solvatore requires the pqcryptosat python package. You can either get a current version from the [CryptoMiniSat repository] (https://github.com/msoos/cryptominisat) or install it with pip:

```
pip install pycryptosat
```

At the moment Solvatore has only been tested with Python2.

# Description of a cryptographic primitive

In the following we will look how to write a cipher description in order to carry out any further cryptanalysis. As an example we choose the lightweight block cipher [`PRESENT`](ciphers/present.py). For the bit-based division property we can ignore the details of the key schedule and only need to consider the update of the internal state.

We first define the S-box and bit-permutation (in cycle notation) which are used in PRESENT:

```python
from cipher_description import CipherDescription


present_sbox = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
                0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

present_permutations = present_permutations = [\
  ['s1', 's16', 's4'], ....
```

Next we have to define the state of our block cipher:

```python
present = CipherDescription(64)
```

We have a 64-bit block cipher, so we need 64 bits to represent the internal state. These bits will be represented as "s0,...,s63" internally. The next step is to define how the state is updated in a single round. In the case of the S-box we can simply add it to our `present` object and apply the S-box to the corresponding bits of the state.

```python
present.add_sbox('S-box', present_sbox)
for i in range(16):
    bits = ["s{}".format(4*i + 0),
            "s{}".format(4*i + 1),
            "s{}".format(4*i + 2),
            "s{}".format(4*i + 3)]
present.apply_sbox('S-box', bits, bits)
```

In a similar way we can simply apply each bit-permutation to the state:

```python
for p in present_permutations:
  present.apply_permutation(p)
```

Solvatore supports most of the operations which are used in the design of cryptographic primitives like S-boxes, permutations, modular addition or matrix multiplications.

# Cryptanalysis of our cipher

Now that we have a cipher description, we can use it to analysis PRESENT. We first have to include solvatore, the cipher description and create our `present` object:

```python
from itertools import combinations
from solvatore import Solvatore
from cipher_description import CipherDescription
from ciphers import present

cipher = present.present
rounds = 9
```

The next step is to setup solvatore and initialize it with our parameters:

```python
solver = Solvatore()
solver.load_cipher(cipher)
solver.set_rounds(rounds)
```

We are now ready to find bit-based division property distinguishers for PRESENT. All we have to do is to define a set of *active* bits and then we can use Solvatore to check if a bit after 9 rounds is *balanced*. A simple way to check if any distinguisher exists is to only have a single bit constant and test all possible position for this constant bit:

```python
for bits in combinations(range(64), 1):
    constant_bits = bits
    active_bits = {i for i in range(64) if i not in constant_bits}
```

Next, we will test for each position whether the bit is *balanced* after 9 rounds. If at least one of the bits is balanced we have found a distinguisher:

```python
    balanced_bits = []
    for i in range(cipher.state_size):
        if solver.is_bit_balanced(i, rounds, active_bits):
            balanced_bits.append(i)

    if len(balanced_bits) > 0:
        print("Found distinguisher!")
```

# References

[1] [Finding Integral Distinguishers with Ease](https://eprint.iacr.org/2018/688.pdf)

[2] [Bit-Based Division Property and Application to Simon Family](https://eprint.iacr.org/2016/285)

