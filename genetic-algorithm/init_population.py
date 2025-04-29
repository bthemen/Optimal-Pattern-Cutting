import random_genome

class InitPopulation:
    def __init__(self, genome_length, ws_width, ws_height, population_size):

        # TODO: add initialization through provided SVG

        # Random genome population
        population = [random_genome(genome_length, ws_width, ws_height) for _ in range(population_size)]

        return population