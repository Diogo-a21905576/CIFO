from operator import attrgetter
from random import uniform, choice

def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """    

    # Calculate total fitness with adjustments for minimization and zero fitness cases
    total_fitness = sum(1/(i.fitness if i.fitness != 0 else 0.1) for i in population)

    # Generate a random number in the range [0, total_fitness)
    spin = uniform(0, total_fitness)
    position = 0

    # Iterate through the population to find the selected individual
    for individual in population:
        position += 1/(individual.fitness if individual.fitness != 0 else 0.1)
        if position > spin:
            return individual
    

    for individual in population:
        if individual.fitness == 0:
            position += 1/0.1
        else:
            position += 1/individual.fitness
        if position > spin:
            return individual



def tournament_sel(population,  tour_size=4):
    tournament = [choice(population.individuals) for _ in range(tour_size)]
    return min(tournament, key=attrgetter("fitness"))