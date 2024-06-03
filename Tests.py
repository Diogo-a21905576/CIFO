from timetable import timetable, parameters_with_no_elitism, parameters_base_elitism, parameters_base_population_improve, parameters_base_probabilities_improve, parameters_base_population_probabilities_improve
from data import simpleData, advancedData


''' First of all, we started by testing our algorithm with no elitism.
#Analyzing the graph, it can be conclude that overall it returns bad results.
So elitism was implemented in all attempts. '''
#timetableScheduling(30, 100, parameters_with_no_elitism, 'NoElitism', 'None', simpleData, fitness=1)

'''To gain insights over our algorithm, we then checked the performance for each type of data with each fitnes's function'''
#timetable(30, 100, parameters_base_elitism, 'Testing', 'None', simpleData, fitness=1)
#timetable(30, 100, parameters_base_elitism, 'Testing', 'None', simpleData, fitness=2)
#timetable(30, 100, parameters_base_elitism, 'Testing', 'None', simpleData, fitness=3)
#timetable(30, 100, parameters_base_elitism, 'Testing', 'None', advancedData, fitness=1)

#(here we decided to remove abc and cycle crossover since it has consistently showed bad results and it is computationally expensive running too many combinations)
#timetable(30, 100, parameters_base_elitism, 'Testing', 'None', advancedData, fitness=2)
#timetable(30, 100, parameters_base_elitism, 'Testing', 'None', advancedData, fitness=3)
'''Here we conclude that the most effective combination is tournament selection along with uniform crossover and binary mutation.'''


'''Once we had an ideia how our algorithm performs, we tried to improve results using different methods:'''
'''- Increase population'''
#timetable(30, 200, parameters_base_population_improve, 'Improving', 'Population', advancedData, fitness=1)
#timetable(30, 200, parameters_base_population_improve, 'Improving', 'Population',  advancedData, fitness=2)
#timetable(30, 200, parameters_base_population_improve, 'Improving', 'Population',  advancedData, fitness=3)
'''This approach has slightly improved results but we conclude that population size alone was not sufficient to address the issues at hand'''


'''- Change crossover and mutation probabilities'''
#timetable(30, 100, parameters_base_probabilities_improve, 'Improving', 'Probabilities', advancedData, fitness=1)
#timetable(30, 100, parameters_base_probabilities_improve, 'Improving', 'Probabilities', advancedData, fitness=2)
#timetable(30, 100, parameters_base_probabilities_improve, 'Improving', 'Probabilities', advancedData, fitness=3)
'''This approach worsened the results, so it was discarded'''

 
'''- Increase population and number of runs, and change crossover and mutation probabilities to check the impact of all the changes made before'''
#timetable(40, 200, parameters_base_population_probabilities_improve, 'Improving', 'Population_Probabilities_Runs', advancedData, fitness=1)
#timetable(40, 200, parameters_base_population_probabilities_improve, 'Improving', 'Population_Probabilities_Runs', advancedData, fitness=2)
#timetable(40, 200, parameters_base_population_probabilities_improve, 'Improving', 'Population_Probabilities_Runs', advancedData, fitness=3)
'''This approach did not improve results and is too computationally expensive to be worthwhile.'''







