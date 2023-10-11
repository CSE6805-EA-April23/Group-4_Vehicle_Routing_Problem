from deap import base, creator, tools    
import random
unit_cost = 8.0
init_cost = 100.0
wait_cost = 1.0
delay_cost = 1.5
ind_size = 100
pop_size = 400
cx_pb = 0.85
mut_pb = 0.02

creator.create('FitnessMax', base.Fitness, weights=(1.0, ))
creator.create('Individual', list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator

toolbox.register('indexes', random.sample, range(1, ind_size + 1), ind_size)
# Structure initializers
toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)
# Operator registering
toolbox.register('evaluate', evaluate_individual, instance=instance, unit_cost=unit_cost, \
    init_cost=init_cost, wait_cost=wait_cost, delay_cost=delay_cost)
toolbox.register('select', tools.selRoulette) #FPS
#toolbox.register('select', tools.selStochasticUniversalSampling) #stochastic SUS
toolbox.register('mate', cx_partially_mapped)
toolbox.register('mate', order_cross_over)
toolbox.register('mutate', inverse_mutation)
toolbox.register('mutate', swap_mutation)

pop = toolbox.population(n=pop_size)
