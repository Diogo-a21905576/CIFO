from random import choice, randint, sample
from charles import Class  
from data import simpleData  

def binary_mutation(individual, data=simpleData):
    """
    Performs a mutation on the attributes of a class within a timetable individual, changing it to a randomly selected value.
    
    Parameters:
        individual (list): The timetable individual to mutate, represented as a list of classes.
        data (dict): The data used for mutation.
        
    Returns:
        list: The mutated timetable individual.
    """
    #Randomly select a class and attribute index for mutation
    mut_index_class = randint(0, len(individual) - 1)
    mut_index_attr = randint(0, len(individual[0]) - 1)

    #Retrieve the attributes of the selected class
    class_attributes = list(vars(individual[mut_index_class]).keys())
    #Select an attribute to mutate
    attribute_to_change = class_attributes[mut_index_attr]
    #Randomly choose a new value for the attribute
    new_attribute_value = choice(data[attribute_to_change])

    #Ensure the new attribute value is different from the current value
    while new_attribute_value == individual[mut_index_class].get_attribute(attribute_to_change):
        new_attribute_value = choice(data[attribute_to_change])

    #Set the new attribute value
    individual[mut_index_class].set_attribute(attribute_to_change, new_attribute_value)

    return individual


    
def swap_mutation(individual):
    """
    Performs a timetable mutation by exchanging attributes between classes in an individual.
    
    Parameters:
        individual (list): The timetable individual to mutate, represented as a list of classes.
        
    Returns:
        list: The mutated timetable individual.
    """
    #Randomly select two class indexes for mutation
    mut_indexes_class = sample(range(len(individual)), 2)

    #Retrieve the classes to exchange attributes
    class1 = individual[mut_indexes_class[0]]
    class2 = individual[mut_indexes_class[1]]

    #Retrieve the attributes of the classes
    attr_class1 = vars(class1)
    attr_class2 = vars(class2)

    #Select attributes to exchange
    attributes_to_exchange = sample(list(attr_class1.keys()), len(attr_class1) // 2)

    #Exchange the selected attributes
    for attribute in attributes_to_exchange:
        temp = attr_class1[attribute]
        attr_class1[attribute] = attr_class2[attribute]
        attr_class2[attribute] = temp

    return individual




def inversion_mutation(individual, data=simpleData):
    """Inversion mutation for a GA individual. Reverts a portion of the representation.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    #Select a random class index to mutate
    mut_index_class = randint(0, len(individual) - 1)

    #Randomly select each attribute
    random_day = choice(data['day'])
    random_timeslot = choice(data['timeslot'])
    random_classroom = choice(data['classroom'])
    random_subject = choice(data['subject'])
    random_teacher = choice(data['teacher'])
    random_group = choice(data['group'])


    #Create a new class with random attributes and replace the existing in a random index
    individual[mut_index_class] = Class(day=random_day, timeslot=random_timeslot, subject=random_subject, group=random_group, classroom=random_classroom, teacher=random_teacher)
    return individual