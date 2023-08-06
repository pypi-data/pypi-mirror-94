# -*- coding: utf-8 -*-



#%%



import numpy as np
import numpy 



#%% Byte conversion
    
def byte_conversion(x,properties):

  count = 0
  conversion_final = np.zeros(len(properties["nb_bytes"]))

  for i in range(len(properties["nb_bytes"])):
    selection = x[count:count+properties["nb_bytes"][i]]

    b = np.array(selection,dtype=str).tolist()
    stringbyte = "".join(b)
    conversion = int(stringbyte, 2)/(2**len(stringbyte)-1)
    conversion_final[i] = properties["min_val"][i] + \
      (properties["max_val"][i]-properties["min_val"][i])*conversion

    count += properties["nb_bytes"][i]

  return conversion_final


# OBJECTIVE : MAXIMIZE
def cal_pop_fitness(pop,properties,obj_fct):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function caulcuates the sum of products between each input and its corresponding weight.
    
    fitness = np.zeros(len(pop))

    for i in range(len(pop)):
        
      # Convert bytes to deltas
      x = pop[i]
      vals = byte_conversion(x,properties)
      fitness[i] = -obj_fct(vals)

    return fitness


def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = numpy.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999
    return parents


def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)

    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k%parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1)%parents.shape[0]
        
        # Random selection of genes
        h = numpy.random.permutation(len(parents.T))
        pos1 = h[:int(len(parents.T)/2)]
        pos2 = h[int(len(parents.T)/2):]

        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, pos1] = parents[parent1_idx, pos1]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, pos2] = parents[parent2_idx, pos2]

    return offspring


def mutation(offspring_crossover,prop_mut):
    # Mutation changes a single gene in each offspring randomly.
    nb_mut = int( numpy.sum(offspring_crossover*0+1)*prop_mut )
    for _ in range(nb_mut):
        # The random value to be added to the gene.
        rd1 = numpy.random.randint(0,len(offspring_crossover))
        rd2 = numpy.random.randint(0,len(offspring_crossover.T))
        offspring_crossover[rd1, rd2] = numpy.abs(offspring_crossover[rd1, rd2] - 1)

    return offspring_crossover



#%%


class ga:
    
    
    def __init__(self,obj_fct,properties,sol_per_pop,ratio_new=.9,\
                 prop_mut=.1,new_population=None):
    
        self.obj_fct = obj_fct
        self.properties = properties
                
        # Paramètres ajustables arbitraires
        self.num_parents_mating = int(sol_per_pop - ratio_new*sol_per_pop)
        self.prop_mut = prop_mut
        
        # Defining the population size.
        self.pop_size = (sol_per_pop,np.sum(properties["nb_bytes"]))
        
        #Creating the initial population.
        if( new_population ):
            0
        else:
            new_population = numpy.random.randint(0,2, size=self.pop_size)
            
        self.new_population = new_population
        
        
        
    def iterate(self,num_generations,verbose=True):
        
        for generation in range(num_generations):

            
            # Measing the fitness of each chromosome in the population.
            fitness = cal_pop_fitness( self.new_population, \
                                      self.properties, self.obj_fct )
            if(verbose):
                print("Generation ", generation+1, " : ", -np.max(fitness))
                
            # Selecting the best parents in the population for mating.
            parents = select_mating_pool(self.new_population, fitness, 
                                              self.num_parents_mating)
            
            # Generating next generation using crossover.
            offspring_crossover = crossover(parents,
                            offspring_size=(self.pop_size[0]-parents.shape[0],
                                        np.sum(self.properties["nb_bytes"])))
            
            # Adding some variations to the offsrping using mutation.
            offspring_mutation = mutation(offspring_crossover,self.prop_mut)
            
            # Creating the new population based on the parents and offspring.
            self.new_population[:parents.shape[0], :] = parents
            self.new_population[parents.shape[0]:, :] = offspring_mutation

        

    def get_solution(self):
        
        fitness = cal_pop_fitness( self.new_population, \
                                      self.properties, self.obj_fct )
        best_pos = np.argsort(-fitness)[0]
        
        sol = self.new_population[best_pos]
        sol = byte_conversion(sol,self.properties)

        return sol
        
        