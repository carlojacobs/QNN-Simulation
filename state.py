# State
import numpy as np

class State:
    def __init__(self, length, values, qubit_number):
        self.length = length
        self.values = values
        self.state_str = "".join(str(x) for x in values)
        state_vec = np.zeros(2**length)
        state_vec[qubit_number] = 1
        self.state_vec = state_vec
