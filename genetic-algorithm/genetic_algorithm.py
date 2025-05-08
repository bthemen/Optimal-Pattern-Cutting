from population import Population
from evolution_config import EvolutionConfig
from genome import Genome
from workspace import Workspace
import numpy as np
import random

class GeneticAlgorithm:
    def __init__(self, population: Population, config: EvolutionConfig) -> None:
        # Define fields
        self.population         = population                # Population of genomes
        self.elite_size         = config.elite_size         # Number of elite kids
        self.crossover_rate     = config.crossover_rate     # Percentage chance of a genome crossover
        self.crossover_ratio    = config.crossover_ratio    # Ratio of shared genomes between parent 1 and parent 2
        self.mutation_rate      = config.mutation_rate      # Percentage chance of a genome mutation 

        # Calculate remaining sizes
        self.crossover_size  = round(self.crossover_rate * (self.population.size - self.elite_size))    # Number of crossover kids
        self.mutation_size   = self.population.size - self.elite_size - self.crossover_size             # Number of mutated kids
        self.parent_size     = 2 * self.crossover_size + self.mutation_size                             # Number of parents

    # Create new population
    def evolve_population(self, ws: Workspace) -> None:
        # Create parents based on expectation values
        expectation = self.population.scale_fitness(self.parent_size)
        parents = self._select_parent(expectation)

        # Create kids
        kids_elite = self._select_elite() # Elites
        kids_crossover = self._select_crossover(parents[:(2 * self.crossover_size)]) # Crossover
        kids_mutated = self._select_mutated(parents[(2 * self.crossover_size):], ws)  # Mutations

        # Make the new population
        self.population.set_genomes(kids_elite + kids_crossover + kids_mutated)
        pass

    # Parents
    def _select_parent(self, expectation: np.array) -> list[int]:
        # Return indices of parents chosen for crossover and mutation

        # Create a dart wheel based on fit genome probabilities
        wheel = np.cumsum(expectation) / self.parent_size

        # Add genome as parent if random number lands in its roulette slot
        parents = [None] * self.parent_size
        for i in range(self.parent_size):
            r = random.random() # Random value between 0 and 1
            for j in range(self.population.size):
                if r < wheel[j]:
                    parents[i] = j
                    break

        # Shuffle the parents
        random.shuffle(parents)

        return parents

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
    def _select_crossover(self, parents: list[int]) -> list[Genome]:
        # Initialization
        kids_crossover = [None] * self.crossover_size

        for i in range(self.crossover_size):
            # Get parents
            parent1 = self.population[parents[2 * i]]
            parent2 = self.population[parents[2 * i + 1]]

            # Get scaling factor
            scale = self.crossover_ratio * random.random()
            delta = scale * (parent2.design_vector - parent1.design_vector)

            # Create kid
            genome = parent1 + delta
            kids_crossover[i] = Genome(genome)

        return kids_crossover

    # Mutated kids
    def _select_mutated(self, parents: list[int], ws: Workspace) -> list[Genome]:
        # TODO: mutations should be based on constraints

        kids_mutated = [None] * self.mutation_size   # Initialization
        for i in range(len(parents)):
            # Mutate kid
            kid = self.population.genomes[parents[i]].mutate_genome(self.mutation_rate, ws)

            # Save to list
            kids_mutated[i] = kid

        return kids_mutated