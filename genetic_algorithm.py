# Import libraries
import random
import numpy as np

## Parameters
# Genetic algorithm parameters
POPULATION_SIZE = 100   # Population per generation
GENOME_LENGTH   = 20    # Number of design variables per genome
GENERATIONS     = 200   # Number of generations in evolution
ELITE_SIZE      = 5     # Number of elite genomes to be carried over
CROSSOVER_RATE  = 0.7   # Percentage chance of a genome crossover
MUTATION_RATE   = 0.01  # Percentage chance of a genome mutation

# Workspace parameters
WS_WIDTH        = 1300  # Workspace width [mm]
WS_HEIGHT       = 2500  # Workspace height [mm]
WS_STEP         = 10    # Step size of workspace grid [mm]
WS_TOLERANCE    = 10    # Tolerance workspace overlap [mm]

## Define Genetic Algorithm functions
# Create a random genome
def random_genome(length):
    # Create random values for the x and y coordinates of the pattern piece centers
    random_value_x = [WS_WIDTH * random.uniform(0, 1) for _ in range(length // 2)]
    random_value_y = [WS_HEIGHT * random.uniform(0, 1) for _ in range(length // 2)]
    # TODO: add rotation of pattern pieces

    # Fill genome
    current_genome = []
    for x, y in zip(random_value_x, random_value_y):
        current_genome.extend([x, y])

    return current_genome

# Create initial population
def init_population(population_size, genome_length):

    # TODO: add initialization through provided SVG

    # Random genome population
    population = [random_genome(genome_length) for _ in range(population_size)]

    return population

# Calculate fitness
def fitness(genome):
    # Index spacing
    spacing = 2

    # TODO: take ultima from bounds method
    # x direction
    x_min = min(genome[1::spacing]) # Minimum x value
    x_max = max(genome[1::spacing]) # Maximum x value

    # y direction
    y_min = min(genome[2::spacing]) # Minimum y value
    y_max = max(genome[2::spacing]) # Maximum y value

    # Calculate effective area
    effective_area = (x_max - x_min) * (y_max - y_min)

    return effective_area

# Calculate fitness scaling
def fitness_scaling(fitness_values, parents_number):
    # Get the indices that would sort the list
    sorted_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i])

    # Create expectation values
    size = len(fitness_values)
    expectation = np.zeros(size)
    expectation[sorted_indices] = 1 / np.sqrt(np.arange(1, size + 1))

    # Scale with number of parents
    expectation = parents_number * expectation / sum(expectation)

    return expectation

# Select parent
def select_parent(population, fitness_values):
    ## TODO: does not work for this use case, try @selectionroulette as in MATLAB
    total_fitness = sum(fitness_values)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, fitness_value in zip(population, fitness_values):
        current += fitness_value
        if current > pick:
            return individual
        
pop = init_population(POPULATION_SIZE, GENOME_LENGTH)
fitness_values = []
for individual in pop:
    fitness_values.append(fitness(individual))
scaling = fitness_scaling(fitness_values, 2)