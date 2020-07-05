from qubit import Qubit
from state import State
import cmath
import math
import itertools
import random
import numpy as np
from scipy.constants import hbar

class QubitSystem:

    def __init__(self, N, coeffs):
        self.N = N
        coeffs_len = len(coeffs)
        default_coeffs = []
        for i in range(2**N):
            default_coeffs.append(1/2**N)
        self.coeffs = default_coeffs
        if not coeffs_len == 2**N:
            print(f"""Invalid parameters: invalid number of coefficients ({2**N} required, got
                    {coeffs_len}). Defaulting...""")
            self.coeffs = default_coeffs
        elif not self.checkUnitarity(coeffs):
            print("Invalid parameters: unitarity not upheld. Defaulting...")
            self.coeffs = default_coeffs
        else:
            self.coeffs = coeffs
        self.collapsed = False
        self.basis_states = self.generate_basis_states()

    def checkUnitarity(self, coeffs):
        total = 0
        for c in coeffs:
            total += abs(c)
        if not total == 1:
            return False, total
        else:
            return True

    def generate_basis_states(self):
        N = self.N
        iterations = list(itertools.product([0, 1], repeat=N))
        basis_states = []
        for i in range(0, len(iterations)):
            iter = list(iterations[i])
            basis_states.append(State(N, iter, i))
        return basis_states

    def measure(self, collapse):
        if not self.collapsed:
            if collapse:
                self.collapsed = True
            probs = [abs(x) for x in self.coeffs]
            probs = [x * (2**self.N) for x in probs]
            random_num = random.uniform(0, 2**self.N)
            for i in range(0, len(probs)):
                prob_sum = sum(probs[0:i+1])
                if random_num < prob_sum:
                    self.collapsed_state = self.basis_states[i]
                    return self.collapsed_state
        else:
            return self.collapsed_state



    def test_probabilities(self, epochs):
        print("Info:\n")
        self.info()
        print("\n")
        print(f"Testing measurement probabilieties with {epochs} epochs...\n")
        results = {}
        for i in range(epochs):
            result = self.measure(False)
            if result.state_str in results:
                results[result.state_str] += 1
            else:
                results[result.state_str] = 1
        for key in sorted(results.keys()):
            print(f"""Estimated probability for state |{key}>: {results[key]/epochs}""")

    def info(self):
        basis_states = self.generate_basis_states()
        info_str = ""
        for i in range(0, len(basis_states)):
            info_str += f"{self.coeffs[i]}*|{basis_states[i].state_str}>"
            if not i == len(basis_states) - 1:
                info_str += " + "
        print(info_str)


    def generate_state(self):
        final_state = np.zeros(2**self.N)
        final_state = [complex(x) for x in final_state]
        for i in range(0, len(self.coeffs)):
            basis_state = self.basis_states[i]
            coeff = self.coeffs[i]
            basis_state_vector = np.array(basis_state.state_vec)
            final_state += coeff*basis_state_vector
        return final_state

    def time_independent_isolated_evo(self, omega, t):
        print("Evolving in time...\n")
        original_state = self.generate_state()
        evolved_state = np.exp(-1j*t*1.244)*original_state
        # evolved_state = np.matmul(np.exp(-1j*omega*t), original_state)
        self.update_after_evo(evolved_state)

    def update_after_evo(self, evolved_state):
        # Calculate coefficients
        new_coeffs = []
        for i in range(0, len(self.basis_states)):
            basis_state = np.array(self.basis_states[i].state_vec)
            new_coeff = np.dot(basis_state, evolved_state)
            new_coeffs.append(new_coeff)
        self.coeffs = new_coeffs
        print(self.coeffs)
        print(self.checkUnitarity(self.coeffs), "\n")
