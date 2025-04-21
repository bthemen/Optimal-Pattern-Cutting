# Import libraries
import random
import numpy as np

## Parameters
# Genetic algorithm parameters
POPULATION_SIZE = 100   # Population per generation
GENOME_LENGTH   = 20    # Number of design variables per genome
GENERATIONS     = 200   # Number of generations in evolution
ELITE_SIZE      = 5     # Number of elite genomes to be carried over
PARENT_SIZE     = 20    # Number of parents for crossover
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

# Select parents
def select_parent(expectation, parent_size):
    # Return indices of parents chosen for crossover mutation

    # Create a dart wheel based on fit genome probabilities
    wheel = np.cumsum(expectation) / parent_size

    # Add genome as parent if random number lands in its roulette slot
    parents = np.zeros(parent_size)
    for i in range(parent_size):
        r = random.random() # Random value between 0 and 1
        for j in range(POPULATION_SIZE):
            if r < wheel[j]:
                parents[i] = j
                break

    return parents
        
pop = init_population(POPULATION_SIZE, GENOME_LENGTH)
fitness_values = []
for individual in pop:
    fitness_values.append(fitness(individual))
expectation = fitness_scaling(fitness_values, PARENT_SIZE)
parents = select_parent(expectation, PARENT_SIZE)