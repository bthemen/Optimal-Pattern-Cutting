import numpy as np
import random

class SelectParent:
    def __init__(self, expectation: np.array, population_size: int, parent_size: int) -> np.array:
        # Return indices of parents chosen for crossover mutation

        # Create a dart wheel based on fit genome probabilities
        wheel = np.cumsum(expectation) / parent_size

        # Add genome as parent if random number lands in its roulette slot
        parents = np.zeros(parent_size, dtype=int)
        for i in range(parent_size):
            r = random.random() # Random value between 0 and 1
            for j in range(population_size):
                if r < wheel[j]:
                    parents[i] = j
                    break

        # Shuffle the parents
        random.shuffle(parents)

        return parents