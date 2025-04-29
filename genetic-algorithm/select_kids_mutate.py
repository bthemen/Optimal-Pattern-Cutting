import numpy as np
import random_genome

class SelectKidsMutate:
    def __init__(self, genomes, parents, genome_length, ws_width, ws_height, mutation_rate):
        # TODO: mutations should be based on constraints

        kids_mutated = []   # Initialization
        for i in range(len(parents)):
            # Get kid
            kid = genomes[parents[i]]

            # Find mutation points
            r = np.random.rand(1, genome_length)
            mutation_points = np.where(r < mutation_rate)   # Mutate genes that are below the threshold

            # Create new genome
            mutated_genome = random_genome(genome_length, ws_width, ws_height)

            # Create mutated kid
            kid[mutation_points] = mutated_genome[mutation_points]

            # Save to list
            kids_mutated.append(kid)

        return kids_mutated