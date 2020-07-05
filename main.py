from qubitsystem import QubitSystem

if __name__ == "__main__":
    system = QubitSystem(2, [0.25, 0.5, 0.125, 0.125])
    system.info()
    system.test_probabilities(10000)
