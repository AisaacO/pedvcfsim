#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, sys, morph, argparse, random, itertools, time, numpy as np, proc_funcs as pf, gen_error as gn
from gt_founders import run
from gt_mapping2 import ggcode
from operator import itemgetter

def main():

    '''
        Get all arguments provided by the user, check validity of
        arguments, file format, file content and writes results
        to an output file specified by user or uses default output
    '''
#    args = parser.parse_args()
#    all_defaults = {}
    all_input = vars(args)
    for key, value in dict(all_input).items():
        if value is None or False:
            del all_input[key]
    seed = args.seed
    if not seed:
        args.seed = int(time.time())
# #        args.seed = 9999
# #        random.seed(args.seed)
    else:
         random.seed(args.seed)
    if sys.argv[1] == 1:
        print(help)
        sys.exit()
    else:
        print("Checking user entries...")
        if len(sys.argv) < 6:
            print("\t> ERROR: Incorrect number of arguments!",len(sys.argv),"! at least 6 required.")
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
       print("ERROR - File not found! Please check your path or confirm your file")
    else :
        print("File found !!! ")
        print("Validating file contents...")
    if os.stat(args.input).st_size == 0:
        print("File",args.input,"is empty, please check the file!")
        sys.exit()
    else:
        num_cols = 5
        with open (args.input, 'r') as pedin:
            if all(col.count('\t') != num_cols-1 for col in pedin):
                print("\t",args.input,"does not contain 6 tabbed columns. Exiting...")
                sys.exit()
            else:
                print( args.input,"is tab separated. Proceeding!")
    n = args.num_sim
    bases = [0,1,2,3]
    e = args.error_rate #0.005
    cov = args.coverage #30
    theta = args.theta
    mutnode = args.mutate_node
    mutate = args.mut_allele
    readers = pf.read_csv(args.input)
    rowss = list(readers)
    headers = rowss[0]
    rest = [row for row in rowss[1:]]
    my_list = [row[:3] for row in rest]
    list2 =[i[0] for i in my_list]
    lex = list(range(1, len(my_list)+1))
    lx = {l1:l2 for l1,l2 in itertools.zip_longest(list2,lex,fillvalue=None)}
    nl = []
    for items in my_list: 
        nn = []
        for item in items:
            if item in lx.keys():
                nn.append(lx[item])
            else:
                nn.append(item)
        nl.append(nn)
    x = ([[int(j) for j in i] for i in nl])
    sam_name = list2
    sample_gl = ["GL/" + str(s) for s in sam_name]
    sample_lb = ["LB/" + str(s) for s in sam_name]
    sam_name = sample_gl + sample_lb
    sam_list = pf.removebrackets(sam_name)
    sample_names = (sam_list.replace(",", "\t")).translate(str.maketrans({"'":None}))
    input_data = [tuple(l) for l in x]
    cNodes = list((i[0] for i in input_data if 0 not in i))
    if not args.mutate_node in cNodes:
        print("Node", args.mutate_node, "is not a child node. Consider using one of", cNodes)
        sys.exit()
    else:
        print("Node to be mutated is a child node. Proceeding!")
    if args.output:
        with open(args.output, 'w') as f:
            l1 = "##fileformat=VCFv4.2"
            l2 = "##FILTER=<ID=PASS,Description=""All filters passed"">"
            l3 = "##vcfsimCommands = -i " + str(args.input) + " -t " +  str(args.theta) + " -n " + str(args.num_sim) + " -e " + str(args.error_rate) + " -c " + str(args.coverage) + " -m " + str(args.mutate_node) + " -a " + str(args.mut_allele) + " -s " + str(args.seed) + " -o " + str(args.output)            
            l4 = "##INFO=<ID=GERMLINE,Number=0,Type=Flag,Description=""Site contains a germline de novo mutation."">"
            l5 = "##INFO=<ID=SOMATIC,Number=0,Type=Flag,Description=""Site contains a somatic de novo mutation."">"
            l6 = "##INFO=<ID=LIBRARY,Number=0,Type=Flag,Description=""Site contains a library de novo mutation."">"
            l7 = "##INFO=<ID=AD,Number=R,Type=Integer,Description=""Allelic depths for the ref and alt alleles in the order listed"">"
            l8 = "##FORMAT=<ID=GT,Number=1,Type=String,Description=""Genotype"">"
            l9 = "##FORMAT=<ID=AD,Number=R,Type=Integer,Description=""Allelic depths for the ref and alt alleles in the order listed"">"            
            l10 = "##contig=<ID=1,length="+ str(args.num_sim) +">"
            l11 = "##vcfsimVersion=< v0.0.1>"
            f.write("%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n" % (l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11))
            data_line = "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t"+sample_names
            f.write("%s\n"%(data_line))
            counter = 1
            count = 0
            for x in range(n):
                count +=1
                ref, node_values, coding = run(input_data,bases,theta, mutnode, mutate) # get values from the function (run)
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
                    year[key]= val
                if 'I' in year: del year['I']
                for key, val in year.items():
                    for i, x in enumerate(coding):
                        if key == i+1: year[key] = [x for y in val]                     
#                            year[key] = [x for y in val]
                inner_dict = dict()
                for k, v in year.items():                    
                    for i in v:
                        i = i.replace(i,"1")
                        inner_dict[k] = [i for y in v]
                vz = []
                for x in inner_dict.values():
                    vz.append(x)
                results = [[int(j) for j in i] for i in vz]
                ddk =["0"]*len(results)                            
                ddad = list(zip(ddk,[str(a).replace(' ','') for a in results]))
                final =[]
                for i in ddad:
                    final.extend([i[0], (i[1]).strip("[]")])
                xx = [":".join(final[i:i+2]) for i in range(0, len(final), 2)]
                soma = [x.replace('1','.') for x in xx]
                soma = [x.replace('0','') for x in soma]
                ref_val = pf.convert_to_string(ref)
                ref_string = pf.removebrackets(ref_val)
                reference = str(ref_string)
                het, hom = gn.gen_err(e)
                final_vals_based_on_error =[]
                calculated_error_rates = []
                for i in coding:
                    if i not in het.index:
                        gt_error = hom.loc[[i]]
                        calculated_error_rates.append(gt_error.values.tolist())
                    else:
                        gt_error = het.loc[[i]]
                        calculated_error_rates.append(gt_error.values.tolist())
                for i in calculated_error_rates:
                    val_based_on_applied_error =[]
                    apply_error_rate = np.random.multinomial(cov, i[0], size=1)
                    val_based_on_applied_error.append(apply_error_rate)
                    final_vals_based_on_error.append(*val_based_on_applied_error)
                list_of_final_vals = np.array(final_vals_based_on_error).tolist()
                ad_rows = list(zip(*list_of_final_vals))
                refalt = []
                refalt.append(reference)
                refalt.extend(alt.split(","))
                ad_rowws = np.array(np.array(*ad_rows)).tolist()
                ddcode = re.split(r'\t+', code)
                all_zero_cols = np.nonzero((np.array(ad_rowws)).sum(axis=0) < 1)
                str_bases = ["A", "G","C", "T"]
                adflags = []
                for i in ad_rowws:
                    ad_dict = []
                    a_dict = dict(zip(str_bases, i))
                    ad_dict.append(a_dict)
                    ds = dict([(key,d[key]) for d in ad_dict for key in d])
                    l = [ds.setdefault(key, 0) for key in refalt ]
                    res = [list(map(d.get, refalt)) for d in ad_dict]
                    rest = list(morph.flatten(res))
                    if all_zero_cols:
                        c = [x for x in i if x not in l]
                        s = [c[0] if len(c) >= 1 and sum(i) <= cov else 0]
                        rest.extend(s)
                    else:
                        pass
                    adflags.append(rest)
#                l = [str(a).replace(' ','') for a in adflags]
                ddadcount = list(zip(ddcode,[str(a).replace(' ','') for a in adflags]))
                merged_ads_and_codes =[]
                for i in ddadcount:
#                    l = (i[1]).strip("[]")
                    merged_ads_and_codes.extend([i[0], (i[1]).strip("[]")])
                mappings = [":".join(merged_ads_and_codes[i:i+2]) for i in range(0, len(merged_ads_and_codes), 2)]
                c = list(map(itemgetter(-1), mappings))
                adf = []
                for x in mappings:
                    if any(int(i) >= 1 for i in c):
                        g = x
                    else:
                        g = x[:-1].strip(',')
                    adf.append(g)
                gtad_maps = '\t'.join(adf)
                l = list(map(str, range(1,4)))
                new_code= [ [ [('0' if b in l else b) for b in x] for x in ddcode] for a in l ]
                dcode = new_code[0]
                lo = ["".join(i) for i in dcode]
                g_soma = [x + y for x, y in zip(lo, soma)]
                gtad_soma = '\t'.join(g_soma)
                last_gtad = "\t".join([gtad_soma, gtad_maps])
#                print(gtad_soma)
#                print(reference, alt, last_gtad)
                f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(str(counter), str(count),str("."),
                                    reference, alt,str("."),str("PASS"),str("."),str("GT"+":AD"),str(last_gtad)))
                
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
                        epilog = examples, formatter_class= argparse.RawDescriptionHelpFormatter)
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-i', '--input', type=pf.valid_extension,
                                help='input file in ped format. Must end with .ped', required = True)
    required.add_argument('-t', '--theta', type= float,  default = 0.001,
                                help='Controls meiosis simulation [default: %(default)3f]', required=True)
    required.add_argument('-n', '--num_sim', type= int, default = 1000,
                                help='Number of simulations [default: %(default)d]', required=True)
    required.add_argument('-m', '--mutate_node', type= int,
                                help='Child node to be mutated', required=True)
    required.add_argument('-e', '--error_rate', type=float, nargs='?',
                                help='Error rate in simulation', required=False)
    required.add_argument('-c', '--coverage', type= float, nargs='?',
                                help='Coverage of sequences', required=False)
    optional.add_argument('-a', '--mut_allele', type=int, choices=range(1, 3),default = 2,
                                help='Mutate allele in child node. 1 for Paternal or 2 for maternal allele [default: %(default)s]', required=False)
    optional.add_argument('-o', '--output', type=pf.valid_output,
                                help='output file name with vcf extension [default: %(default)s]', default= "result.vcf")
    optional.add_argument('-v', '--version', action='version', version='%(prog)s 2.0', help='output version details')
    optional.add_argument('-V', '--verbose',action = "store_true",
                                help='Increased simulation verbosity', required=False)
    optional.add_argument('-s', '--seed', type=int, dest="seed",
                                help='Random seed for simulation run', required=False)
    parser._action_groups.append(optional)

    try:
        args = parser.parse_args()
        main()
    except KeyboardInterrupt:
        sys.exit(1)
