# -*- coding: utf-8 -*-
"""
Created on Sun May 20 22:52:46 2018

@author: eyeamnice
"""
import random
import gt_child as gt
import proc_funcs as pf
from collections import OrderedDict

def run(df,bases, theta,mutnode,mutate):

    found_alle, ref_alle = first(df,bases,theta)
    node_values = found_alle
    lb = gt.second(df)
    node_dict = dict()
    for val in lb:
        lc = gt.child_alleles(val,node_values)
        if len(lc) == 3 and mutnode not in node_values.keys():
            ld = gt.third(lc)
#            print(ld)
            for key, value in ld.items():
                if key == mutnode:
                    base_val = bases
                    mutate_this = value[0][0]
                    mutate_this2 = value[1][0]
                    allele = list()
                    allele2 = list()
                    for bas in base_val:
                        if mutate == 1 and bas != mutate_this:
                            allele.append(bas)
                            mut_allele = random.choices(allele)
                            for key, val in ld.items():
                                change_node_val = val[0][0]
                            values = [*mut_allele, change_node_val]
                            mutated_node = {key: [values]}
                            node_dict.update(mutated_node)
                        if mutate == 2 and bas != mutate_this2:
                            allele2.append(bas)
                            mut_allele = random.choices(allele2)
                            for key, val in ld.items():
                                change_node_val = val[1][0]
                            values = [change_node_val, *mut_allele]
                            mutated_node = {key: [values]}
                            node_dict.update(mutated_node)
        node_values.update(node_dict)
        ld = gt.third(lc)
        for x , v in ld.items():
            ldd = [i for sub in v for i in sub]
        newdict = {x:[ldd]}
        node_values.update(newdict)
        ordered_genotypes = OrderedDict((k, v) for k, v in sorted(node_values.items(),
                                         key=lambda x: x[0]))
        convert = ordered_genotypes
        coding = []
        for ke, va in convert.items():
            for i in va:
                l = pf.convert_to_string(i)
                coding.append(l)
    return ref_alle, ordered_genotypes, coding

def first(df,bases,theta):

    '''
        Generates dictionary of genotypes for all founder nodes
        using the Chinese Restaurant Process for a finite set of
        tables (4 in this case corresponding to A,G,C,T)

    '''

    founder_Nodes = set((i[0] for i in df if 0 in i))
    founder_alleles = {key:[] for key in founder_Nodes}
    founders = len(founder_Nodes)
    num_alleles = founders*2
    prob=[]
    for x in range(num_alleles):
        bas = bases
        tab = []
        weight=[]
        for x in bas:
            prob = theta/4
            weight.append(prob)
        numb = random.choices(bas, weights = weight)
        tab.append(numb)
        for vals in bas:
            if [vals] == numb:
                weight[vals] += 1
                table = []
                for j in range(num_alleles):
                    chosen_base = random.choices(bas, weights = weight)
                    table.append(chosen_base)
                    weight[vals] += 1
                tables = pf.removebrackets(table)
                tables= eval('[' + tables + ']')
                ref_allele = numb
    alleles = [tables[i:i + 2] for i in range(0, len(tables), 2)]
    for index, i in enumerate(alleles):
        for ind, k in enumerate(founder_alleles.values()):
            if index == ind:
                k.append(i)
##    print(founder_alleles,ref_allele, alt_alleles)
    return founder_alleles, ref_allele
