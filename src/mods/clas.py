# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 10:56:58 2018

@author: eyeamnice
"""

# define Python user-defined exceptions
class ZygotError(Exception):
   """Base class for other exceptions"""
   pass

class ValueNotProvided(ZygotError):
   """Raised when the input value is too small"""
   pass

class ValueNotEnough(ZygotError):
   """Raised when the input value is too large"""
   pass

#number = 10
#
#while True:
#   try:
#       i_num = int(input("Enter a number: "))
#       if i_num < number:
#           raise ValueNotProvided
#       elif i_num > number:
#           raise ValueNotEnough
#       break
#   except ValueNotProvided:
#       print("No values for zygosity were provided")
#       print()
#   except ValueNotEnough:
#       print("The number of values for zygosity must be = 3!")
#       print()
#
#print("Congratulations! You guessed it correctly.")

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
##!/usr/bin/env python
## -*- coding: utf-8 -*-
#
#import os
#import re
#import sys
#import argparse
#import itertools
#import time
#import numpy as np
#import proc_funcs as pf
#import gen_error as gn
#from gt_founders import run
#from gt_mapping2 import ggcode
#import tqdm
#
#
#
#def main():
#    
#    args = parse_args(sys.argv[1:])
#    verify = checkargs(args)
#    print(verify)
#
#
#    all_input = vars(args)
#    n = args.num_sim
#    bases = [0, 1, 2, 3]
#    e = args.error_rate
#    cov = args.coverage
#    theta = args.theta
#    zygosity = args.zygosity
#    mutate_this_node = args.mutate_node
#    mutnode = []
#    for key, value in dict(all_input).items():
#        if value is None or False:
#            del all_input[key]
#    mutate = args.mut_allele
#    readers = pf.read_csv(args.input)
#    rowss = [["0" if x == "." else x for x in row] for row in list(readers)]
#    # Exclude file headers and get individuals and their samples
#    file_exclude_header = [row for row in rowss[2:]]
#    sites_lists = [row[:3] for row in file_exclude_header]
#    sample_lists = [row[4:] for row in file_exclude_header]
#    try:
#        individuals = [i[0] for i in sites_lists]
#    except IndexError:
#        individuals = [i for i in sites_lists]
#    num_sites = list(range(1, len(sites_lists) + 1))
##    print(num_sites)
#    ind_index_dict = {
#        l1: l2 for l1,
#        l2 in itertools.zip_longest(
#            individuals,
#            num_sites,
#            fillvalue=None)}
#    str_sites = []
#    for items in sites_lists:
#        ind_sites = []
#        for item in items:
#            if item in ind_index_dict.keys():
#                ind_sites.append(ind_index_dict[item])
#            else:
#                ind_sites.append(item)
#        str_sites.append(ind_sites)
#    sites = ([[int(j) for j in i] for i in str_sites])
#    for index, ind in enumerate(sites_lists):
#        if mutate_this_node in ind:
#            mutnode = index + 1
#    sam_name = individuals
#    sample_gl = [str(s) for s in sam_name]
#    sample_lb = [s for s in sample_lists]
#    sam_name = sample_gl + sample_lb
#    sam_list = pf.removebrackets(sam_name)
#    sname = (sam_list.replace(", ", "\t")).translate(
#        str.maketrans({"'": None}))
#    input_data = [tuple(l) for l in sites]
#    cNodes = list((i[0] for i in input_data if 0 not in i))
#    if mutnode not in cNodes:
#        print(
#            "Node",
#            args.mutate_node,
#            "is not a child node. Consider using one of",
#            cNodes)
#        sys.exit()
#    else:
#        print("Node to be mutated is a child node. Proceeding!")
#    if args.output:
#        with open(args.output, 'w') as vcf:
#            header_one = first_header(args, zygosity)
#            vcf.write(f"{chr(10).join(header_one)}")
#            header_two = (
#             "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t" + sname)
#            vcf.write("%s\n" % (header_two))
#            counter = 1
#            count = 0
#            for x in tqdm.tqdm(range(n), total=len(range(n))):
#                count += 1
#                # get values from the function (run)
#                ref, node_values, coding = run(
#                    input_data, bases, theta, mutnode, mutate)
#                '''
#                    check if zygosity is given and if value = 1, the genotypes
#                    of the individuals will be the same (always conform to
#                    mutated node if its one of the monozygote
#                    twins). If value = 2, the genotypes are different (
#                    dizygotes treated as different individuals).
#                '''
#                try:
#                    if args.zygosity:
#                        zygo = [item for s in args.zygosity for item in s]
#                        for i, j in enumerate(node_values.keys()):
#                            for k, x in enumerate(individuals):
#                                if (k == i and x == zygo[2] and
#                                        k == mutnode and zygo[0] == str(1)):
#                                    node_values[k + 1] = (
#                                            node_values.get(mutnode))
#                                    cod = dict(enumerate(coding))
#                                    for q, s in enumerate(coding):
#                                        if q == k:
#                                            coding[q] = cod.get(q-1)
#                                if zygo[0] == str(2):
#                                    pass
#                except Exception:
#                    pass
#                alt, code, inner_node = ggcode(node_values, ref)
#                readers = pf.read_csv(args.input)
#                rowss = list(readers)
#                rowss_as_strings = [row for row in rowss[0:]]
#                rowss_dict = dict()
#                for i in rowss_as_strings:
#                    key = i[0]
#                    val = i[4:]
#                    rowss_dict[key] = val
#                for key, val in rowss_dict.items():
#                    for i, x in enumerate(coding):
#                        if key == i + 1:
#                            rowss_dict[key] = [x for y in val]
#                inner_dict = dict()
#                for k, v in rowss_dict.items():
#                    for i in v:
#                        inner_dict[k] = [i.replace(i, "1") for y in v]
#                all_ones_val = []
#                for x in inner_dict.values():
#                    all_ones_val.append(x)
#                code_results = [[int(j) for j in i] for i in all_ones_val]
#                results = list(zip(["0"] * len(code_results), [str(a).replace(
#                        ' ', '') for a in code_results]))
#                final_results = []
#                for i in results:
#                    final_results.extend([i[0], (i[1]).strip("[]")])
#                merged_final = [":".join(final_results[i:i + 2]) for i in
#                                range(0, len(final_results), 2)]
#                soma = [x.replace('1', '.') for x in merged_final]
#                soma = [x.replace('0', '') for x in soma]
#                ref_val = pf.convert_to_string(ref)
#                ref_string = pf.removebrackets(ref_val)
#                reference = str(ref_string)
#                het, hom = gn.gen_err(e)
#                final_vals_based_on_error = []
#                calculated_error_rates = []
#                for i in coding:
#                    if i not in het.index:
#                        gt_error = hom.loc[[i]]
#                        calculated_error_rates.append(gt_error.values.tolist())
#                    else:
#                        gt_error = het.loc[[i]]
#                        calculated_error_rates.append(gt_error.values.tolist())
#                for z, i in enumerate(calculated_error_rates):
#                    val_based_on_applied_error = []
#                    if not (z + 1) in cNodes:
#                        apply_error_rate = np.random.multinomial(
#                            cov[0], i[0], size=1)
#                        val_based_on_applied_error.append(apply_error_rate)
#                    else:
#                        apply_error_rate = np.random.multinomial(
#                            cov[1], i[0], size=1)
#                        val_based_on_applied_error.append(apply_error_rate)
#                    final_vals_based_on_error.append(
#                        *val_based_on_applied_error)
#                list_of_final_vals = np.array(
#                    final_vals_based_on_error).tolist()
#                ad_rows = list(zip(*list_of_final_vals))
#                ad_rowws = np.array(np.array(*ad_rows)).tolist()
#                str_bases = ["A", "G", "C", "T"]
#                ad_dict = []
#                for y, i in enumerate(ad_rowws):
#                    a_dict = dict(zip(str_bases, i))
#                    ad_dict.append(a_dict)
#                refalt = []
#                refalt.append(reference)
#                refalt.extend(alt.split(","))
#                ads_and_errors = []
#                for i in ad_dict:
#                    ad_list = [i.setdefault(key, 0) for key in refalt]
#                    for k, v in i.items():
#                        if k not in refalt and v > 0:
#                            refalt.append(k)
#                            ad_list.append(v)
#                    ads_and_errors.append(ad_list)
#                for x in ads_and_errors:
#                    if len(x) < len(refalt):
#                        x.append(0)
#                        ads_and_errors.append(x)
#                    else:
#                        pass
#                final_alts = ",".join(refalt[1:])
#                ddcode = re.split(r'\t+', code)
#                ddadcount = list(zip(ddcode, [str(a).replace(
#                        ' ', '') for a in ads_and_errors]))
#                merged_ads_and_codes = []
#                for i in ddadcount:
#                    merged_ads_and_codes.extend([i[0], (i[1]).strip("[]")])
#                mappings = [":".join(merged_ads_and_codes[i:i + 2])
#                            for i in range(0, len(merged_ads_and_codes), 2)]
#                gtad_maps = '\t'.join(mappings)
#                list_range = list(map(str, range(1, 5)))
#                new_code = [[[('0' if b in list_range else b) for b in x]
#                             for x in ddcode] for a in list_range]
#                dcode = new_code[0]
#                lo = ["".join(i) for i in dcode]
#                try:
#                    args.zygosity
#                    zygo = [item for s in args.zygosity for item in s]
#                    if zygo[0] == str(1):
#                        twin_dict2 = dict(zip(individuals, mappings))
#                        g_soma = [x + y for x, y in zip(lo, soma)]
#                        for k, v in enumerate(g_soma):
#                            for s, t in enumerate(ddcode):
#                                if s == k and k == (mutnode - 1):
#                                    g_soma[k] = re.sub(r'.*:', t + ":", v)
#                                for x, y in enumerate(individuals):
#                                    if zygo[2] == y:
#                                        g_soma[x] = re.sub(
#                                                r'.*:', t + ":", v)
#                                        for i in twin_dict2.keys():
#                                            if zygo[0] == str(1):
#                                                if (zygo[2] == i and
#                                                        zygo[1] ==
#                                                        mutate_this_node):
#                                                    twin_dict2[i] = (
#                                                        twin_dict2[zygo[1]])
#                                                elif (zygo[1] == i and
#                                                      zygo[2] ==
#                                                      mutate_this_node):
#                                                    twin_dict2[i] = (
#                                                        twin_dict2[zygo[2]])
#                                                elif (zygo[1] == i or
#                                                      zygo[2] == i and
#                                                      zygo[2] !=
#                                                      mutate_this_node or
#                                                      zygo[1] !=
#                                                      mutate_this_node):
#                                                    twin_dict2[i] = (
#                                                        twin_dict2[zygo[1]])
#                                                else:
#                                                    pass
#                                            if zygo[0] == str(2):
#                                                pass
#                                        mapmaps = list(twin_dict2.values())
#                                        for p, q in enumerate(mapmaps):
#                                            for s, t in enumerate(
#                                                    mappings):
#                                                if p == x and p == s:
#                                                    mapmaps[x] = q.replace(
#                                                                q, t)
#                        gtad_maps = '\t'.join(mapmaps)
#                        gtad_soma = '\t'.join(g_soma)
#                    else:
#                        g_soma = [x + y for x, y in zip(lo, soma)]
#                        for k, v in enumerate(g_soma):
#                            for s, t in enumerate(ddcode):
#                                if s == k and k == (mutnode - 1):
#                                    g_soma[k] = re.sub(r'.*:', t + ":", v)
#                        gtad_maps = '\t'.join(mappings)
#                        gtad_soma = '\t'.join(g_soma)
#                except Exception:
#                    g_soma = [x + y for x, y in zip(lo, soma)]
#                    for k, v in enumerate(g_soma):
#                        for s, t in enumerate(ddcode):
#                            if s == k and k == (mutnode - 1):
#                                g_soma[k] = re.sub(r'.*:', t + ":", v)
#                gtad_maps = '\t'.join(mappings)
#                gtad_soma = '\t'.join(g_soma)
#                last_gtad = "\t".join([gtad_soma, gtad_maps])
#                vcf.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (str(
#                    counter), str(count), str("."), reference, final_alts, str(
#                        "."), str("PASS"), str("."), str("GT" + " :AD"), str(
#                                last_gtad)))
##                pass
#        print("Results have been written to ", args.output)
#
#
#def checkargs(args):
#    
#    '''
#        Get all arguments provided by the user, check validity of
#        arguments, file format, file content and writes results
#        to an output file specified by user or uses default output
#    '''    
#
#    try:
#        
#        if args.seed:
#            pass
#        else:
#            args.seed = int(time.time())
#        if sys.argv[1] == 1:
#            print(help)
#            sys.exit()
#        else:
#            print("Checking user entries...")
#        if len(sys.argv) < 6:
#            print("\t> ERROR: Incorrect number of arguments!",
#                  len(sys.argv), "! at least 6 required.")
#            print(help)
#            sys.exit()
#        else:
#            print("Commands for this simulation includes:")
#            for arg in vars(args):
#                print("\t", arg, getattr(args, arg))
#            print("Entries >OK! Proceeding...")
#            print("Checking", args.input, "file exist...")
#        if not os.path.exists(args.input):
#            print("ERROR - File not found! Please check your path/filename")
#            sys.exit()
#        else:
#            print("File found !!! ")
#            print("Validating file contents...")
#        if os.stat(args.input).st_size == 0:
#            print("File", args.input, "is empty, please check the file!")
#            sys.exit()
#        else:
#            num_cols = 5
#            with open(args.input, 'r') as pedin:
#                if all(col.count('\t') < num_cols - 1 for col in pedin):
#                    print(
#                        "\t",
#                        args.input,
#                        "should contain at least 5 columns. Exiting...")
#                    sys.exit()
#                else:
#                    print(args.input, "is tab separated. Proceeding!")
#        if args.zygosity is not None and len(args.zygosity) not in (0, 3):
#            args.zygosity
#        else:
#            args.zygosity = None
#        
#    except KeyboardInterrupt:
#        sys.exit(1)
#
#        
#def first_header(args, zygosity):
#
#    '''
#    Write vcf header to file. This includes the user supplied input values 
#    for the simulation run
#    '''
#    l1 = "##fileformat=VCFv4.2"
#    l2 = "##phasing=partial"
#    l3 = "##contig=<ID=1,length = " + str(args.num_sim) + ">"
#    l4 = "##vcfsimCommands = -i " + str(args.input) + " -t " + str(
#        args.theta) + " -n " + str(args.num_sim) + " -e " + str(
#        args.error_rate) + " -c " + str(
#        args.coverage) + " -m " + str(args.mutate_node) + " -a " + str(
#        args.mut_allele) + " -z " + str(zygosity) + " -s " + str(
#        args.seed) + " -o " + str(args.output)
#    l5 = "##FILTER=<ID=PASS,Description = "'"All filters passed"'" > "
#    l6 = "##FORMAT=<ID=GT,Number = 1,Type=String,Description = "
#    '"Genotype"'" > "
#    l7 = "##FORMAT=<ID=AD,Number = R,Type=Integer,Description = "
#    '"Allelic depths for the ref and alt alleles in listed order"'">"
#    l8 = "##vcfsimVersion = v0.0.1"
#    header_one = [l1, l2, l3, l4, l5, l6, l7, l8]
#    return header_one
#
#    
#def parse_args(args):
#    
#    #Parse the command line arguments to the program
#    examples = '''example:
#    [python] [vcfsim.py] [input.ped] [theta] [No of simulations]
#    [node with mutation] [output]
#    Example: vcfsim.py input.ped -t 0.001 -N 1000 -n 3 -o output.vcf'''
#    parser = argparse.ArgumentParser(
#        description='Simulating mutation from pedigree and graph-like files',
#        epilog=examples, formatter_class=argparse.RawDescriptionHelpFormatter)
#    optional = parser._action_groups.pop()
#    required = parser.add_argument_group('required arguments')
#    required.add_argument('-i', '--input',
#                          type=pf.valid_extension,
#                          help='input file in ped format.'
#                          ' Must end with .ped',
#                          required=True)
#    required.add_argument('-t', '--theta',
#                          type=float, default=0.001,
#                          help='Controls meiosis simulation'
#                          ' [default: %(default)3f]',
#                          required=True)
#    required.add_argument('-n', '--num_sim',
#                          type=int,
#                          default=1000,
#                          help='Number of simulations'
#                          ' [default: %(default)d]',
#                          required=True)
#    required.add_argument('-m', '--mutate_node',
#                          help='Child node to be mutated',
#                          required=True)
#    required.add_argument('-e', '--error_rate',
#                          type=float, nargs='?',
#                          help='Genotype Error rate',
#                          required= True)
#    required.add_argument('-c', '--coverage',
#                          type=int,
#                          nargs=2,
#                          help='Coverage of sequences',
#                          required=True)
#    optional.add_argument('-a', '--mut_allele',
#                          type=int, choices=range(1, 3),
#                          default=2,
#                          help='Mutate allele in child node.'
#                          ' 1 for Paternal allele or'
#                          ' 2 for maternal allele'
#                          ' [default: %(default)s]',
#                          required=False)
#    optional.add_argument('-o', '--output',
#                          type=pf.valid_output,
#                          default="result.vcf",
#                          help='Output file name with vcf extension'
#                          '[default: %(default)s]',
#                          required = False)
#    optional.add_argument('-v','--version',
#                          action='version',
#                          version='%(prog)s 1.0.1',
#                          help='output version details')
#    optional.add_argument('-V', '--verbose',
#                          action="store_true",
#                          help='Increased simulation verbosity',
#                          required=False)
#    optional.add_argument('-s', '--seed',
#                          type=int, dest="seed",
#                          help='Random seed for simulation run',
#                          required=False)
#    optional.add_argument('-z', '--zygosity',
#                          action='append', nargs=3,
#                          help='Specifies zygosity of twin children if'
#                          ' any. 1 for Monozygotic or 2 for Dizygotic'
#                          ' [default: %(default)s]',
#                          required=False)
#    parser._action_groups.append(optional)
#    return parser.parse_args(args)
#
#if __name__ == '__main__':
#    
#    print("*******************************************")
#    print("\tBegin \033[0;33mpedvcfsim.py\033[0;m(v1.0.1)")
#    print("\tLast updated: August 19, 2018.")
#    print("\tRequires running python 3!\n")
#    print("*******************************************")
#
#    main()
#
#































#
#
#
##!/usr/bin/env python
## -*- coding: utf-8 -*-
#
#import os
#import re
#import sys
#import argparse
#import itertools
#import time
#import numpy as np
#import proc_funcs as pf
#import gen_error as gn
#from gt_founders import run
#from gt_mapping2 import ggcode
#import tqdm
#
#class ZygotError(Exception):
#   """Base class for other exceptions"""
#   pass
#
#class ValueNotProvided(ZygotError):
#   """Raised when the input value is too small"""
#   pass
#
#class ValueNotEnough(ZygotError):
#   """Raised when the input value is too large"""
#   pass
#
#def main():
#    
#
#    args = parse_args(sys.argv[1:])
#    try:
#        verify = checkargs(args)
#    except Exception:
#        print(verify)
#        sys.exit()
#    all_input = vars(args)
#    n = args.num_sim
#    bases = [0, 1, 2, 3]
#    e = args.error_rate
#    cov = args.coverage
#    theta = args.theta
#    zygosity = args.zygosity
#    mutate_this_node = args.mutate_node
#    mutnode = []
#    for key, value in dict(all_input).items():
#        if value is None or False:
#            del all_input[key]
#    mutate = args.mut_allele
#    readers = pf.read_csv(args.input)
#    rowss = [["0" if x == "." else x for x in row] for row in list(readers)]
#    # Exclude file headers and get individuals and their samples
#    file_exclude_header = [row for row in rowss[2:]]
#    sites_lists = [row[:3] for row in file_exclude_header]
#    sample_lists = [row[4:] for row in file_exclude_header]
#    try:
#        individuals = [i[0] for i in sites_lists]
#    except IndexError:
#        individuals = [i for i in sites_lists]
#    num_sites = list(range(1, len(sites_lists) + 1))
##    print(num_sites)
#    ind_index_dict = {
#        l1: l2 for l1,
#        l2 in itertools.zip_longest(
#            individuals,
#            num_sites,
#            fillvalue=None)}
#    str_sites = []
#    for items in sites_lists:
#        ind_sites = []
#        for item in items:
#            if item in ind_index_dict.keys():
#                ind_sites.append(ind_index_dict[item])
#            else:
#                ind_sites.append(item)
#        str_sites.append(ind_sites)
#    sites = ([[int(j) for j in i] for i in str_sites])
#    for index, ind in enumerate(sites_lists):
#        if mutate_this_node in ind:
#            mutnode = index + 1
#    sam_name = individuals
#    sample_gl = [str(s) for s in sam_name]
#    sample_lb = [s for s in sample_lists]
#    sam_name = sample_gl + sample_lb
#    sam_list = pf.removebrackets(sam_name)
#    sname = (sam_list.replace(", ", "\t")).translate(
#        str.maketrans({"'": None}))
#    input_data = [tuple(l) for l in sites]
#    cNodes = list((i[0] for i in input_data if 0 not in i))
#    if mutnode not in cNodes:
#        print(
#            "Node",
#            args.mutate_node,
#            "is not a child node. Consider using one of",
#            cNodes)
#        sys.exit()
#    else:
#        print("Node to be mutated is a child node. Proceeding!")
#    if args.output:
#        with open(args.output, 'w') as vcf:
#            header_one = first_header(args, zygosity)
#            vcf.write(f"{chr(10).join(header_one)}")
#            header_two = (
#             "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t" + sname)
#            vcf.write("%s\n" % (header_two))
#            counter = 1
#            count = 0
#            for x in tqdm.tqdm(range(n), total=len(range(n))):
#                count += 1
#                # get values from the function (run)
#                ref, node_values, coding = run(
#                    input_data, bases, theta, mutnode, mutate)
#                '''
#                    check if zygosity is given and if value = 1, the genotypes
#                    of the individuals will be the same (always conform to
#                    mutated node if its one of the monozygote
#                    twins). If value = 2, the genotypes are different (
#                    dizygotes treated as different individuals).
#                '''
#                try:
##                    if args.zygosity:
##                    zygo = [item for s in args.zygosity for item in s]
#                    if args.zygosity == None:
#                        raise ValueNotProvided
#                    elif len(zygo) < 3:
#                        raise ValueNotEnough
#                    for i, j in enumerate(node_values.keys()):
#                        for k, x in enumerate(individuals):
#                            if (k == i and x == zygo[2] and
#                                    k == mutnode and zygo[0] == str(1)):
#                                node_values[k + 1] = (
#                                        node_values.get(mutnode))
#                                cod = dict(enumerate(coding))
#                                for q, s in enumerate(coding):
#                                    if q == k:
#                                        coding[q] = cod.get(q-1)
#                            if zygo[0] == str(2):
#                                pass
#                except ValueNotProvided:
#                   print("No values for zygosity were provided")
#                   print()
#                except ValueNotEnough:
#                   print("The number of values for zygosity must be = 3!")
#                   print()
#                                
##                    pass
#                alt, code, inner_node = ggcode(node_values, ref)
#                readers = pf.read_csv(args.input)
#                rowss = list(readers)
#                rowss_as_strings = [row for row in rowss[0:]]
#                rowss_dict = dict()
#                for i in rowss_as_strings:
#                    key = i[0]
#                    val = i[4:]
#                    rowss_dict[key] = val
#                for key, val in rowss_dict.items():
#                    for i, x in enumerate(coding):
#                        if key == i + 1:
#                            rowss_dict[key] = [x for y in val]
#                inner_dict = dict()
#                for k, v in rowss_dict.items():
#                    for i in v:
#                        inner_dict[k] = [i.replace(i, "1") for y in v]
#                all_ones_val = []
#                for x in inner_dict.values():
#                    all_ones_val.append(x)
#                code_results = [[int(j) for j in i] for i in all_ones_val]
#                results = list(zip(["0"] * len(code_results), [str(a).replace(
#                        ' ', '') for a in code_results]))
#                final_results = []
#                for i in results:
#                    final_results.extend([i[0], (i[1]).strip("[]")])
#                merged_final = [":".join(final_results[i:i + 2]) for i in
#                                range(0, len(final_results), 2)]
#                soma = [x.replace('1', '.') for x in merged_final]
#                soma = [x.replace('0', '') for x in soma]
#                ref_val = pf.convert_to_string(ref)
#                ref_string = pf.removebrackets(ref_val)
#                reference = str(ref_string)
#                het, hom = gn.gen_err(e)
#                final_vals_based_on_error = []
#                calculated_error_rates = []
#                for i in coding:
#                    if i not in het.index:
#                        gt_error = hom.loc[[i]]
#                        calculated_error_rates.append(gt_error.values.tolist())
#                    else:
#                        gt_error = het.loc[[i]]
#                        calculated_error_rates.append(gt_error.values.tolist())
#                for z, i in enumerate(calculated_error_rates):
#                    val_based_on_applied_error = []
#                    if not (z + 1) in cNodes:
#                        apply_error_rate = np.random.multinomial(
#                            cov[0], i[0], size=1)
#                        val_based_on_applied_error.append(apply_error_rate)
#                    else:
#                        apply_error_rate = np.random.multinomial(
#                            cov[1], i[0], size=1)
#                        val_based_on_applied_error.append(apply_error_rate)
#                    final_vals_based_on_error.append(
#                        *val_based_on_applied_error)
#                list_of_final_vals = np.array(
#                    final_vals_based_on_error).tolist()
#                ad_rows = list(zip(*list_of_final_vals))
#                ad_rowws = np.array(np.array(*ad_rows)).tolist()
#                str_bases = ["A", "G", "C", "T"]
#                ad_dict = []
#                for y, i in enumerate(ad_rowws):
#                    a_dict = dict(zip(str_bases, i))
#                    ad_dict.append(a_dict)
#                refalt = []
#                refalt.append(reference)
#                refalt.extend(alt.split(","))
#                ads_and_errors = []
#                for i in ad_dict:
#                    ad_list = [i.setdefault(key, 0) for key in refalt]
#                    for k, v in i.items():
#                        if k not in refalt and v > 0:
#                            refalt.append(k)
#                            ad_list.append(v)
#                    ads_and_errors.append(ad_list)
#                for x in ads_and_errors:
#                    if len(x) < len(refalt):
#                        x.append(0)
#                        ads_and_errors.append(x)
#                    else:
#                        pass
#                final_alts = ",".join(refalt[1:])
#                ddcode = re.split(r'\t+', code)
#                ddadcount = list(zip(ddcode, [str(a).replace(
#                        ' ', '') for a in ads_and_errors]))
#                merged_ads_and_codes = []
#                for i in ddadcount:
#                    merged_ads_and_codes.extend([i[0], (i[1]).strip("[]")])
#                mappings = [":".join(merged_ads_and_codes[i:i + 2])
#                            for i in range(0, len(merged_ads_and_codes), 2)]
#                gtad_maps = '\t'.join(mappings)
#                list_range = list(map(str, range(1, 5)))
#                new_code = [[[('0' if b in list_range else b) for b in x]
#                             for x in ddcode] for a in list_range]
#                dcode = new_code[0]
#                lo = ["".join(i) for i in dcode]
#                try:
#                    args.zygosity
#                    zygo = [item for s in args.zygosity for item in s]
#                    if zygo[0] == str(1):
#                        twin_dict2 = dict(zip(individuals, mappings))
#                        g_soma = [x + y for x, y in zip(lo, soma)]
#                        for k, v in enumerate(g_soma):
#                            for s, t in enumerate(ddcode):
#                                if s == k and k == (mutnode - 1):
#                                    g_soma[k] = re.sub(r'.*:', t + ":", v)
#                                for x, y in enumerate(individuals):
#                                    if zygo[2] == y:
#                                        g_soma[x] = re.sub(
#                                                r'.*:', t + ":", v)
#                                        for i in twin_dict2.keys():
#                                            if zygo[0] == str(1):
#                                                if (zygo[2] == i and
#                                                        zygo[1] ==
#                                                        mutate_this_node):
#                                                    twin_dict2[i] = (
#                                                        twin_dict2[zygo[1]])
#                                                elif (zygo[1] == i and
#                                                      zygo[2] ==
#                                                      mutate_this_node):
#                                                    twin_dict2[i] = (
#                                                        twin_dict2[zygo[2]])
#                                                elif (zygo[1] == i or
#                                                      zygo[2] == i and
#                                                      zygo[2] !=
#                                                      mutate_this_node or
#                                                      zygo[1] !=
#                                                      mutate_this_node):
#                                                    twin_dict2[i] = (
#                                                        twin_dict2[zygo[1]])
#                                                else:
#                                                    pass
#                                            if zygo[0] == str(2):
#                                                pass
#                                        mapmaps = list(twin_dict2.values())
#                                        for p, q in enumerate(mapmaps):
#                                            for s, t in enumerate(
#                                                    mappings):
#                                                if p == x and p == s:
#                                                    mapmaps[x] = q.replace(
#                                                                q, t)
#                        gtad_maps = '\t'.join(mapmaps)
#                        gtad_soma = '\t'.join(g_soma)
#                    else:
#                        g_soma = [x + y for x, y in zip(lo, soma)]
#                        for k, v in enumerate(g_soma):
#                            for s, t in enumerate(ddcode):
#                                if s == k and k == (mutnode - 1):
#                                    g_soma[k] = re.sub(r'.*:', t + ":", v)
#                        gtad_maps = '\t'.join(mappings)
#                        gtad_soma = '\t'.join(g_soma)
#                except Exception:
#                    g_soma = [x + y for x, y in zip(lo, soma)]
#                    for k, v in enumerate(g_soma):
#                        for s, t in enumerate(ddcode):
#                            if s == k and k == (mutnode - 1):
#                                g_soma[k] = re.sub(r'.*:', t + ":", v)
#                gtad_maps = '\t'.join(mappings)
#                gtad_soma = '\t'.join(g_soma)
#                last_gtad = "\t".join([gtad_soma, gtad_maps])
#                vcf.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (str(
#                    counter), str(count), str("."), reference, final_alts, str(
#                        "."), str("PASS"), str("."), str("GT" + " :AD"), str(
#                                last_gtad)))
##                pass
#        print("Results have been written to ", args.output)
#
#
#def checkargs(args):
#    
#    '''
#        Get all arguments provided by the user, check validity of
#        arguments, file format, file content and writes results
#        to an output file specified by user or uses default output
#    '''    
#
#    try:
#        
#        if args.seed:
#            pass
#        else:
#            args.seed = int(time.time())
#        if sys.argv[1] == 1:
#            print(help)
#            sys.exit()
#        else:
#            print("Checking user entries...")
#        if len(sys.argv) < 6:
#            print("\t> ERROR: Incorrect number of arguments!",
#                  len(sys.argv), "! at least 6 required.")
#            print(help)
#            sys.exit()
#        else:
#            print("Commands for this simulation includes:")
#            for arg in vars(args):
#                print("\t", arg, getattr(args, arg))
#            print("Entries >OK! Proceeding...")
#            print("Checking", args.input, "file exist...")
#        if not os.path.exists(args.input):
#            print("ERROR - File not found! Please check your path/filename")
#            sys.exit()
#        else:
#            print("File found !!! ")
#            print("Validating file contents...")
#        if os.stat(args.input).st_size == 0:
#            print("File", args.input, "is empty, please check the file!")
#            sys.exit()
#        else:
#            num_cols = 5
#            with open(args.input, 'r') as pedin:
#                if all(col.count('\t') < num_cols - 1 for col in pedin):
#                    print(
#                        "\t",
#                        args.input,
#                        "should contain at least 5 columns. Exiting...")
#                    sys.exit()
#                else:
#                    print(args.input, "is tab separated. Proceeding!")
#        if args.zygosity is not None and len(args.zygosity) not in (0, 3):
#            args.zygosity
#        else:
#            args.zygosity = None
#        
#    except KeyboardInterrupt:
#        sys.exit(1)
#
#        
#def first_header(args, zygosity):
#
#    '''
#    Write vcf header to file. This includes the user supplied input values 
#    for the simulation run
#    '''
#    l1 = "##fileformat=VCFv4.2"
#    l2 = "##phasing=partial"
#    l3 = "##contig=<ID=1,length = " + str(args.num_sim) + ">"
#    l4 = "##vcfsimCommands = -i " + str(args.input) + " -t " + str(
#        args.theta) + " -n " + str(args.num_sim) + " -e " + str(
#        args.error_rate) + " -c " + str(
#        args.coverage) + " -m " + str(args.mutate_node) + " -a " + str(
#        args.mut_allele) + " -z " + str(zygosity) + " -s " + str(
#        args.seed) + " -o " + str(args.output)
#    l5 = "##FILTER=<ID=PASS,Description = "'"All filters passed"'" > "
#    l6 = "##FORMAT=<ID=GT,Number = 1,Type=String,Description = "
#    '"Genotype"'" > "
#    l7 = "##FORMAT=<ID=AD,Number = R,Type=Integer,Description = "
#    '"Allelic depths for the ref and alt alleles in listed order"'">"
#    l8 = "##vcfsimVersion = v0.0.1"
#    header_one = [l1, l2, l3, l4, l5, l6, l7, l8]
#    return header_one
#
#    
#def parse_args(args):
#    
#    #Parse the command line arguments to the program
#    examples = '''example:
#    [python] [vcfsim.py] [input.ped] [theta] [No of simulations]
#    [node with mutation] [output]
#    Example: vcfsim.py input.ped -t 0.001 -N 1000 -n 3 -o output.vcf'''
#    parser = argparse.ArgumentParser(
#        description='Simulating mutation from pedigree and graph-like files',
#        epilog=examples, formatter_class=argparse.RawDescriptionHelpFormatter)
#    optional = parser._action_groups.pop()
#    required = parser.add_argument_group('required arguments')
#    required.add_argument('-i', '--input',
#                          type=pf.valid_extension,
#                          help='input file in ped format.'
#                          ' Must end with .ped',
#                          required=True)
#    required.add_argument('-t', '--theta',
#                          type=float, default=0.001,
#                          help='Controls meiosis simulation'
#                          ' [default: %(default)3f]',
#                          required=True)
#    required.add_argument('-n', '--num_sim',
#                          type=int,
#                          default=1000,
#                          help='Number of simulations'
#                          ' [default: %(default)d]',
#                          required=True)
#    required.add_argument('-m', '--mutate_node',
#                          help='Child node to be mutated',
#                          required=True)
#    required.add_argument('-e', '--error_rate',
#                          type=float, nargs='?',
#                          help='Genotype Error rate',
#                          required= True)
#    required.add_argument('-c', '--coverage',
#                          type=int,
#                          nargs=2,
#                          help='Coverage of sequences',
#                          required=True)
#    optional.add_argument('-a', '--mut_allele',
#                          type=int, choices=range(1, 3),
#                          default=2,
#                          help='Mutate allele in child node.'
#                          ' 1 for Paternal allele or'
#                          ' 2 for maternal allele'
#                          ' [default: %(default)s]',
#                          required=False)
#    optional.add_argument('-o', '--output',
#                          type=pf.valid_output,
#                          default="result.vcf",
#                          help='Output file name with vcf extension'
#                          '[default: %(default)s]',
#                          required = False)
#    optional.add_argument('-v','--version',
#                          action='version',
#                          version='%(prog)s 1.0.1',
#                          help='output version details')
#    optional.add_argument('-V', '--verbose',
#                          action="store_true",
#                          help='Increased simulation verbosity',
#                          required=False)
#    optional.add_argument('-s', '--seed',
#                          type=int, dest="seed",
#                          help='Random seed for simulation run',
#                          required=False)
#    optional.add_argument('-z', '--zygosity',
#                          action='append', nargs=3,
#                          help='Specifies zygosity of twin children if'
#                          ' any. 1 for Monozygotic or 2 for Dizygotic'
#                          ' [default: %(default)s]',
#                          required=False)
#    parser._action_groups.append(optional)
#    return parser.parse_args(args)
#
#if __name__ == '__main__':
#    
#    print("*******************************************")
#    print("\tBegin \033[0;33mpedvcfsim.py\033[0;m(v1.0.1)")
#    print("\tLast updated: August 19, 2018.")
#    print("\tRequires running python 3!\n")
#    print("*******************************************")
#
#    main()


