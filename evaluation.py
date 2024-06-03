from charles import Population
from data import simpleData
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
import pandas as pd


def evaluateCombination(gens, select, mutate, crossover, mut_prob, xo_prob, elitism, pop_size=100, data=simpleData):
    """
    Evaluates a genetic algorithm combination by running the evolution process.

    Parameters:
        gens (int): Number of generations to run the algorithm.
        select (function): Function to select parents.
        mutate (function): Function to mutate individuals.
        crossover (function): Function to perform crossover between parents.
        mut_prob (int): Probability of mutation.
        xo_prob (int): Probability of crossover.
        elitism (bool): Whether to preserve the best individuals in the population.
        pop_size (int, optional): Size of the population. Defaults to 100.
        data (dict, optional): Data dictionary specifying problem parameters. Defaults to data1.

    Returns:
        pd.Series: Series containing fitness values for each generation.
    """
    pop = Population(
        size=pop_size,
        sol_size=len(data['group']) * len(data['subject']) * data['classesPerSubject'],
        classrooms=data['classroom'],
        groups=data['group'],
        subjects=data['subject'],
        timeslots=data['timeslot'],
        days=data['day'],
        teachers=data['teacher']
    )

    #Evolve the population using the provided parameters
    fitness_values = pop.evolve(
        gens=gens,
        select=select,
        mutate=mutate,
        crossover=crossover,
        mut_prob=mut_prob,
        xo_prob=xo_prob,
        elitism=elitism,
        data=data
    )
    # Convert the fitness values to a pandas Series
    fitness_series = pd.Series(fitness_values)
    best_individual = min(pop, key=lambda x: x.fitness)

    return fitness_series, deepcopy(best_individual)



#create a plot that visualizes the results of different combinations of a genetic algorithm, showing how they perform over generations.
def combinationsGraph(folderToShow):
    """
    Creates a plot with each combination, for each type of data and fitness function.
    Parameters:
        folderToShow (str): folder path where to place the plot of combinations.
    """
    folder_path = folderToShow
    abf_data = []
    std = []
    fileNames = []

    # Checks for each .csv file in the path provided as an input
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            # Add the name of each file found in the folder to a list
            fileNames.append(file_name)
            file_path = os.path.join(folder_path, file_name)
            # Reads the csv in order to retrieve the data needed to create the plot
            df = pd.read_csv(file_path)
            # Check the column with the name 'ABF' and adds the values to the list abf_data
            abf_data.append(df['ABF'].values) 
            # Perform the same thing as above to the list std
            std.append(df['StdDev'].values)

    # To create the x-axis, with the number of generations       
    generations = np.arange(len(abf_data[0]))

    # Creating the plot for each combination possible
    plt.figure(figsize=(12, 8))  # Increased figure size for better readability
    color_map = plt.get_cmap('tab20')  # Using a colormap with more color options

    for combination in range(len(abf_data)):
        color = color_map(combination / len(abf_data))
        plt.plot(generations, abf_data[combination], label=fileNames[combination].replace(".csv", ""),
                 linestyle='-', marker='o', color=color)  # Different line style and marker
        # Adding to the plot the standard deviations, in order to later analyze the statistical significance
        plt.fill_between(generations, abf_data[combination] - std[combination], abf_data[combination] + std[combination],
                         color=color, alpha=0.2)
    
    plt.title('ABF Results for Each Combination', fontsize=16, weight='bold')
    plt.xlabel('Generations', fontsize=14)
    plt.ylabel('Average best fitness', fontsize=14)
    plt.legend(loc='best', fontsize='medium')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Saving the plot in a .jpeg image in order to preserve it when the run ends
    plot = folderToShow.rstrip('/').split('/')[-1]
    namePlot = f"{plot}.jpeg"
    plt.savefig(os.path.join(folderToShow, namePlot), format='jpeg', dpi=300)
    plt.show()




# Function to project the timetable
def create_visual_timetable(best_individual, data, folderToShow):
    # Define the correct order of the days
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', "Saturday"]  # Add more if needed
    timeslots = sorted(map(int, data['timeslot']))  # Ensure timeslots are sorted

    # Create a MultiIndex for the columns and rows
    index = pd.MultiIndex.from_product([data['timeslot'], days_of_week], names=['Timeslot', 'Day'])
    columns = ['Subject', 'Group', 'Teacher', 'Classroom']

    # Initialize the DataFrame with the MultiIndex
    timetable = pd.DataFrame(index=index, columns=columns)

    # Fill the timetable DataFrame
    for class_block in best_individual.representation:
        day = class_block.get_day()
        timeslot = class_block.get_timeslot()
        classroom = class_block.get_classroom()
        subject = class_block.get_subject()
        group = class_block.get_group()
        teacher = class_block.get_teacher()

        # Populate the timetable
        timetable.loc[(timeslot, day)] = [subject, group, teacher, classroom]

    # Reset index to have timeslots and days as regular columns
    timetable.reset_index(inplace=True)

    # Ensure the 'Day' column is a categorical type with the correct order
    timetable['Day'] = pd.Categorical(timetable['Day'], categories=days_of_week, ordered=True)

    # Pivot the table for better visualization
    timetable_pivot = timetable.pivot(index='Timeslot', columns='Day', values=['Subject', 'Group', 'Teacher', 'Classroom'])

    # Ensure timeslots are treated as integers and sort the index numerically
    timetable_pivot.index = timetable_pivot.index.astype(int)
    timetable_pivot.sort_index(level='Timeslot', inplace=True)

    # Reorder columns by days of the week
    timetable_pivot = timetable_pivot.reindex(columns=pd.MultiIndex.from_product([['Subject', 'Group', 'Teacher', 'Classroom'], days_of_week]))

    # Create a formatted string for each cell
    def format_cell(subject, group, teacher, classroom):
        if pd.isnull(subject):
            return ''
        return f"{subject} ({group})\n{teacher}\nRoom: {classroom}"

    # Apply the formatting function to each cell
    for day in days_of_week:
        timetable_pivot[('Formatted', day)] = timetable_pivot.apply(
            lambda row: format_cell(row[('Subject', day)], row[('Group', day)], row[('Teacher', day)], row[('Classroom', day)]),
            axis=1
        )

    # Extract the formatted timetable
    formatted_timetable = timetable_pivot['Formatted']

    # Plot the timetable using matplotlib
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.axis('off')
    ax.axis('tight')

    # Create the table
    table = ax.table(cellText=formatted_timetable.values, 
                     colLabels=formatted_timetable.columns, 
                     rowLabels=formatted_timetable.index, 
                     cellLoc='center', 
                     loc='center')

    # Adjust font size for readability
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Adjust column widths for better visibility
    for key, cell in table.get_celld().items():
        cell.set_height(0.1)
        cell.set_width(0.2)

    # Save the timetable visualization as a PNG image
    plot_name = folderToShow.rstrip('/').split('/')[-1] + '_timetable.png'
    plt.savefig(os.path.join(folderToShow, plot_name), format='png', dpi=300)
    plt.show()




