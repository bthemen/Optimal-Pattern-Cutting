from population import Population
from evolution_config import EvolutionConfig
from genome import Genome

class GeneticAlgorithm:
    def __init__(self, population: Population, config: EvolutionConfig) -> None:
        # Define fields
        self.population         = population                # Population of genomes
        self.elite_size         = config.elite_size         # Number of elite kids
        self.crossover_rate     = config.crossover_rate     # Percentage chance of a genome crossover
        self.crossover_ratio    = config.crossover_ratio    # Ratio of shared genomes between parent 1 and parent 2
        self.mutation_rate      = config.mutation_rate      # Percentage chance of a genome mutation 

    # Create new population
    def evolve_population(self) -> None:
        # Create kids
        kids_elite = self._select_elite() # Elites
        kids_crossover = select_kids_crossover(population, parents[:(2 * CROSSOVER_SIZE)]) # Crossover
        kids_mutated = select_kids_mutate(population, parents[(2 * CROSSOVER_SIZE):])  # Mutations

        # Make the new population
        population = kids_elite + kids_crossover + kids_mutated
        pass

    # Elite kids
    def _select_elite(self) -> list[Genome]:
        # Local alias
        genomes = self.population.genomes

        # Get the indices that would sort the population by most fit
        sorted_indices = sorted(range(self.population.size), key=lambda i: genomes[i].fitness)

        # Select elite kids
        kids_elite = [genomes[i] for i in sorted_indices[0:self.elite_size]]

        return kids_elite

    # Crossover kids
    def _select_crossover(self) -> list[Genome]:
        # Get number of kids
        kids_size = len(parents) // 2

        # Initialization
        kids_crossover = [None] * kids_size

        for i in range(kids_size):
            # Get parents
            parent1 = self.genomes[parents[2 * i]]
            parent2 = self.genomes[parents[2 * i + 1]]

            # Get scaling factor
            scale = crossover_ratio * random.random()
            delta = scale * (parent2 - parent1)

            # Create kid
            kids_crossover.append(parent1 + delta)

        return kids_crossover

    # Mutated kids
    def _select_mutated(self) -> list[Genome]:
        pass