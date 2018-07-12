from cipher_description import CipherDescription


bivium = CipherDescription(177)
bivium.apply_xor("s65", "s92", "t0")
bivium.apply_and("s90", "s91", "t1")
bivium.apply_xor("t0", "t1", "t2")
bivium.apply_xor("t2", "s170", "s92")
bivium.apply_xor("s161", "s176", "t3")
bivium.apply_and("s174", "s175", "t4")
bivium.apply_xor("t3", "t4", "t5")
bivium.apply_xor("t5", "s68", "s176")
switch_last_bits = ("s92", "s176")
bivium.apply_permutation(switch_last_bits)
permutation_1 = tuple("s{}".format(i) for i in range(93))
permutation_2 = tuple("s{}".format(i) for i in range(93, 177))
bivium.apply_permutation(permutation_1)
bivium.apply_permutation(permutation_2)
bivium.set_rounds(708)
