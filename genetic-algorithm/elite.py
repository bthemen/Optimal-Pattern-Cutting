import numpy as np

class SelectKidsElite:
    def __init__(self, genomes: list[np.array], fitness_values: list[np.array], population_size: int, elite_size: int) -> list[np.array]:
        # Get the indices that would sort the population by most fit
        sorted_indices = sorted(range(population_size), key=lambda i: fitness_values[i])

        # Select elite kids
        kids_elite = [genomes[i] for i in sorted_indices[0:elite_size]]

        return kids_elite