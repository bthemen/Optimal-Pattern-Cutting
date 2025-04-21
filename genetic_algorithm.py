# Import libraries
import random
import numpy as np

## Parameters
# Genetic algorithm parameters (set)
POPULATION_SIZE = 100   # Population per generation
GENOME_LENGTH   = 20    # Number of design variables per genome
GENERATIONS     = 200   # Number of generations in evolution
ELITE_SIZE      = 6     # Number of elite kids
CROSSOVER_RATE  = 0.7   # Percentage chance of a genome crossover
CROSSOVER_RATIO = 0.5   # Ratio of shared genomes between parent 1 and parent 2
MUTATION_RATE   = 0.01  # Percentage chance of a genome mutation

# Genetic algorithm parameters (derived)
CROSSOVER_SIZE  = round(CROSSOVER_RATE * (POPULATION_SIZE - ELITE_SIZE))    # Number of crossover kids
MUTATION_SIZE   = POPULATION_SIZE - ELITE_SIZE - CROSSOVER_SIZE             # Number of mutated kids
PARENT_SIZE     = 2 * CROSSOVER_SIZE + MUTATION_SIZE                        # Number of parents

# Workspace parameters
WS_WIDTH        = 1300  # Workspace width [mm]
WS_HEIGHT       = 2500  # Workspace height [mm]
WS_STEP         = 10    # Step size of workspace grid [mm]
WS_TOLERANCE    = 10    # Tolerance workspace overlap [mm]

## Define Genetic Algorithm functions
# Create a random genome
def random_genome():
    # Create random values for the x and y coordinates of the pattern piece centers
    random_value_x = WS_WIDTH * np.random.uniform(0, 1, size=GENOME_LENGTH // 2)
    random_value_y = WS_HEIGHT * np.random.uniform(0, 1, size=GENOME_LENGTH // 2)
    # TODO: add rotation of pattern pieces

    # Fill genome
    current_genome = np.zeros([1, GENOME_LENGTH])
    for i in range(GENOME_LENGTH // 2):
        current_genome[0, 2 * i]       = random_value_x[i]
        current_genome[0, 2 * i + 1]   = random_value_y[i]

    return current_genome

# Create initial population
def init_population():

    # TODO: add initialization through provided SVG

    # Random genome population
    population = [random_genome() for _ in range(POPULATION_SIZE)]

    return population

# Calculate fitness
def fitness(genome):
    # Index spacing
    spacing = 2

    # TODO: take ultima from bounds method
    # x direction
    x_min = min(genome[0, 1::spacing]) # Minimum x value
    x_max = max(genome[0, 1::spacing]) # Maximum x value

    # y direction
    y_min = min(genome[0, 2::spacing]) # Minimum y value
    y_max = max(genome[0, 2::spacing]) # Maximum y value

    # Calculate effective area
    effective_area = (x_max - x_min) * (y_max - y_min)

    return effective_area

# Calculate fitness scaling
def fitness_scaling(fitness_values):
    # Get the indices that would sort the list
    sorted_indices = sorted(range(POPULATION_SIZE), key=lambda i: fitness_values[i])

    # Create expectation values
    size = POPULATION_SIZE
    expectation = np.zeros(size)
    expectation[sorted_indices] = 1 / np.sqrt(np.arange(1, size + 1))

    # Scale with number of parents
    expectation = PARENT_SIZE * expectation / sum(expectation)

    return expectation

# Select parents
def select_parent(expectation):
    # Return indices of parents chosen for crossover mutation

    # Create a dart wheel based on fit genome probabilities
    wheel = np.cumsum(expectation) / PARENT_SIZE

    # Add genome as parent if random number lands in its roulette slot
    parents = np.zeros(PARENT_SIZE, dtype=int)
    for i in range(PARENT_SIZE):
        r = random.random() # Random value between 0 and 1
        for j in range(POPULATION_SIZE):
            if r < wheel[j]:
                parents[i] = j
                break

    # Shuffle the parents
    random.shuffle(parents)

    return parents
        
# Select elite kids
def select_kids_elite(genomes, fitness_values):
    # Get the indices that would sort the population by most fit
    sorted_indices = sorted(range(POPULATION_SIZE), key=lambda i: fitness_values[i])

    # Select elite kids
    kids_elite = [genomes[i] for i in sorted_indices[0:ELITE_SIZE]]

    return kids_elite
    
# Create crossover kids
def select_kids_crossover(genomes, parents):
    # Get number of kids
    kids_size = len(parents) // 2

    # Initialization
    kids_crossover = []

    for i in range(kids_size):
        # Get parents
        parent1 = genomes[parents[2 * i]]
        parent2 = genomes[parents[2 * i + 1]]

        # Get scaling factor
        scale = CROSSOVER_RATIO * random.random()
        delta = scale * (parent2 - parent1)

        # Create kid
        kids_crossover.append(parent1 + delta)

    return kids_crossover

# Create mutated kids
def select_kids_mutate(genomes, parents):
    kids_mutated = []   # Initialization
    for i in range(len(parents)):
        # Get kid
        kid = genomes[parents[i]]

        # Find mutation points
        r = np.random.rand(1, GENOME_LENGTH)
        mutation_points = np.where(r < MUTATION_RATE)   # Mutate genes that are below the threshold

        # Create new genome
        mutated_genome = random_genome()

        # Create mutated kid
        kid[mutation_points] = mutated_genome[mutation_points]

        # Save to list
        kids_mutated.append(kid)

    return kids_mutated


pop = init_population()
fitness_values = []
for individual in pop:
    fitness_values.append(fitness(individual))
expectation = fitness_scaling(fitness_values)
parents = select_parent(expectation)
kids_elite = select_kids_elite(pop, fitness_values)
kids_crossover = select_kids_crossover(pop, parents[:(2 * CROSSOVER_SIZE)])
kids_mutated = select_kids_mutate(pop, parents[(2 * CROSSOVER_SIZE):])

new_pop = kids_elite + kids_crossover + kids_mutated

exit(1)