from functools import reduce
from itertools import product
import os
import json
from turtle import update

COMMENT     = ":comment"
TRANSITION  = ":transition"
VAR         = ":var"
GUARD       = ":guard"
U_GUARD     = ":uguard"
NUMCASES    = ":numcases 2"
CASE        = ":case"
VAL         = ":val"

HEADER      = TRANSITION+"\n"+VAR+" x\n"+VAR+" j\n"

with open('sample.json','r') as file:
    data = json.load(file)

states_lists    = list()
state_var_dict  = dict()
vars_list       = list()
clocks_dict     = dict()


for process in data['process']:
    states_of_process = list()
    num_state = 0
    for state in process['state_list']:
        states_of_process.append({'name':process['name'],'id':num_state,'state':state})
        num_state += 1
    states_lists.append(states_of_process)
    state_var_dict[process['name']] = process['state_var']
    vars_list.extend(process['other_vars'])
    vars_list.append(process['state_var'])
    clocks_dict[process['name']] = process['clock_var']

vars_list.extend(data['stateless_var'])

if os.path.exists('transition.txt'):
    os.remove('transition.txt')

universal_guards = str()
for process in data['process']:
    if process['parametrized']:
        num_state = 0
        for state in process['state_list']:
            universal_guards += U_GUARD + " (= "+state_var_dict[process['name']]+"[j] "+str(num_state)+")"
            if state['inv']:
                universal_guards += " (<= (+ "+clocks_dict[process['name']]+"[j]"+" d) "+state['inv']+")"
            universal_guards += "\n"
            num_state += 1

updates = str()
updates += NUMCASES+"\n"
updates += CASE+" (= x j)\n"
for var in vars_list:
    updates += " "+VAL+" "+var+"[j]\n"
for clock in clocks_dict.values():
    updates += " "+VAL+" (+ "+clock+"[j] d)\n"
updates += CASE+"\n"
for var in vars_list:
    updates += " "+VAL+" "+var+"[j]\n"
for clock in clocks_dict.values():
    updates += " "+VAL+" (+ "+clock+"[j] d)\n"

list_combinations = list(product(*states_lists))

final_res = str()
for transition in list_combinations:
    output = HEADER
    output += GUARD+" (> d 0) "
    for element in transition:
        output += "(= "+state_var_dict[element['name']]+"[x] "+str(element['id'])+") "
        if element['state']['inv']:
            output += "(<= (+ "+clocks_dict[element['name']]+"[x] d) "+element['state']['inv']+") "
    output += "\n"
    output += universal_guards
    output += updates + "\n"
    final_res += output
    
with open('transition.txt','w') as file:
    file.write(final_res)


                        




