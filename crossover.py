from random import choice, randint, random
from charles import Individual

def single_point_xo(parent1, parent2):
    #exchange portions of the schedule between parents, potentially creating new schedules that inherit beneficial arrangements from both parents.
    """Implementation of single point crossover.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_point = randint(1, len(parent1)-2)
    offspring1 = parent1[:xo_point] + parent2[xo_point:]
    offspring2 = parent2[:xo_point] + parent1[xo_point:]
    return offspring1, offspring2



def uniform_xo(p1, p2):
    """
    Perform crossover by randomly selecting each gene from either parent with equal probability.

    Parameters:
        p1 (list): parent 1
        p2 (list): parent 2
    Returns:
        tuple: Two offspring resulting from crossover
    """
    offspring1 = []
    offspring2 = []

    for gene1, gene2 in zip(p1, p2):
        if random() < 0.5:
            #Select gene from parent 1
            offspring1.append(gene1)
            offspring2.append(gene2)
        else:
            #Select gene from parent 2
            offspring1.append(gene2)
            offspring2.append(gene1)

    return offspring1, offspring2



def cycle_xo(p1, p2):
    """Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    offspring1 = Individual(representation=p1.representation[:])
    offspring2 = Individual(representation=p2.representation[:])

    #Create a dictionary to map class objects to their indices
    p1_indices = {class_obj: i for i, class_obj in enumerate(p1.representation)}
    p2_indices = {class_obj: i for i, class_obj in enumerate(p2.representation)}

    # Create a list to track which attributes have been swapped
    swapped = [False] * len(p1.representation)

    #Iterate over each attribute
    for i in range(len(p1.representation)):
        if not swapped[i]:
            #Start a new cycle
            cycle_start = i
            while not swapped[i]:
                #Swap attributes between parents
                offspring1.representation[i], offspring2.representation[i] = offspring2.representation[i], offspring1.representation[i]                
                swapped[i] = True
                #Find the index of the attribute in the other parent
                idx = p1_indices.get(offspring2.representation[i], None)
                i = idx
        
            while i != cycle_start:
                #Swap attributes between parents
                offspring1.representation[i], offspring2.representation[i] = offspring2.representation[i], offspring1.representation[i]                
                swapped[i] = True
                #Find the index of the attribute in the other parent
                idx = p1_indices.get(offspring2.representation[i], None)
                i = idx
        return offspring1, offspring2



def abc(p1, p2):
    """
    Attribute-Based Crossover. Randomly selects a number of changes in attributes, 
    between 1/4 and 3/4 of all attributes. Then, it checks if the attribute to be 
    changed has not yet been changed in this iteration and performs the swap.
    Parameters:
        p1(class): parent 1
        p2(class): parent 2
    Returns:
        2 objects class Individual: offspring 1 and offspring 2
    """
    offspring1 = p1[:]
    offspring2 = p2[:]
    
    sizeInd = len(p1)
    numAtrr = len(vars(p1[0]))
    num_attribute_exchanges = randint(int((sizeInd*numAtrr) * (1/4)) - 1, (int((sizeInd*numAtrr) * (3/4)) - 1))
    n = 0

    #Save attributes already changed to prevent repetition
    changed_attributes = []

    #Randomly selects attributes to exchange between objects
    while n < num_attribute_exchanges:
        object_index = randint(0, len(p1) - 1)
        attribute_to_exchange = choice(list(vars(p1[object_index]).keys())) 

        if (object_index,attribute_to_exchange) not in changed_attributes:
            changed_attributes.append((object_index,attribute_to_exchange))
            n += 1

            geneP1 = p1[object_index]
            geneP2 = p2[object_index]
            geneO1 = offspring1[object_index]
            geneO2 = offspring2[object_index]

            temp = geneP1.get_attribute(attribute_to_exchange)
            geneO1.set_attribute(attribute_to_exchange, geneP2.get_attribute(attribute_to_exchange))
            geneO2.set_attribute(attribute_to_exchange, temp)

    return offspring1, offspring2



