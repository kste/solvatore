""" A division property solver based on the CryptoMiniSat 5 solver.
"""
from pycryptosat import Solver
import sys
from math import log
from itertools import combinations, product
from functools import reduce
from operator import or_

class Solvatore(object):
    def __init__(self):
        '''
        Create a new Solvatore instance
        '''
        self.cipher = None
        self.round_states =[]
        self.rounds = None
        self.fresh_conditions = False
        self.sbox_cnfs = {}
        self.model_size = 0
        return

    def load_cipher(self, cipher):
        '''
        Load a cipher description to Solvatore
        '''
        self.model_size = 0
        self.cipher = cipher
        self.state_size = cipher.state_size
        self.fresh_conditions = False
        self.set_rounds(cipher.rounds)
        self.sbox_cnfs = {}
        
        return
    

        
    def addclause(self,clause):
        self.solver.add_clause(clause)
        self.model_size +=1
        return
        
    def set_rounds(self, rounds):
        '''
        Specify the number of times the round transition is applied
        '''
        rounds = int(rounds)
        if not rounds >= 0:
            print('The number of rounds needs to be positive')
            sys.exit(1)
        self.rounds = rounds
        self.fresh_conditions = False
        return

    def create_conditions(self):
        '''
        Create conditions for solver from cipher description
        '''
        if self.cipher == None:
            print('You need to load a cipher.')
            sys.exit(1)
        if  self.rounds == None:
            print('You need to specify the number of rounds.')
            sys.exit(1)
        if self.fresh_conditions:
            return
        self.solver = Solver()
        self.next_variable = 1
        self.state_bit = [i + 1 for i in range(self.state_size)]
        state = [self.state_bit[i] for i in range(self.state_size)]
        self.round_states.append(state)
        self.next_variable += self.state_size
        self.temporary = {i: None for i in self.cipher.temporaries}
        self.sbox_tmps = {}

        for rnd in range(self.rounds):
            for step in self.cipher.transition:
                if step[-1] == 'XOR':
                    self.apply_xor(step[0], step[1], step[2])
                elif step[-1] == 'AND':
                    self.apply_and(step[0], step[1], step[2])
                elif step[-1] == 'PERM':
                    self.apply_permutation(step[0])
                elif step[-1] == 'SBOX':
                    self.apply_sbox(step[0], step[1], step[2])
                elif step[-1] == 'MOV':
                    self.apply_mov(step[0], step[1])
            self.set_temporaries_to_zero()
            state = [self.state_bit[i] for i in range(self.state_size)]
            self.round_states.append(state)
        self.fresh_conditions = True
        return

    def apply_mov(self, target, source):
        """ When target != source, we have the following allowed trails
            on source, target:
              0 0 -> 0 0
              1 0 -> 0 1
              1 0 -> 1 0
            In particular, when the target is a state bit, it cannot be equal
            to 1.
        """
        if target == source:
            return
        old_source, new_source = self.get_variables(source)
        old_target, new_target = self.get_variables(target)
        #Ensure old target is 0
        if old_target != None:
            self.addclause([-old_target])
        self.addclause([-old_source, new_source, new_target])
        self.addclause([old_source, -new_source])
        self.addclause([old_source, -new_target])
        self.addclause([-new_source, -new_target])
        return

    def apply_xor(self, target, source_1, source_2):
        """ First move source_2 to target, then apply the following
            rules on source_1, target:
              0 0 -> 0 0
              0 1 -> 0 1
              1 0 -> 1 0
              1 0 -> 0 1
              1 1 -> 1 1
        """
        if source_1 == source_2:
            old_target, new_target = self.get_variables(target)
            self.addclause([-new_target])
            return
        if source_1 != target:
            self.apply_mov(target, source_2)
            source = source_1
        else:
            source = source_2
        old_source, new_source = self.get_variables(source)
        old_target, new_target = self.get_variables(target)
        self.addclause([-new_source, old_source])
        self.addclause([new_target, -old_target])
        self.addclause([-new_source, -new_target, old_target])
        self.addclause([new_source, new_target, -old_source])
        self.addclause([-new_target, old_source, old_target])
        self.addclause([new_source, -old_source, -old_target])
        return

    def apply_and(self, target, source_1, source_2):
        """ First move source_2 to target, then apply the following
            rules on source_1, target:
              0 0 -> 0 0
              0 1 -> 0 1
              1 0 -> 1 0
              1 0 -> 0 1
              1 1 -> 0 1
        """
        if source_1 == source_2:
            self.apply_mov(target, source_1)
            return
        if source_1 != target:
            self.apply_mov(target, source_2)
            source = source_1
        else:
            source = source_2
        old_source, new_source = self.get_variables(source)
        old_target, new_target = self.get_variables(target)
        self.addclause([-new_source, old_source])
        self.addclause([new_target, -old_target])
        self.addclause([-new_source, -new_target])
        self.addclause([new_source, new_target, -old_source])
        self.addclause([-new_target, old_source, old_target])
        return

    def apply_permutation(self, permutation):
        '''
        Relabel the state bits according to the permutation
        '''
        last_value = int(permutation[-1][1:])
        tmp = self.state_bit[last_value]
        for bit in permutation:
            number = int(bit[1:])
            self.state_bit[number], tmp = tmp, self.state_bit[number]
        return

    def apply_sbox(self, sbox_name, input_bits, output_bits):
        cnf = self.get_sbox_cnf(sbox_name, len(input_bits), len(output_bits))
        for bit in input_bits:
            self.apply_mov('copy_' + bit, bit)
        sources = [self.get_variables('copy_' + bit) for bit in input_bits]
        targets = [self.get_variables(bit) for bit in output_bits]
        for in_clause, out_clause in cnf:
            clause = [sources[i][0] if in_clause[i] == 1 else \
                      -sources[i][0] for i in range(len(sources))]
            clause += [targets[i][1] if out_clause[i] == 1 else \
                       -targets[i][1] for i in range(len(targets))]
            self.addclause(clause)
        # Ensure that the target bits did not contain 1s
        for i in range(len(targets)):
            self.addclause([-targets[i][0]])

    def get_sbox_cnf(self, sbox_name, n, m):
        if sbox_name in self.sbox_cnfs:
            return self.sbox_cnfs[sbox_name]
        if sbox_name not in self.cipher.sboxes:
            raise KeyError('sbox_name not in cipher.sboxes')
        sbox = self.cipher.sboxes[sbox_name]
        anf = self.get_anf(sbox)
        # Store the products of the output anfs in products
        products = []
        for output_dp in range(2**m):
            # Set the empty product to the constant 1
            prod = [0 for _ in range(2**n)]
            prod[0] = 1
            # Multiply the anfs of the selected output bits
            for i in range(m):
                if (output_dp >> i) & 1:
                    # multiply prod with output bit
                    result = [0 for _ in range(2**n)]
                    for j in range(2**n):
                        for k in range(2**n):
                            result[j|k] ^= prod[j] * ((anf[k] >> i) & 1)
                    prod = result
            products.append(prod)
        # Store guaranteed zero derivatives
        zero_derivatives = []
        for input_dp in range(2**n):
            for output_dp in range(2**m):
                prod = products[output_dp]
                # If not term in the output product contains all selected
                # input bits, the derivative is zero, so we store it.
                if not any(input_dp & i == input_dp for i in range(2**n) if prod[i]):
                    zero_derivatives.append((input_dp, output_dp))
        # As the zero derivatives are the transitions we want to exclude,
        # we can use them to generate the CNF.
        cnf = []
        for in_dp, out_dp in zero_derivatives:
            cnf.append((tuple(((in_dp >> i) & 1) ^ 1 for i in range(n)),\
                       tuple(((out_dp >> i) & 1) ^ 1 for i in range(m))))
        self.sbox_cnfs[sbox_name] = cnf
        return cnf

    def get_anf(self, sbox):
        n = int(log(len(sbox), 2))
        anf = [x for x in sbox]
        for i in range(n):
            mask = (1 << i)
            for j in range(len(anf)):
                if j & mask:
                    anf[j] ^= anf[j^mask]
        return anf

    def is_sbox_bijective(self, sbox, n, m):
        if n != m:
            return False
        if len(set(sbox[i & (2**n-1)] for i in range(2**n))) != 2**n:
            return False
        return True

    def set_temporaries_to_zero(self):
        '''
        To guarantee that temporaries are zero at end of rounds
        '''
        for tmp in self.temporary.values():
            self.addclause([-tmp])
        return

    def get_variables(self, bit):
        if bit[0] == 's':
            number = int(bit[1:])
            old_bit = self.state_bit[number]
            new_bit = self.next_variable
            self.state_bit[number] = new_bit
            self.next_variable += 1
        elif bit[0] == 't':
            old_bit = self.temporary[bit]
            new_bit = self.next_variable
            self.temporary[bit] = new_bit
            self.next_variable += 1
        else:
            if bit in self.sbox_tmps:
                old_bit = self.sbox_tmps[bit]
            else:
                old_bit = None
            new_bit = self.next_variable
            self.next_variable += 1
            self.sbox_tmps[bit] = new_bit
        return old_bit, new_bit

    def is_bit_balanced(self, bit, rnd, active):
        self.create_conditions()
        if bit >= self.state_size:
            raise ValueError("There are only {} state bits."\
                             .format(self.state_size))
        active_bits = map(int, active)
        for active_bit in active_bits:
            if active_bit >= self.state_size or active_bit < 0:
                print('Bit {} designated as active bit, but there are only '
                      '{} state bits.'.format(active_bit, self.state_size))
                sys.exit(1)
        conditions = []
        for i in range(self.state_size):
            if i in active_bits:
                conditions.append(self.round_states[0][i])
            else:
                conditions.append(-self.round_states[0][i])
        for i in range(self.state_size):
            if i != bit:
                conditions.append(-self.round_states[rnd][i])
            else:
                conditions.append(self.round_states[rnd][i])
        unbalanced, _ = self.solver.solve(conditions)
        return not unbalanced

    def distinguisher_exists(self, rnd):
        #TODO: not working at the moment
        self.create_conditions()

        # No all zero input, no all active input
        input_allzero = [self.round_states[0][i] for i in range(self.state_size)]
        input_allone = [-self.round_states[0][i] for i in range(self.state_size)]
        self.addclause(input_allzero)
        self.addclause(input_allone)

        # At least one unit vector reachable
        out_cond = [self.round_states[rnd][i] for i in range(self.state_size)]
        self.addclause(out_cond)

        # No pair should be sat together
        for pair in combinations(range(self.state_size), 2):
            exclude_pair = [-self.round_states[rnd][pair[0]],
                            -self.round_states[rnd][pair[1]]]
            self.addclause(exclude_pair)
        sat, solution = self.solver.solve()

        # for r in range(rnd + 1):
        #     print("\nRound {}: ".format(r))
        #     for i in self.round_states[r]:
        #         print int(solution[i]),

        return sat, solution


    def is_reachable(self, output_bits, rnd, active_bits):
        self.create_conditions()
        conditions = []
        for i in range(self.state_size):
            if i in active_bits:
                conditions.append(self.round_states[0][i])
            else:
                conditions.append(-self.round_states[0][i])
        for i in range(self.state_size):
            if i not in output_bits:
                conditions.append(-self.round_states[rnd][i])
            else:
                conditions.append(self.round_states[rnd][i])
        reachable, _ = self.solver.solve(conditions)
        return reachable
