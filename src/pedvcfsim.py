#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import argparse
import random
import itertools
import time
import numpy as np
import proc_funcs as pf
import gen_error as gn
from gt_founders import run
from gt_mapping2 import ggcode
import tqdm
import pyprog
from time import sleep
from tqdm import trange
from tqdm import tqdm_notebook


def main():
    '''
        Get all arguments provided by the user, check validity of
        arguments, file format, file content and writes results
        to an output file specified by user or uses default output
    '''
    all_input = vars(args)
    for key, value in dict(all_input).items():
        if value is None or False:
            del all_input[key]
    try:
        args.seed
    except:
        args.seed = int(time.time())
    else:
        random.seed(args.seed)
    if sys.argv[1] == 1:
        print(help)
        sys.exit()
    else:
        print("Checking user entries...")
        if len(sys.argv) < 6:
            print("\t> ERROR: Incorrect number of arguments!",
                  len(sys.argv), "! at least 6 required.")
            print(help)
            sys.stderr.flush()
            sys.exit()
        else:
            print("Commands for this simulation includes:")
            for arg in vars(args):
                print("\t", arg, getattr(args, arg))
            print("Entries >OK! Proceeding...")
            print("Checking", args.input, "file exist...")
    if not os.path.exists(args.input):
        print("ERROR - File not found! Please check your path/filename")
        sys.exit()
    else:
        print("File found !!! ")
        print("Validating file contents...")
    if os.stat(args.input).st_size == 0:
        print("File", args.input, "is empty, please check the file!")
        sys.exit()
    else:
        num_cols = 5
        with open(args.input, 'r') as pedin:
            if all(col.count('\t') < num_cols - 1 for col in pedin):
                print(
                    "\t",
                    args.input,
                    "should contain 5 tabbed columns at least. Exiting...")
                sys.exit()
            else:
                print(args.input, "is tab separated. Proceeding!")
    n = args.num_sim
    bases = [0, 1, 2, 3]
    e = args.error_rate
    cov = args.coverage
    theta = args.theta
    mutate_this_node = args.mutate_node
    mutnode = []
    try:
        args.zygosity
    except:
        args.zygosity = None
    mutate = args.mut_allele
    readers = pf.read_csv(args.input)
    rowss = [["0" if x == "." else x for x in row] for row in list(readers)]
    # Exclude file headers and get individuals and their samples
    file_exclude_header = [row for row in rowss[2:]]
    sites_lists = [row[:3] for row in file_exclude_header]
    sample_lists = [row[4:] for row in file_exclude_header]
#    print(sites_lists, "...", sample_lists)
    try:
        individuals = [i[0] for i in sites_lists]
    except IndexError:
        individuals = [i for i in sites_lists]
    num_sites = list(range(1, len(sites_lists) + 1))
#    print(num_sites)
    lx = {
        l1: l2 for l1,
        l2 in itertools.zip_longest(
            individuals,
            num_sites,
            fillvalue=None)}
#    print(lx)
    str_sites = []
    for items in sites_lists:
        ind_sites = []
        for item in items:
            if item in lx.keys():
                ind_sites.append(lx[item])
            else:
                ind_sites.append(item)
        str_sites.append(ind_sites)
#    print(str_sites)
    sites = ([[int(j) for j in i] for i in str_sites])
#    print(sites)
    for index, ind in enumerate(sites_lists):
        if mutate_this_node in ind:
            mutnode = index +1
#    print(mutnode)
            
    sam_name = individuals
    sample_gl = [str(s) for s in sam_name]
    sample_lb = [s for s in sample_lists]
    sam_name = sample_gl + sample_lb
#    print(sam_name)
    sam_list = pf.removebrackets(sam_name)
    sample_names = (sam_list.replace(", ", "\t")).translate(
        str.maketrans({"'": None}))
#    print(sample_names)
    input_data = [tuple(l) for l in sites]
    cNodes = list((i[0] for i in input_data if 0 not in i))
#    print(cNodes)
    if mutnode not in cNodes:
        print(
            "Node",
            args.mutate_node,
            "is not a child node. Consider using one of",
            cNodes)
        sys.exit()
    else:
        print("Node to be mutated is a child node. Proceeding!")
    if args.output:
        with open(args.output, 'w') as f:
            l1 = "##fileformat=VCFv4.2"
            l2 = "##phasing=partial"
            l3 = "##contig=<ID=1,length = " + str(args.num_sim) + ">"
            l4 = "##vcfsimCommands = -i " + str(args.input) + " -t " + str(args.theta) + " -n " + str(args.num_sim) + " -e " + str(args.error_rate) + " -c " + str(
                args.coverage) + " -m " + str(args.mutate_node) + " -a " + str(args.mut_allele) + " -z " + str(args.zygosity) + " -s " + str(args.seed) + " -o " + str(args.output)
            l5 = "##FILTER=<ID=PASS,Description = "'"All filters passed"'" > "
            l6 = "##FORMAT=<ID=GT,Number = 1,Type=String,Description = "'"Genotype"'" > "
            l7 = "##FORMAT=<ID=AD,Number = R,Type=Integer,Description = "'"Allelic depths for the ref and alt alleles in the order listed"'">"
            l8 = "##vcfsimVersion = v0.0.1"
            f.write(
                "%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n" %
                (l1, l2, l3, l4, l5, l6, l7, l8))
            data_line = "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t" + sample_names
            f.write("%s\n" % (data_line))
            counter = 1
            count = 0
            for x in tqdm.tqdm(range(n), total=len(range(n))):
#                for x in range(n):
    #                s =  ((x/5000)*'#')+str(x)+(' %')
    #                print ('\r'+s)
    #                for i in tqdm.tqdm(range(1)):
                count += 1
                # get values from the function (run)
                ref, node_values, coding = run(
                    input_data, bases, theta, mutnode, mutate)
#                print(node_values, coding)
                try:
                    if args.zygosity:
                        zygo = [item for s in args.zygosity for item in s]
#                        print(zygo)
                        for i, j in enumerate(node_values.keys()):
                            for k, x in enumerate(individuals):
#                                print(k,x, i, j)
                                if k ==i and x == zygo[2] and k == mutnode and zygo[0] == str(1):                                    
                                    node_values[k + 1] = node_values.get(mutnode)
                                    cod = dict(enumerate(coding))
#                                    print(cod)
                                    for q, s in enumerate(coding):
#                                        print(q, s, k, x)
                                        if q == k:
                                            coding[q] = cod.get(q-1)
#                                            print(coding)                                            
                                if zygo[0] == str(2):
                                    pass
                except:
                    pass
#                print(node_values)    
                alt, code, inner_node = ggcode(node_values, ref)
                readers = pf.read_csv(args.input)
                rowss = list(readers)
#                headers = rowss[0]
                rest = [row for row in rowss[0:]]
#                print(rest)
                year = dict()
                for i in rest:
                    key = i[0]
                    val = i[4:]
                    year[key] = val
                if 'I' in year:
                    del year['I']
                for key, val in year.items():
                    for i, x in enumerate(coding):
                        if key == i + 1:
                            year[key] = [x for y in val]
                inner_dict = dict()
                for k, v in year.items():
                    for i in v:
                        i = i.replace(i, "1")
                        inner_dict[k] = [i for y in v]
                vz = []
                for x in inner_dict.values():
                    vz.append(x)
                results = [[int(j) for j in i] for i in vz]
                ddk = ["0"] * len(results)
                ddad = list(zip(ddk, [str(a).replace(' ', '')
                                      for a in results]))
                final = []
                for i in ddad:
                    final.extend([i[0], (i[1]).strip("[]")])
                xx = [":".join(final[i:i + 2])
                      for i in range(0, len(final), 2)]
                soma = [x.replace('1', '.') for x in xx]
                soma = [x.replace('0', '') for x in soma]
                ref_val = pf.convert_to_string(ref)
                ref_string = pf.removebrackets(ref_val)
                reference = str(ref_string)
                het, hom = gn.gen_err(e)
                final_vals_based_on_error = []
#                print(coding)
                calculated_error_rates = []
                for i in coding:
                    if i not in het.index:
                        gt_error = hom.loc[[i]]
                        calculated_error_rates.append(gt_error.values.tolist())
                    else:
                        gt_error = het.loc[[i]]
                        calculated_error_rates.append(gt_error.values.tolist())
                for z, i in enumerate(calculated_error_rates):
                    val_based_on_applied_error = []
                    if not (z + 1) in cNodes:
                        apply_error_rate = np.random.multinomial(
                            cov[0], i[0], size=1)
                        val_based_on_applied_error.append(apply_error_rate)
                    else:
                        apply_error_rate = np.random.multinomial(
                            cov[1], i[0], size=1)
                        val_based_on_applied_error.append(apply_error_rate)
                    final_vals_based_on_error.append(
                        *val_based_on_applied_error)
                list_of_final_vals = np.array(
                    final_vals_based_on_error).tolist()
                ad_rows = list(zip(*list_of_final_vals))
#                print(ad_rows)
                ad_rowws = np.array(np.array(*ad_rows)).tolist()
#                print(ad_rowws)
                str_bases = ["A", "G", "C", "T"]
                ad_dict = []
                for y, i in enumerate(ad_rowws):
                    a_dict = dict(zip(str_bases, i))
                    ad_dict.append(a_dict)
#                ds = dict([(key,d[key]) for d in ad_dict for key in d])
#                print(ad_dict)
                refalt = []
                refalt.append(reference)
                refalt.extend(alt.split(","))
                keysss = []
                for i in ad_dict:
                    l = [i.setdefault(key, 0) for key in refalt]
                    for k, v in i.items():
                        if k not in refalt and v > 0:
                            refalt.append(k)
                            l.append(v)
                    keysss.append(l)
                keyssss = keysss
#                print(keysss)
                for x in keysss:
                    if len(x) < len(refalt):
                        x.append(0)
                        keyssss.append(x)
                    else:
                        pass
#                print(keyssss, "\n")
                final_alts = ",".join(refalt[1:])
                ddcode = re.split(r'\t+', code)
#                print(ddcode)
                ddadcount = list(
                    zip(ddcode, [str(a).replace(' ', '') for a in keyssss]))
#                print(ddadcount)
                merged_ads_and_codes = []
                for i in ddadcount:
                    merged_ads_and_codes.extend([i[0], (i[1]).strip("[]")])
                mappings = [":".join(merged_ads_and_codes[i:i + 2])
                            for i in range(0, len(merged_ads_and_codes), 2)]
#                print(mappings)
#                print(sample_lists, individuals)
                gtad_maps = '\t'.join(mappings)
                list_range = list(map(str, range(1, 5)))
#                print(ddcode)
                new_code = [[[('0' if b in list_range else b) for b in x]
                             for x in ddcode] for a in list_range]
#                print(new_code, "\n")
                dcode = new_code[0]
#                print(dcode)
                lo = ["".join(i) for i in dcode]
#                print(soma)
#                print(mappings)
#                print(coding)
                try:
                    args.zygosity
#                    try:
                    zygo = [item for s in args.zygosity for item in s]
                    if zygo[0] == str(1):
#                        print(zygo)
                        twin_dict2 = dict(zip(individuals, mappings))
    #                        print(twin_dict2)
                        g_soma = [x + y for x, y in zip(lo, soma)]
                        for k, v in enumerate(g_soma):
                            for s, t in enumerate(ddcode):
                                if s == k and k == (mutnode - 1):
                                    g_soma[k] = re.sub(r'.*:', t + ":", v)
                                    for x, y in enumerate(individuals):
                                        if zygo[2] == y:
                                            g_soma[x] = re.sub(r'.*:', t + ":", v)
    #                        print(g_soma)
                                            for i in twin_dict2.keys():
                                                if zygo[0] == str(1):
                            #                    print(i)
                                                    if zygo[2] == i and zygo[1] == mutate_this_node:
                                                        twin_dict2[i] = twin_dict2[zygo[1]]
                                                    elif zygo[1] == i and zygo[2] == mutate_this_node:
                                                        twin_dict2[i] = twin_dict2[zygo[2]]
                                                    elif zygo[1] == i or zygo[2] == i and zygo[2] != mutate_this_node or zygo[1] != mutate_this_node:
                                                        twin_dict2[i] = twin_dict2[zygo[1]]
                                                    else:
                                                        pass
                                                if zygo[0] == str(2):
                                                    pass
                        #                    print(twin_dict2)
                                            mapmaps = list(twin_dict2.values())
                                            for p, q in enumerate(mapmaps):
                                                for r, s in enumerate(mappings):
                                                    if p == x and p == r:
                                                        mapmaps[x] = q.replace(q,s)
    #                        print(mapmaps)
    #                        print(list(mapmaps))
                        gtad_maps = '\t'.join(mapmaps)
                        gtad_soma = '\t'.join(g_soma)
                    else:
                        g_soma = [x + y for x, y in zip(lo, soma)]
                        for k, v in enumerate(g_soma):
                            for s, t in enumerate(ddcode):
                                if s == k and k == (mutnode - 1):
                                    g_soma[k] = re.sub(r'.*:', t + ":", v)
                        gtad_maps = '\t'.join(mappings)
                        gtad_soma = '\t'.join(g_soma)
                except:
                    g_soma = [x + y for x, y in zip(lo, soma)]
                    for k, v in enumerate(g_soma):
                        for s, t in enumerate(ddcode):
                            if s == k and k == (mutnode - 1):
                                g_soma[k] = re.sub(r'.*:', t + ":", v)
#                except:
#                        g_soma = [x + y for x, y in zip(lo, soma)]
                gtad_maps = '\t'.join(mappings)
                gtad_soma = '\t'.join(g_soma)
#                print(gtad_soma, gtad_maps)
                last_gtad = "\t".join([gtad_soma, gtad_maps])
#                print(last_gtad)
#                sleep(0.1)
#    # Set current status
#                prog.set_stat(x + 1)
#    # Update Progress Bar again
#                prog.update()
                f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (str(counter), str(count), str("."),
                                                                  reference, final_alts, str("."), str("PASS"), str("."), str("GT" + " :AD"), str(last_gtad)))
                pass#time.sleep(0.01)
#            prog.end()
##                for i in tqdm.tqdm(range(1)):
##                    time.sleep(0.01)
        print("Results have been written to ", args.output)


if __name__ == '__main__':

    #    parser = argparse.ArgumentParser()
    """ Gets input from user through command line. By using argparse, values entered are automatically
        checked against the required types before simulation is started.
    """
    print("*******************************************")
#    print("\tBegin \033[0;34mvcfsim.py\033[0;m(v0.0.1)")
    print("\tBegin \033[0;33mvcfsim.py\033[0;m(v0.0.1)")
#    \x1b[1,33m
    print("\tLast updated: May 03, 2018.")
    print("\tRequires running python 3!\n")
    print("*******************************************")
    examples = '''example:
    [python] [vcfsim.py] [input.ped] [theta] [No of simulations] [node with mutation] [output]
    Example: vcfsim.py input.ped -t 0.001 -N 1000 -n 3 -o output.vcf'''
    parser = argparse.ArgumentParser(
        description='Simulating meiosis and mutation in vcf format from pedigree file',
        epilog=examples, formatter_class=argparse.RawDescriptionHelpFormatter)
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-i', '--input', type=pf.valid_extension,
                                help='input file in ped format. Must end with .ped', required=True)
    required.add_argument('-t', '--theta', type=float, default=0.001,
                                help='Controls meiosis simulation [default: %(default)3f]', required=True)
    required.add_argument('-n', '--num_sim', type=int, default=1000,
                                help='Number of simulations [default: %(default)d]', required=True)
    required.add_argument('-m', '--mutate_node', 
                                help='Child node to be mutated', required=True)
    required.add_argument('-e', '--error_rate', type=float, nargs='?',
                                help='Error rate in simulation', required=False)
    required.add_argument('-c', '--coverage', type=int, nargs=2,
                                help='Coverage of sequences', required=False)
    optional.add_argument('-z', '--zygosity', action='append',nargs=3, metavar=('zygosity','twin1','twin2'),
                                help='Specifies zygosity of twin children if any. 1 for Monozygotic or 2 for Dizygotic [default: %(default)s]', required=False)
    optional.add_argument('-a', '--mut_allele', type=int, choices=range(1, 3), default=2,
                                help='Mutate allele in child node. 1 for Paternal or 2 for maternal allele [default: %(default)s]', required=False)
    optional.add_argument('-o', '--output', type=pf.valid_output,
                                help='Output file name with vcf extension [default: %(default)s]', default="result.vcf")
    optional.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s 2.0',
        help='output version details')
    optional.add_argument('-V', '--verbose', action="store_true",
                                help='Increased simulation verbosity', required=False)
    optional.add_argument('-s', '--seed', type=int, dest="seed",
                                help='Random seed for simulation run', required=False)
    parser._action_groups.append(optional)

    try:
        args = parser.parse_args()
        main()
    except KeyboardInterrupt:
        sys.exit(1)
