import numpy as np

class RandomGenome:
    def __init__(self, genome_length, ws_width, ws_height):
        # Create random values for the x and y coordinates of the pattern piece centers
        random_value_x = ws_width * np.random.uniform(0, 1, size=genome_length // 2)
        random_value_y = ws_height * np.random.uniform(0, 1, size=genome_length // 2)
        # TODO: add rotation of pattern pieces

        # Fill genome
        current_genome = np.zeros([1, genome_length])
        for i in range(genome_length // 2):
            current_genome[0, 2 * i]       = random_value_x[i]
            current_genome[0, 2 * i + 1]   = random_value_y[i]

        return current_genome