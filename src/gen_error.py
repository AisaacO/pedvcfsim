# -*- coding: utf-8 -*-
"""
Created on Sun May 20 23:10:38 2018

@author: eyeamnice
"""
import itertools
import pandas as pd

"""
    Error coding for alleles using a dictionary
    with alleles as keys and counts as values.
    This allows calculation of alleic depth field
    in the vcf
"""

def gen_err(e):

    biallelic_gts_with_zeros = list(itertools.permutations('AGCT0', 2))
    removed_vals_with_zeros =[]
    for i in biallelic_gts_with_zeros:
        if i[0] == "0":
            change = i[1]
            remove_zero_vals = (change,) + i[1:]
            removed_vals_with_zeros.append(remove_zero_vals)
    biallelic_gts = biallelic_gts_with_zeros + removed_vals_with_zeros
    final_biallelic_gts = [(i) for i in biallelic_gts if "0" not in i]
    list_of_biallelic_gts = [list(e) for e in final_biallelic_gts]
    gt=[]
    for x in list_of_biallelic_gts:
           gt.append( (''.join([w+' ' for w in x])).strip())
    gen = [e for e in gt if e.strip()]
    gt_list = [e.replace(" ","") for e in gen]
    df = pd.DataFrame({}, columns=list('AGCT'), index=gt_list)
    map_df = pd.DataFrame([df.index.str.contains(x) for x in df.columns],
                          columns=gt_list,
                          index=list('AGCT')).T
    r = df.index.str.match(r"(\w)\1{1,}")
    het = map_df.iloc[~r,:].applymap(lambda k: 1/2-e/3 if k else e/3)
    hom = map_df.iloc[r,:].applymap(lambda k: 1-e if k else e/3)

    return het, hom
