# Qubit class
import cmath
import math
import random
from state import State

class Qubit:

    def __init__(self, x, y):
        self.a = x
        self.b = y
        if not abs(self.a) + abs(self.b) == 1:
            print("Invalid parameters: unitarity not upheld. Defaulting...")
            self.a = 0.5
            self.b = 0.5
        self.collapsed = False

    def info(self):

        print(f"{self.a}*|0> + {self.b}*|1>")

    def measure(self):
        if not self.collapsed:
            self.collapsed = True
            prob_0 = abs(self.a)
            random_num = random.random()
            if self.a == 1:
                return State(1, [0])
            elif self.b == 1:
                return State(1, [1])
            elif random_num < prob_0:
                self.a = 1
                self.b = 0
                return State(1, [0])
            else:
                self.b = 1
                self.a = 0
                return State(1, [1])
