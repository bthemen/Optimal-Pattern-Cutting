from genome import Genome
from workspace import Workspace

class Population:
    # Constructor
    def __init__(self, size: int) -> None:
        self.size = size
        self.genomes: list[Genome] | None = None

    # Initialize population
    def initialize(self, genome_length: int, ws: Workspace) -> None:
        # Create list of Genome objects and initialize their design vectors
        population = [None] * self.size
        for i in range(self.size):
            genome = Genome(genome_length)
            genome.random_genome(ws)  # Fill the design_vector
            population[i] = genome

        self.genomes = population

    # # Create new population
    # def evolve_population(self) -> None:
    #     # Create kids
    #     kids_elite = select_kids_elite(population, fitness_values) # Elites
    #     kids_crossover = select_kids_crossover(population, parents[:(2 * CROSSOVER_SIZE)]) # Crossover
    #     kids_mutated = select_kids_mutate(population, parents[(2 * CROSSOVER_SIZE):])  # Mutations

    #     # Make the new population
    #     population = kids_elite + kids_crossover + kids_mutated
    #     pass

    # String representation
    def __str__(self) -> str:
        return f"Population with {self.size} genomes"

    # Developer representation
    def __repr__(self) -> str:
        return f"Population(size={self.size}, genomes={self.genomes})"