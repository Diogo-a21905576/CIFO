from evaluation import evaluateCombination, combinationsGraph
from sklearn.model_selection import ParameterGrid
import pandas as pd
import os


def evaluate_genetic_algorithm(nRuns, nGens, configDict, folderToStore, data):
    """
    Runs the genetic algorithm and calculates values for plotting.

    Parameters:
        nRuns (int): Number of runs for the algorithm.
        nGens (int): Number of generations for the algorithm.
        configDict (dict): Parameters for configuring possible combinations.
        folderToStore (str): Folder path to store the CSV file.
        data (dict): Type of data to use, simple or complex.

    Returns:
        tuple: Best combination and its average best fitness.
    """
    #Generate a grid of hyperparameter combinations
    parameters = list(ParameterGrid(configDict))
    print("Number of combinations to be tested:", len(parameters))

    best_ABF = float('inf')
    best_combination = None

    #Loop through each parameter combination
    for param_combination in range(len(parameters)):
        select = parameters[param_combination]['select']
        crossover = parameters[param_combination]['crossover']
        xo_prob = parameters[param_combination]['xo_prob']
        mutate = parameters[param_combination]['mutate']
        mut_prob = parameters[param_combination]['mut_prob']
        elitism = parameters[param_combination]['elitism']
        populationSize = parameters[param_combination]['population']

        print("Testing combination:", parameters[param_combination])
        combination = pd.DataFrame()
        combination['Generations'] = pd.Series([i for i in range(nGens)])

        for r in range(nRuns):
            print("------------------------------------")
            print("Run combination", r)
            print("------------------------------------")
            runs, _ = evaluateCombination(nGens, select, mutate, crossover, mut_prob, xo_prob, elitism, populationSize, data)
            combination[f'Run{r}'] = runs

        #calculate the average best fitness and standard deviation
        combination['ABF'] = combination.iloc[:, 1:].mean(axis=1).round(3)
        combination['StdDev'] = combination.iloc[:, 1:].std(axis=1).round(3)

        # Save the results into a CSV file
        if 'Testing' in folderToStore:
            folder = 'Results/'+folderToStore+'/'
            os.makedirs(folder, exist_ok=True)
            combination.to_csv(folder+str(select.__name__)+'-'+str(crossover.__name__)+'-'+str(mutate.__name__)+'.csv', index=False)

        elif 'NoElitism' in folderToStore:
            folder = 'Results/'+folderToStore+'/'
            os.makedirs(folder, exist_ok=True)
            combination.to_csv(folder+str(select.__name__)+'-'+str(crossover.__name__)+'-'+str(mutate.__name__)+'.csv', index=False)

        elif 'Improving' in folderToStore:
            folder = 'Results/'+folderToStore+'/'
            os.makedirs(folder, exist_ok=True)

            #The improving is in the number of population individuals
            if 'Population' in folderToStore:
                combination.to_csv(folder+str(select.__name__)+'-'+str(crossover.__name__)+'-'+str(mutate.__name__)+'-'+str(populationSize)+'.csv', index=False)
                
            #The improving is in the probabilities of crossover and mutation
            elif 'Probabilities' in folder:
                combination.to_csv(folder+str(select.__name__)+'-'+str(crossover.__name__)+'-'+str(mutate.__name__)+'-'+str('prob_mut_xo')+'.csv', index=False)
                
            #The improving is in the number of population individuals, probabilities of crossover and mutation and number of runs
            elif 'Population_Probabilities_Runs' in folder:
                combination.to_csv(folder+str(select.__name__)+'-'+str(crossover.__name__)+'-'+str(mutate.__name__)+'-'+str('Population_Probabilities_Runs')+'.csv', index=False)

        
    #Calculate the mean of average best fitness and update best combination if applicable
    mean_ABF = combination['ABF'].mean()
    if mean_ABF < best_ABF:
        best_ABF = mean_ABF
        best_combination = param_combination

    # Generate comparison plots for combinations
    combinationsGraph(folder)
    print(f"Best Combination: {best_combination} with ABF: {best_ABF}")
    return best_combination, best_ABF
