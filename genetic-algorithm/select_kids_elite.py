class SelectKidsElite:
    def __init__(self, genomes, fitness_values, population_size, elite_size):
        # Get the indices that would sort the population by most fit
        sorted_indices = sorted(range(population_size), key=lambda i: fitness_values[i])

        # Select elite kids
        kids_elite = [genomes[i] for i in sorted_indices[0:elite_size]]

        return kids_elite