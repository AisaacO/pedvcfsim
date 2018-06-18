# -*- coding: utf-8 -*-
"""
Created on Sun May 20 22:56:40 2018

@author: eyeamnice

"""

import random

"""
    Generates genotypes of all children nodes
    and updates the dictionary genertaed for
    founder nodes in the pedigree

"""

def second(input_data):

    edges=[]
    for val in input_data:
        if 0 not in val:
            edges.append(val)
    return edges

def child_alleles(edges, node_genotypes):

    myedge = []
    node =[]
    for index, value in enumerate(edges):
        if value not in node_genotypes.keys():
            if not node:
                node.insert(0,value)
        if value in node_genotypes.keys():
            for key in node_genotypes.keys():
                if value == key:
                    myedge.append(node_genotypes.get(value))
    child_edge = list(node + myedge)
    return child_edge

def third(child_edge):

    if len(child_edge) == 3:
        node_dict = dict()
        for index, value in enumerate(child_edge):
            key = child_edge[0]
            if not len(child_edge) < 3:
                node_dict = {key: child_edge[1:3]}
                for val in node_dict.values():
                    for index in val[0]:
                        value1 = random.choices(index)
                    for index in val[1]:
                        value2 = random.choices(index)
                        pair_vals = (value1 , value2)
                        for key, value in node_dict.items():
                            node_dict[key] = pair_vals
        return node_dict
