# Local application imports
import init_population
import fitness_scaling
import fitness
import crossover
import elite
import mutate
import select_parent

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

## Initialize population
population = init_population(GENOME_LENGTH, WS_WIDTH, WS_HEIGHT, POPULATION_SIZE)

## Loop through generations
for generation in range(GENERATIONS):
    # Calculate fitness values
    fitness_values = [fitness(genome) for genome in population]
    top_fitness = min(fitness_values)

    # Output generation score
    print(f"Generation {generation}: best fitness {top_fitness}")

    # Calculate expectation values for parents
    expectation = fitness_scaling(fitness_values, POPULATION_SIZE, PARENT_SIZE)

    # Select parents
    parents = select_parent(expectation, POPULATION_SIZE, PARENT_SIZE)

    # Create kids
    kids_elite = elite(population, fitness_values, POPULATION_SIZE, ELITE_SIZE) # Elites
    kids_crossover = crossover(population, parents[:(2 * CROSSOVER_SIZE)], CROSSOVER_RATIO) # Crossover
    kids_mutated = mutate(population, parents[(2 * CROSSOVER_SIZE):], GENOME_LENGTH, WS_WIDTH, WS_HEIGHT, MUTATION_RATE)  # Mutations

    # Make the new population
    population = kids_elite + kids_crossover + kids_mutated

# Calculate best fitness
final_fitness = [fitness(genome) for genome in population]
best_index = final_fitness.index(min(final_fitness))
best_solution = population[best_index]
best_fitness = final_fitness[best_index]

# Print results
print(f"Best solution [{best_index}, fitness: {best_fitness}]: {best_solution}")