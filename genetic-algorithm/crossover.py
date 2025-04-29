import numpy as np
import random

class SelectKidsCrossover:
    def __init__(self, genomes: list[np.array], parents: np.array, crossover_ratio: float) -> list[np.array]:
        # Get number of kids
        kids_size = len(parents) // 2

        # Initialization
        kids_crossover = []

        for i in range(kids_size):
            # Get parents
            parent1 = genomes[parents[2 * i]]
            parent2 = genomes[parents[2 * i + 1]]

            # Get scaling factor
            scale = crossover_ratio * random.random()
            delta = scale * (parent2 - parent1)

            # Create kid
            kids_crossover.append(parent1 + delta)

        return kids_crossover