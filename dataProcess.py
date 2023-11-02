import os
import io
import random
from csv import DictWriter
from deap import base, creator, tools
import fnmatch
from json import load, dump
from filelocation import filePath
# -*- coding: utf-8 -*-

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

def calculate_distance(customer1, customer2):
    #rootover ((x1-x2)^2 + (y1-y2)^2)
    '''gavrptw.uitls.calculate_distance(customer1, customer2)'''
    return ((customer1['coordinates']['x'] - customer2['coordinates']['x'])**2 + \
        (customer1['coordinates']['y'] - customer2['coordinates']['y'])**2)**0.5

def make_dirs_for_file(path):
    '''gavrptw.uitls.make_dirs_for_file(path)'''
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass

def text2json(customize=False):
    '''gavrptw.uitls.text2json(customize=False)'''
    text_data_dir = os.path.join(BASE_DIR, 'data', 'text_customize' if customize else 'text')
    json_data_dir = os.path.join(BASE_DIR, 'data', 'json_customize' if customize else 'json')
    print("Root Path ",BASE_DIR)
    print("Text direction ", text_data_dir)
    print("Json direction ", json_data_dir)

    
    for text_file in map(lambda text_filename: os.path.join(text_data_dir, text_filename), \
        fnmatch.filter(os.listdir(text_data_dir), '*.txt')):
        print("Testing ", text_file)
        
        json_data = {}
        with io.open(text_file, 'rt', encoding='utf-8', newline='') as file_object:
            #print(file_object.read()) will show whole file
            for line_count, line in enumerate(file_object, start=1):

                # print("Test ", line_count)
                # print("Test2 ", line)


                if line_count in [2, 3, 4, 6, 7, 8, 9]:
                    pass
                elif line_count == 1:
                    # <Instance name>
                    json_data['instance_name'] = line.strip() #line.strip works As Trim()
                 

                elif line_count == 5:
                    # <Maximum vehicle number>, <Vehicle capacity>
                    values = line.strip().split()
                    
                    json_data['max_vehicle_number'] = int(values[0])
                    json_data['vehicle_capacity'] = float(values[1])
                    
                elif line_count == 10: #marking the starting point in json
                    # Custom number = 0, depart
                    # <Custom number>, <X coordinate>, <Y coordinate>,
                    # ... <Demand>, <Ready time>, <Due date>, <Service time>
                    values = line.strip().split()
                    
                    json_data['depart'] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        },
                        'demand': float(values[3]),
                        'ready_time': float(values[4]),
                        'due_time': float(values[5]),
                        'service_time': float(values[6]),
                    }
                    # print(json_data)
                    # return
                else:
                    # <Custom number>, <X coordinate>, <Y coordinate>,
                    # ... <Demand>, <Ready time>, <Due date>, <Service time>
                    values = line.strip().split()
                    # if(line_count==14):
                        # print("Else ", values[0])
                        
                    json_data[f'customer_{values[0]}'] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        },
                        'demand': float(values[3]),
                        'ready_time': float(values[4]),
                        'due_time': float(values[5]),
                        'service_time': float(values[6]),
                    }
        #print(json_data)
        
        # customers = ['depart'] + [f'customer_{x}' for x in range(1, 101)]
        customers = []  # rewrite this whole in readable way
        customers.append('depart')
        for i in range(1, 101):
            customers.append(f'customer_{i}')
        #print(customers)
        # print(json_data) #show total data
        
        json_data['distance_matrix'] = [[calculate_distance(json_data[customer1], json_data[customer2]) for customer1 in customers] for customer2 in customers]
        #print(json_data)
        
        json_file_name = f"{json_data['instance_name']}.json"
        json_file = os.path.join(json_data_dir, json_file_name)
        #print(f'Write to file: {json_file}')
        

        make_dirs_for_file(path=json_file)
        with io.open(json_file, 'wt', encoding='utf-8', newline='') as file_object:
            dump(json_data, file_object, sort_keys=True, indent=4, separators=(',', ': '))
        # break

#this BASE_DIR is dedicated for base path
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname('__file__')))

if __name__ == '__main__':
    text2json()