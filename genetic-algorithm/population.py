from genome import Genome
from workspace import Workspace
import numpy as np

class Population:
    # Constructor
    def __init__(self, size: int) -> None:
        # Define fields
        self.size = size  # Population per generation
        self.genomes: list[Genome] | None = None

    # Initialize population
    def initialize(self, genome_length: int, ws: Workspace) -> None:
        # TODO: add initialization through provided SVG

        # Create list of Genome objects and initialize their design vectors
        population = [None] * self.size
        for i in range(self.size):
            genome = Genome(genome_length, ws)
            population[i] = genome

        self.genomes = population

    # Scale fitness
    def scale_fitness(self, parent_size: int) -> np.array:
        # Get the indices that would sort the list
        sorted_indices = sorted(range(self.size), key=lambda i: self.genomes[i].fitness)

        # Create expectation values
        expectation = np.zeros(self.size)
        expectation[sorted_indices] = 1 / np.sqrt(np.arange(1, self.size + 1))

        # Scale with number of parents
        expectation = parent_size * expectation / sum(expectation)

        return expectation

    # Set genomes
    def set_genomes(self, genomes: list[Genome]) -> None:
        self.genomes = genomes

    # String representation
    def __str__(self) -> str:
        return f"Population with {self.size} genomes"

    # Developer representation
    def __repr__(self) -> str:
        return f"Population(size={self.size}, genomes={self.genomes})"