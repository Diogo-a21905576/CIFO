from charles import Individual
from selection import fps,tournament_sel
from crossover import single_point_xo, uniform_xo, cycle_xo, abc
from mutation import binary_mutation, swap_mutation, inversion_mutation
from tsp import get_fitness1, get_fitness2, get_fitness3
from search import evaluate_genetic_algorithm
from data import advancedData, simpleData


parameters_with_no_elitism = {
    'select': [fps,tournament_sel],
    'crossover': [single_point_xo, uniform_xo, cycle_xo, abc],
    'xo_prob': [0.9],
    'mutate': [binary_mutation, swap_mutation, inversion_mutation],
    'mut_prob': [0.05],
    'elitism': [False],
    'population': [100]
}

parameters_base_elitism = {
    'select': [fps,tournament_sel],
    'crossover': [single_point_xo, uniform_xo],
    'xo_prob': [0.9],
    'mutate': [binary_mutation, swap_mutation, inversion_mutation],
    'mut_prob': [0.05],
    'elitism': [True],
    'population': [100]
}

#use of elitism for improving phase since it has consistently improved the results
parameters_base_population_improve = {
    'select': [fps,tournament_sel],
    'crossover': [single_point_xo, uniform_xo],
    'xo_prob': [0.9],
    'mutate': [binary_mutation, swap_mutation, inversion_mutation],
    'mut_prob': [0.05],
    'elitism': [True],
    'population': [200]
}

parameters_base_probabilities_improve = {
    'select': [fps,tournament_sel],
    'crossover': [single_point_xo, uniform_xo],
    'xo_prob': [0.8],  
    'mutate': [binary_mutation, swap_mutation, inversion_mutation],
    'mut_prob': [0.2], 
    'elitism': [True],
    'population': [100]
}

parameters_base_population_probabilities_improve = {
    'select': [fps,tournament_sel],
    'crossover': [single_point_xo, uniform_xo],
    'xo_prob': [0.8],  # crossover rate between 0.8 and 1.0
     'mutate': [binary_mutation, swap_mutation, inversion_mutation],
    'mut_prob': [0.2], # mutation rate between 0 and 0.2
    'elitism': [True],
    'population': [200]
}


def select_fitness_function(fitness, data):
    if fitness == 1:
        return lambda self: get_fitness1(self, data)
    elif fitness == 2:
        return lambda self: get_fitness2(self, data)
    elif fitness == 3:
        return lambda self: get_fitness3(self, data)
 


def timetable(nRuns, nGens, parameters, phase, improvement, data=simpleData, fitness=1):
    """
    In this function, the parameters we want to test will be passed and files will be saved with 
    the output in the desired folder
    Parameters:
        nRuns(int): number of runs to perform for each configuration
        nGens(int): number of generations to perform for each configuration
        parameters(Dictionary): parameters to use to run the configuration
        phase(str): 'None', for the case of testing the elistism True vs False;
                    'Testing', to test base parameters for each type of data 
                    (simple and complex) with each fitness function 1, 2 and 3;
                    'Improving', trying to change hyperparemeters to improve results from 'Testing'.
        improvement(str): Type of improvement 'None', for not being in this phase;
                          'Population', improvement in the number of individuals in the Population;
                          'Probabilites', improvement in the probabilities of mutation and crossover;
                          'Population_Probabilies_Runs', improvement in the number of individuals in the Population, 
                           probabilities of mutation and crossover and number of runs performed.
        data(Dictionary): The data used (simple data default)
        fitness(int): fitness function to use
    """
    #Select fitness function
    Individual.get_fitness = select_fitness_function(fitness, data)

    # Get folder name for storing files
    fitness_folder = str(fitness)
    data_folder = [key for key, val in globals().items() if val == data]
    folder = str(data_folder[0]) + "_" + 'fitness' + fitness_folder

    if phase == 'Testing':
        folderToStore = phase+'/'+folder
    elif phase == 'NoElitism':
        folderToStore = phase
    elif phase == 'Improving':
        folderToStore = phase+'/'+improvement+'/'+folder

    best_parameters = evaluate_genetic_algorithm(nRuns, nGens, parameters, folderToStore, data)
    