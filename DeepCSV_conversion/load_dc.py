import sys
from pprint import pprint
from DeepJetCore.DataCollection import DataCollection

datacollection_name = sys.argv[1]

dc = DataCollection()
dc.readFromFile(datacollection_name)

means = dc.means[0]
stddevs = dc.means[1]
varnames = dc.means.dtype.names
mean_dic = {}

for mean, stddev, name in zip(means, stddevs, varnames):
    mean_dic.update( { name : [ mean, stddev ] } )


branch_list = dc.dataclass.branches
cutoffs = dc.dataclass.branchcutoffs

variables = []
for branches, cutoff in zip(branch_list, cutoffs):
    for branch in branches:
        offset = -mean_dic[branch][0]
        scale = 1./mean_dic[branch][1]

        if cutoff > 1:
            for i in range(0, cutoff):
                var = branch+'_'+str(i)
                variables.append( { 'name' : var, 'scale' : scale, 'offset' : offset , 'defaults' : 0.0 } )
        else:
            variables.append( { 'name' : branch, 'scale' : scale, 'offset' : offset , 'defaults' : 0.0 } )

outputs = [
        "probb",
        "probbb",
        "probc",
        "probudsg"
    ]


var_dic = {}

var_dic['class_labels'] = outputs
var_dic['inputs'] = variables
defaults = {}

for var in variables:
    defaults.update( { var['name'] : var['defaults'] } )
var_dic['defaults'] = defaults

import json
with open('DeepCSV_var.json', 'w') as json_file:
    json.dump(var_dic, json_file)
with open('defaults.json', 'w') as json_file:
    json.dump(defaults, json_file)
