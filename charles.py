from random import choice, random
from operator import attrgetter
from copy import deepcopy

class Class:
    def __init__(self, group, classroom, timeslot, day, subject, teacher):
        """
        Initiates a Class object
        Parameters:
            day(str): value of the day
            timeslot(str): value of the timeslot
            classroom(str): value of the classroom
            subject(str): value of the subject
            teacher(str): value of the teacher
            group(str): value of the group
        Returns:
            Object: Class object 
        """
        self.day = day
        self.timeslot = timeslot
        self.classroom = classroom
        self.subject = subject
        self.teacher = teacher
        self.group = group

    def get_attribute(self, attribute):
        """
        Check which kind of attribute to return from a Class object
        Parameters:
            attribute(str): type of attribute to return its value
        Returns:
            str: attribute value of the Class object 
        """
        return getattr(self, attribute)
    
    def get_day(self):
        return self.day
    
    def get_timeslot(self):
        return self.timeslot

    def get_classroom(self):
        return self.classroom
    
    def get_subject(self):
        return self.subject

    def get_teacher(self):
        return self.teacher

    def get_group(self):
        return self.group
    
    def set_attribute(self, attribute, new_attribute):
        """
        Sets the value of the specified attribute.
        Parameters:
            attribute (str): Attribute name.
            new_value (str): New value for the attribute.
        """
        if attribute == "day":
            self.day = new_attribute
        elif attribute == "timeslot":
            self.timeslot = new_attribute
        elif attribute == "classroom":
            self.classroom = new_attribute
        elif attribute == "subject":
            self.subject = new_attribute
        elif attribute == "teacher":
            self.teacher = new_attribute
        elif attribute == "group":
            self.group = new_attribute


    def __len__(self):
        """
        Returns the number of attributes of the Class object.
        Returns:
            int: Number of attributes.
        """
        return len(vars(self))

    def __repr__(self):
        """
        Returns a string representation of the Class object.
        Returns:
            str: String representation.
        """
        return f"Class: {self.day}, {self.timeslot}, {self.classroom}, {self.subject}, {self.group}, {self.teacher}"

class Individual:
    def __init__(self, representation=None, size=None, days=None, timeslots=None, subjects=None, groups=None, classrooms=None, teachers=None):
        """
        Initializes an Individual object.
        Parameters:
            representation (list): List of Class objects representing the individual.
            size (int): Number of classes in the individual's timetable.
            days (list): List of possible days.
            timeslots (list): List of possible timeslots.
            subjects (list): List of possible subjects.
            groups (list): List of possible groups.
            classrooms (list): List of possible classrooms.
            teachers (list): List of possible teachers.
        """
        if representation is None:
            # Create a new random representation if none is provided
            self.representation = [
                Class(choice(groups), choice(classrooms), choice(timeslots), choice(days), choice(subjects), choice(teachers))
                for _ in range(size)
            ]
        else:
            self.representation = representation
        self.fitness = self.get_fitness()  # Calculate fitness

    def get_fitness(self):
        raise Exception("You need to monkey patch the fitness function.")

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f" Fitness: {self.fitness}"

    def __iter__(self):
        return iter(self.representation)



class Population:
    def __init__(self, size, **kwargs):
        """
        Parameters:
            representation (list): List of Class objects representing the individual.
            size (int): Number of classes in the individual's timetable.
            days (list): List of possible days.
            timeslots (list): List of possible timeslots.
            subjects (list): List of possible subjects.
            groups (list): List of possible groups.
            classrooms (list): List of possible classrooms.
            teachers (list): List of possible teachers.
        Returns:
            Object: Population object 
        """
        self.size = size

        self.individuals = []

        for _ in range(size):
            self.individuals.append(
                Individual(                              
                    size=kwargs["sol_size"],
                    days=kwargs["days"],
                    subjects=kwargs["subjects"],
                    classrooms=kwargs["classrooms"],
                    groups=kwargs["groups"],
                    timeslots=kwargs["timeslots"],
                    teachers=kwargs["teachers"],
                )
            )
        

    def evolve(self, gens, xo_prob, mut_prob, select, mutate, crossover, elitism, data, sigma_share=1.0, alpha=1):       
        """
        Evolves the population over a specified number of generations.
        Parameters:
            gens (int): Number of generations.
            xo_prob (float): Crossover probability.
            mut_prob (float): Mutation probability.
            select (function): Selection function.
            mutate (function): Mutation function.
            crossover (function): Crossover function.
            elitism (bool): Whether to use elitism.
            data (dict): Additional data for mutation.
        Returns:
            list: Fitness values for each generation.
        """
        totalFitness = []  #To store fitness of each generation
        
        for i in range(gens):
            new_pop = []

            if elitism:
                #Preserve the best individual if elitism is enabled
                elite = deepcopy(min(self.individuals, key=attrgetter("fitness"))) 

            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self) #Select parents
                if random() < xo_prob:
                    offspring1, offspring2 = crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2

                if random() < mut_prob:
                    #Perform mutation on offspring1
                    offspring1 = mutate(offspring1, data) if mutate.__name__ in ['binary_mutation', 'inversion_mutation'] else mutate(offspring1)
                if random() < mut_prob:
                    #Perform mutation on offspring2
                    offspring2 = mutate(offspring2, data) if mutate.__name__ in ['binary_mutation', 'inversion_mutation'] else mutate(offspring2)
                new_pop.append(Individual(representation=offspring1))  #Add offspring to new population

                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))

            if elitism:
                #Replace the worst individual with the elite individual if elitism is enabled
                worst = max(new_pop, key=attrgetter("fitness"))
                if elite.fitness < worst.fitness:
                    new_pop.pop(new_pop.index(worst))
                    new_pop.append(elite)
            
            self.individuals = new_pop #Update the population
            
            print(f"Best individual of gen #{i + 1}: {min(self, key=attrgetter('fitness'))}")

            #Checking for each generation what is the lower fitness observed
            genFitness = float(min(self, key=attrgetter("fitness")).fitness)
            totalFitness.append(genFitness)
        
        return totalFitness
    

    def __len__(self):
        """
        Checks the number of individuals of the Population object
        Returns:
            int: number of all the individuals in the Population
        """
        return len(self.individuals)

    def __getitem__(self, position):
        """
        Gets a individual from the Population Object at a specific position
        Returns:
            Individual: an Individual Object
        """
        return self.individuals[position]