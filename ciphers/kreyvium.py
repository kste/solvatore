from cipher_description import CipherDescription

#(iv127 ... iv0) = (s288 ... s415)




def generate_Kreyvium_version(rounds):
    kreyvium = CipherDescription(416)

    for i in range(128):
        kreyvium.apply_mov("s{}".format(93+i), "s{}".format(288+i))

    for r in range(rounds):
        kreyvium.apply_xor("s65", "s92", "t1")
        kreyvium.apply_xor("s161", "s176", "t2")
        kreyvium.apply_xor("s242", "s287", "t3")

        kreyvium.apply_and("s90", "s91", "tand1")
        kreyvium.apply_and("s174", "s175", "tand2")
        kreyvium.apply_and("s285", "s286", "tand3")

        kreyvium.apply_xor("t1", "tand1", "t1")
        kreyvium.apply_xor("t1", "s415", "t1")
        kreyvium.apply_xor("t1", "s170", "s92")

        kreyvium.apply_xor("t2", "tand2", "t2")
        kreyvium.apply_xor("t2", "s263", "s176")

        kreyvium.apply_xor("t3", "tand3", "t3")
        kreyvium.apply_xor("t3", "s68", "s287")

        switch_last_bits = ("s92", "s176", "s287")
        kreyvium.apply_permutation(switch_last_bits)

        permutation_1 = tuple("s{}".format(i) for i in range(93))
        permutation_2 = tuple("s{}".format(i) for i in range(93, 177))
        permutation_3 = tuple("s{}".format(i) for i in range(177, 288))
        permutation_4 = tuple("s{}".format(i) for i in range(288, 416))
        kreyvium.apply_permutation(permutation_1)
        kreyvium.apply_permutation(permutation_2)
        kreyvium.apply_permutation(permutation_3)
        kreyvium.apply_permutation(permutation_4)

    return kreyvium