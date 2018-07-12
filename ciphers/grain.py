from cipher_description import CipherDescription


grain = CipherDescription(256)

# LFSR (s0 ... s127)

grain.apply_xor("s0", "s7", "t0")
grain.apply_xor("t0", "s38", "t0")
grain.apply_xor("t0", "s70", "t0")
grain.apply_xor("t0", "s81", "t0")
grain.apply_xor("t0", "s96", "t0")  # t0 is now s_{i + 128}

# NFSR (s128 ... s255) = (b0 ... b127)

grain.apply_and("s131", "s195", "tand0")
grain.apply_and("s139", "s142", "tand1")
grain.apply_and("s145", "s146", "tand2")
grain.apply_and("s155", "s187", "tand3")
grain.apply_and("s168", "s176", "tand4")
grain.apply_and("s189", "s193", "tand5")
grain.apply_and("s196", "s212", "tand6")

grain.apply_xor("s0", "s128", "t1")
grain.apply_xor("t1", "s154", "t1")
grain.apply_xor("t1", "s184", "t1")
grain.apply_xor("t1", "s219", "t1")
grain.apply_xor("t1", "s224", "t1")
grain.apply_xor("t1", "tand0", "t1")
grain.apply_xor("t1", "tand1", "t1")
grain.apply_xor("t1", "tand2", "t1")
grain.apply_xor("t1", "tand3", "t1")
grain.apply_xor("t1", "tand4", "t1")
grain.apply_xor("t1", "tand5", "t1")
grain.apply_xor("t1", "tand6", "t1")  # t1 is now s_{i + 256} + s127

# h
grain.apply_and("s140", "s8", "tand0")
grain.apply_and("s13", "s20", "tand1")
grain.apply_and("s223", "s42", "tand2")
grain.apply_and("s60", "s79", "tand3")
grain.apply_and("s140", "s223", "tand4")
grain.apply_and("tand4", "s95", "tand4")
grain.apply_xor("tand0", "tand1", "th")
grain.apply_xor("th", "tand2", "th")
grain.apply_xor("th", "tand3", "th")
grain.apply_xor("th", "tand4", "th")

# z
grain.apply_xor("th", "s93", "tz")
grain.apply_xor("tz", "s130", "tz")
grain.apply_xor("tz", "s143", "tz")
grain.apply_xor("tz", "s164", "tz")
grain.apply_xor("tz", "s173", "tz")
grain.apply_xor("tz", "s192", "tz")
grain.apply_xor("tz", "s201", "tz")
grain.apply_xor("tz", "s217", "tz")


# Shift registers
permutation_1 = tuple("s{}".format(i) for i in range(128))
permutation_2 = tuple("s{}".format(i) for i in range(128, 256))
grain.apply_permutation(permutation_1)
grain.apply_permutation(permutation_2)

# Feedback output
grain.apply_xor("tz", "t0", "s0")
grain.apply_xor("tz", "t1", "s128")

grain.set_rounds(256)
