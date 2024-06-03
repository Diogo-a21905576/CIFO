from charles import Individual
from selection import tournament_sel
from crossover import uniform_xo
from mutation import binary_mutation
from timetable import select_fitness_function
from data import simpleData, advancedData
from evaluation import evaluateCombination, create_visual_timetable, combinationsGraph
from copy import deepcopy
import matplotlib.pyplot as plt
import pandas as pd
import os



'''Finally here we are testing the performance of our algorithm with the best combination and the best parameters'''

best_parameters = {
    'select': [tournament_sel],
    'crossover': [uniform_xo],
    'xo_prob': [0.9],
    'mutate': [binary_mutation],
    'mut_prob': [0.05],
    'elitism': [True],
    'population': [200]
}

def timetableBestParamenters(nRuns, nGens, best_parameters, phase, improvement, data=simpleData, fitness=1):

    Individual.get_fitness = select_fitness_function(fitness, data)
    fitness_folder = str(fitness)
    data_folder = [key for key, val in globals().items() if val == data]
    folder = str(data_folder[0]) + "_" + 'fitness' + fitness_folder
    folderToStore = phase +'/'+folder

    best_ABF = float('inf')
    best_individual = None

    # Extract parameters from best_parameters
    select = best_parameters['select'][0]
    crossover = best_parameters['crossover'][0]
    xo_prob = best_parameters['xo_prob'][0]
    mutate = best_parameters['mutate'][0]
    mut_prob = best_parameters['mut_prob'][0]
    elitism = best_parameters['elitism'][0]
    populationSize = best_parameters['population'][0]

    combination = pd.DataFrame()
    combination['Generations'] = pd.Series([i for i in range(nGens)])

    for r in range(nRuns):
        print("------------------------------------")
        print("Run combination", r)
        print("------------------------------------")
        combination[f'Run{r}'], current_best_individual = evaluateCombination(nGens, select, mutate, crossover, mut_prob, xo_prob, elitism, populationSize, data)

        if current_best_individual.fitness < best_ABF:
            best_individual = deepcopy(current_best_individual)
            best_ABF = current_best_individual.fitness

        print("best_individual", best_individual)

    combination['ABF'] = combination.iloc[:, 1:].mean(axis=1).round(3)
    combination['StdDev'] = combination.iloc[:, 1:].std(axis=1).round(3)

    folder = 'Results/'+folderToStore+'/'
    os.makedirs(folder, exist_ok=True)
    combination.to_csv(folder+str(select.__name__)+'-'+str(crossover.__name__)+'-'+str(mutate.__name__)+'.csv', index=False)

    # Generate comparison plots for combinations
    combinationsGraph(folder)
    # Visualize the timetable before returning
    create_visual_timetable(best_individual, data, folder)
    

#timetableBestParamenters(30, 200, best_parameters, 'Best', 'None', simpleData, fitness=1)
#timetableBestParamenters(30, 200, best_parameters, 'Best', 'None', simpleData, fitness=2)
#timetableBestParamenters(30, 200, best_parameters, 'Best', 'None', simpleData, fitness=3)
#timetableBestParamenters(30, 200, best_parameters, 'Best', 'None', advancedData, fitness=1)
#timetableBestParamenters(30, 200, best_parameters, 'Best', 'None', advancedData, fitness=2)
#timetableBestParamenters(30, 200, best_parameters, 'Best', 'None', advancedData, fitness=3)









    

