from cipher_description import CipherDescription


trivium = CipherDescription(288)
trivium.apply_xor("s65", "s92", "t1")
trivium.apply_xor("s161", "s176", "t2")
trivium.apply_xor("s242", "s287", "t3")


trivium.apply_and("s90", "s91", "tand1")
trivium.apply_and("s174", "s175", "tand2")
trivium.apply_and("s285", "s286", "tand3")

trivium.apply_xor("t1", "tand1", "t1")
trivium.apply_xor("t1", "s170", "s92")

trivium.apply_xor("t2", "tand2", "t2")
trivium.apply_xor("t2", "s263", "s176")

trivium.apply_xor("t3", "tand3", "t3")
trivium.apply_xor("t3", "s68", "s287")

switch_last_bits = ("s92", "s176", "s287")
trivium.apply_permutation(switch_last_bits)

permutation_1 = tuple("s{}".format(i) for i in range(93))
permutation_2 = tuple("s{}".format(i) for i in range(93, 177))
permutation_3 = tuple("s{}".format(i) for i in range(177, 288))
trivium.apply_permutation(permutation_1)
trivium.apply_permutation(permutation_2)
trivium.apply_permutation(permutation_3)
trivium.set_rounds(1152)
