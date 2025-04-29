import numpy as np

class FitnessScaling:
    def __init__(self, fitness_values, population_size, parent_size):
        # Get the indices that would sort the list
        sorted_indices = sorted(range(population_size), key=lambda i: fitness_values[i])

        # Create expectation values
        size = population_size
        expectation = np.zeros(size)
        expectation[sorted_indices] = 1 / np.sqrt(np.arange(1, size + 1))

        # Scale with number of parents
        expectation = parent_size * expectation / sum(expectation)

        return expectation