from genome import Genome
from workspace import Workspace
from evolution_config import EvolutionConfig

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

    # String representation
    def __str__(self) -> str:
        return f"Population with {self.size} genomes"

    # Developer representation
    def __repr__(self) -> str:
        return f"Population(size={self.size}, genomes={self.genomes})"