import sys
from pprint import pprint
from DeepJetCore.DataCollection import DataCollection

datacollection_name = sys.argv[1]

dc = DataCollection()
dc.readFromFile(datacollection_name)

print(dc.samples)

print(dc.sourceList)
print(dc.dataclass)
print(dc.weighterobjects)
print(type(dc.weighterobjects))

print(len(dc.weighterobjects.get('means')[0]))
print(dc.weighterobjects.get('means').dtype.names)
#print(dc.__batchsize )
print(dc.batch_uses_sum_of_squares )
print(dc.optionsdict )

shapes=dc.getKerasFeatureShapes()
print(shapes)

#print("dataclass")
#print(help(dc.dataclass))


print("branches")
print(type(dc.dataclass))
print(dir(dc.dataclass))
#print(dc.dataclass.eta_rel_branches)
#print(dc.dataclass.track_branches)
#print(dc.dataclass.global_branches)
#branches=self.vtx_branches+self.eta_rel_branches+self.track_branches+self.global_branches

#sys.exit()

means = dc.weighterobjects.get('means')[0]
stddevs = dc.weighterobjects.get('means')[1]
varnames = dc.weighterobjects.get('means').dtype.names
#stddevs = dc.means[1]
#varnames = dc.means.dtype.names
mean_dic = {}


for mean, stddev, name in zip(means, stddevs, varnames):
    mean_dic.update( { name : [ mean, stddev ] } )

print(mean_dic)

print("{:<40} {:<25} {:<10}".format('Var','Mean','Stddev'))
for k, v in mean_dic.items():
    label, num = v
    print("{:<40} {:<25} {:<10}".format(k, label, num))


### COPIED FROM modules/datastructures/TrainData_deepFlavour.py trainData_DeepCSV (it is private there and can't be accessed in a pretty way, i think...)
global_branches = ['jet_pt', 'jet_eta',
                   'TagVarCSV_jetNSecondaryVertices',
                   'TagVarCSV_trackSumJetEtRatio',
                   'TagVarCSV_trackSumJetDeltaR',
                   'TagVarCSV_vertexCategory',
                   'TagVarCSV_trackSip2dValAboveCharm',
                   'TagVarCSV_trackSip2dSigAboveCharm',
                   'TagVarCSV_trackSip3dValAboveCharm',
                   'TagVarCSV_trackSip3dSigAboveCharm',
                   'TagVarCSV_jetNSelectedTracks',
                   'TagVarCSV_jetNTracksEtaRel']
n_global = 1

track_branches = ['TagVarCSVTrk_trackJetDistVal',
                 'TagVarCSVTrk_trackPtRel',
                 'TagVarCSVTrk_trackDeltaR',
                 'TagVarCSVTrk_trackPtRatio',
                 'TagVarCSVTrk_trackSip3dSig',
                 'TagVarCSVTrk_trackSip2dSig',
                 'TagVarCSVTrk_trackDecayLenVal']
n_track = 6

eta_rel_branches = ['TagVarCSV_trackEtaRel']
n_eta_rel = 4

vtx_branches = ['TagVarCSV_vertexMass',
             'TagVarCSV_vertexNTracks',
             'TagVarCSV_vertexEnergyRatio',
             'TagVarCSV_vertexJetDeltaR',
             'TagVarCSV_flightDistance2dVal',
             'TagVarCSV_flightDistance2dSig',
             'TagVarCSV_flightDistance3dVal',
             'TagVarCSV_flightDistance3dSig']
n_vtx_branches = 1

branch_list = global_branches + track_branches + eta_rel_branches + vtx_branches
cutoffs = len(global_branches)*[n_global] + len(track_branches)*[n_track] + len(eta_rel_branches)*[n_eta_rel] + len(vtx_branches)*[n_vtx_branches] 
#cutoffs = [n_global] + [n_track] + [n_eta_rel] + [n_vtx_branches] 

print(len(branch_list), branch_list)
print(len(cutoffs), cutoffs)
print(sum(cutoffs))
#branch_list = dc.dataclass.branches
#cutoffs = dc.dataclass.branchcutoffs

#sys.exit()
#branch_list = dc.dataclass.branches
#cutoffs = dc.dataclass.branchcutoffs

variables = []
for branches, cutoff in zip(branch_list, cutoffs):
    offset = -mean_dic[branches][0]
    scale = 1./mean_dic[branches][1]
    print(branches, cutoff, offset, scale)
#    continue

    if cutoff > 1:
        for i in range(0, cutoff):
            var = branches+'_'+str(i)
            variables.append( { 'name' : var, 'scale' : scale, 'offset' : offset , 'defaults' : 0.0 } )
    else:
        variables.append( { 'name' : branches, 'scale' : scale, 'offset' : offset , 'defaults' : 0.0 } )


#    for branch in branches:
#        offset = -mean_dic[branch][0]
#        scale = 1./mean_dic[branch][1]
#
#        if cutoff > 1:
#            for i in range(0, cutoff):
#                var = branch+'_'+str(i)
#                variables.append( { 'name' : var, 'scale' : scale, 'offset' : offset , 'defaults' : 0.0 } )
#        else:
#            variables.append( { 'name' : branch, 'scale' : scale, 'offset' : offset , 'defaults' : 0.0 } )

#print(variables)

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
