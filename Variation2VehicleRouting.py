import os
import io
import random
from csv import DictWriter
from deap import base, creator, tools
import fnmatch
from json import load, dump
from filelocation import filePath
# -*- coding: utf-8 -*-

def print_route(route, instance,merge=False):
    route_str = '0'
    sub_route_count = 0
    total_routeCovered =0
   # print(instance["customer_1"]["coordinates"])
    # print("print ",route)
    #print("customer X-cor ", json[])
    for sub_route in route:
        sub_route_distance = 0
        
        sub_route_str = '0'
        
        for customer_id in sub_route:
            # sub_route_distance+= calculate_distance("customer_"+str(customer_id),"customer_"+str(customer_id+1),instance) 
            sub_route_str = f'{sub_route_str} - {customer_id}'
            route_str = f'{route_str} - {customer_id}'
            
        sub_route_str = f'{sub_route_str} - 0'
        for i in range (sub_route_count,len(route)):
               for j in range (0, len(sub_route)-1):
                   #print ("customer ",route[i][j], "customer ",route[i][j+1])
                    sub_route_distance+= calculate_distance("customer_"+str(route[i][j]),"customer_"+str(route[i][j+1]),instance) 

                
               #print("route over ",sub_route_count)
               break
        sub_route_count += 1
        if not merge:
                    #sub_route_distance+= calculate_distance("customer_"+str(route[i][j]),"customer_"+str(route[i][j+1]),instance) 
            total_routeCovered = total_routeCovered+ sub_route_distance
            print(f'  Vehicle {sub_route_count}\'s route: {sub_route_str} total-area covered {sub_route_distance}')
        route_str = f'{route_str} - 0'
    if merge:
        print(route_str)  
    print("Total Distance Covered by All Vehicles ",total_routeCovered)    
     


def guess_path_type(path):
    if os.path.isfile(path):
        return 'File'
    if os.path.isdir(path):
        return 'Directory'
    if os.path.islink(path):
        return 'Symbolic Link'
    if os.path.ismount(path):
        return 'Mount Point'
    return 'Path'

def exist(path, overwrite=False, display_info=True):
    if os.path.exists(path):
        if overwrite:
            # if display_info:
            #     print(f'{guess_path_type(path)}: {path} exists. Overwrite.')
            os.remove(path)
            return False
        # if display_info:
            # print(f'{guess_path_type(path)}: {path} exists.')
        return True
    # if display_info:
    #     print(f'{guess_path_type(path)}: {path} does not exist.')
    return False

def load_instance(json_file):
    #Converted filePath generic for All
    if exist(path=filePath(), overwrite=False, display_info=True):
        # print("file exist")
        #Converted filePath generic for All
        with io.open(filePath(), 'r', encoding='utf-8', newline='') as file_object:
            return load(file_object)
    else:
        print("Check Your File Path")
    return None


def merge_rules(rules):
    is_fully_merged = True
    for round1 in rules:
        if round1[0] == round1[1]:
            rules.remove(round1)
            is_fully_merged = False
        else:
            for round2 in rules:
                if round2[0] == round1[1]:
                    rules.append((round1[0], round2[1]))
                    rules.remove(round1)
                    rules.remove(round2)
                    is_fully_merged = False
    return rules, is_fully_merged

def calculate_distance(customer1, customer2):
    return ((customer1['coordinates']['x'] - customer2['coordinates']['x'])**2 + \
        (customer1['coordinates']['y'] - customer2['coordinates']['y'])**2)**0.5

def calculate_distance(customer1, customer2,instance):
    if(customer1 == "customer_0"):

        return ((40 - instance[customer2]['coordinates']['x']**2 + \
                50 - instance[customer2]['coordinates']['y'])**2)**0.5
    # print(customer1," ",instance[customer1]['coordinates']['x'] , instance[customer1]['coordinates']['y'])
    # print(customer2," ",instance[customer2]['coordinates']['x'] , instance[customer2]['coordinates']['y'])

    return ((instance[customer1]['coordinates']['x'] - instance[customer2]['coordinates']['x'])**2 + \
        (instance[customer1]['coordinates']['y'] - instance[customer2]['coordinates']['y'])**2)**0.5


def individual_to_route_decoding(individual, instance):
    route = []
    vehicle_capacity = instance['vehicle_capacity']
    depart_due_time = instance['depart']['due_time']
    # Initialize a sub-route
    sub_route = []
    vehicle_load = 0
    elapsed_time = 0
    last_customer_id = 0
    for customer_id in individual:
        # Update vehicle load
        demand = instance[f'customer_{customer_id}']['demand']
        updated_vehicle_load = vehicle_load + demand
        # Update elapsed time
        service_time = instance[f'customer_{customer_id}']['service_time']
        return_time = instance['distance_matrix'][customer_id][0]
        updated_elapsed_time = elapsed_time + \
            instance['distance_matrix'][last_customer_id][customer_id] + service_time + return_time
        # Validate vehicle load and elapsed time
        if (updated_vehicle_load <= vehicle_capacity) and (updated_elapsed_time <= depart_due_time):
            # Add to current sub-route
            sub_route.append(customer_id)
            vehicle_load = updated_vehicle_load
            elapsed_time = updated_elapsed_time - return_time
        else:
            # Save current sub-route
            route.append(sub_route)
            # Initialize a new sub-route and add to it
            sub_route = [customer_id]
            vehicle_load = demand
            elapsed_time = instance['distance_matrix'][0][customer_id] + service_time
        # Update last customer ID
        last_customer_id = customer_id
    if sub_route != []:
        # Save current sub-route before return if not empty
        route.append(sub_route)
    return route


def evaluate_individual(individual, instance, unit_cost=1.0, init_cost=0, wait_cost=0, delay_cost=0):
   
    total_cost = 0
    route = individual_to_route_decoding(individual, instance)
    total_cost = 0
    for sub_route in route:
        sub_route_time_cost = 0
        sub_route_distance = 0
        elapsed_time = 0
        last_customer_id = 0
        for customer_id in sub_route:
            # Calculate section distance
            distance = instance['distance_matrix'][last_customer_id][customer_id]
            # Update sub-route distance
            sub_route_distance = sub_route_distance + distance
            # Calculate time cost
            arrival_time = elapsed_time + distance
             # ready time is the starting time of customer. 3pm . Suppose arrival time 3:5 pm
              # due time is last time of customer. 3:10 pm. Suppose arrival time 3:5 pm
            time_cost = wait_cost * max(instance[f'customer_{customer_id}']['ready_time'] - arrival_time, 0) + delay_cost * max(arrival_time - instance[f'customer_{customer_id}']['due_time'], 0)
            # Update sub-route time cost
            sub_route_time_cost = sub_route_time_cost + time_cost
            # Update elapsed time
            elapsed_time = arrival_time + instance[f'customer_{customer_id}']['service_time']
            # Update last customer ID
            last_customer_id = customer_id
        # Calculate transport cost
        sub_route_distance = sub_route_distance + instance['distance_matrix'][last_customer_id][0]
        sub_route_transport_cost = init_cost + unit_cost * sub_route_distance
        # Obtain sub-route cost
        sub_route_cost = sub_route_time_cost + sub_route_transport_cost
        # Update total cost
        total_cost = total_cost + sub_route_cost
    fitness = 1.0 / total_cost
    return (fitness, )
 
def order_cross_over(ind1, ind2):
    
    # print("Crossing")
    child1 = [0]*len(ind1)
    child2 = [0] *len(ind2)
    
    cxpoint1, cxpoint2 = sorted(random.sample(range(min(len(ind1), len(ind2))), 2))
    #print("CutPoint1 ",cxpoint1) 
    #print("CutPoint2 ", cxpoint2)
    backup = cxpoint1
    part1 = ind1[cxpoint1:cxpoint2+1] #slice data 1
    part2 = ind2[cxpoint1:cxpoint2+1] #slice data 2

    i=0
    while(cxpoint1<cxpoint2):
        child1[cxpoint1]=part1[i]
        cxpoint1+=1 
        i+=1
    i=0
    cxpoint1 = backup
  
    return child1, child2

def swap_mutation(individual):
    start, stop = (random.sample(range(len(individual)), 2))
    #start=random.randint(0,len(ind))
    #stop=random.randint(0,len(ind))
    temp=individual[start]
    individual[start]=individual[stop]
    individual[stop]=temp
    return (individual, )
    

def run_gavrptw(instance_name, unit_cost, init_cost, wait_cost, delay_cost, ind_size, pop_size, \
    cx_pb, mut_pb, n_gen, export_csv=False, customize_data=False):
 
    json_data_dir = os.path.join(BASE_DIR, 'data', 'json')
    #print(os.path.join(BASE_DIR, 'data', 'json'))

    json_file = os.path.join(json_data_dir, f'{instance_name}.json')
    instance = load_instance(json_file=json_file)
    if instance is None:
        print("Please Check Your file path")
        return
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
    #t5 = toolbox.register('select', tools.selRoulette) #Fitness Proportionate
    #toolbox.register('select', tools.selStochasticUniversalSampling) #stochastic SUS
    toolbox.register('mate', order_cross_over)
    toolbox.register('mutate', swap_mutation)
    print(pop_size)
    pop = toolbox.population(n=pop_size)

    print('Start of evolution')
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    # print("fit ",fitnesses)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    #print(f'  Evaluated {len(pop)} individuals')
    # Begin the evolution
    for gen in range(n_gen):
        print(f'-- Generation {gen} --')
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_pb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            if random.random() < mut_pb:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        print(f'  Evaluated {len(invalid_ind)} individuals')
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)


        mean = sum(fits) / length
        sum2 = sum([x**2 for x in fits])
        std = abs(sum2 / length - mean**2)**0.5
        print(f'  Min {min(fits)}')
        print(f'  Max {max(fits)}')
        print(f'  Avg {mean}')
        print(f'  Std {std}')
       
    print('-- End of (successful) evolution --')
    best_ind = tools.selBest(pop, 1)[0]
    print(f'Best individual: {best_ind}')
    print(f'Fitness: {best_ind.fitness.values[0]}')
    print_route(individual_to_route_decoding(best_ind, instance),instance)
    print(f'Total cost: {1 / best_ind.fitness.values[0]}')



def main():
    '''main()'''
    random.seed(64)

    instance_name = 'C222'

    unit_cost = 8.0
    init_cost = 100.0
    wait_cost = 1.0
    delay_cost = 1.5

    ind_size = 100
    pop_size = 400
    cx_pb = 0.85
    mut_pb = 0.02
    n_gen = 300

    export_csv = True

    run_gavrptw(instance_name=instance_name, unit_cost=unit_cost, init_cost=init_cost, \
        wait_cost=wait_cost, delay_cost=delay_cost, ind_size=ind_size, pop_size=pop_size, \
        cx_pb=cx_pb, mut_pb=mut_pb, n_gen=n_gen, export_csv=export_csv)

#this BASE_DIR is dedicated for base path
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname('__file__')))
# file= open(filePath(),'r')
# print(file.read())
print(BASE_DIR)

if __name__ == '__main__':
    main()
