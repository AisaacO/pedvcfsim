# -*- coding: utf-8 -*-
"""
Created on Sun May 20 23:18:59 2018

@author: eyeamnice
Creates a mapping of the genotypes if observed
"""
from proc_funcs import removebrackets

def ggcode(node_values, ref):
    
    called_gens = [i for i in node_values.values()] #store called genotype values
    modified_gen = [] #list to store modified genotype values converted from values in range (0...3) to range(1...4)
    for i in called_gens:
        gen_to_modify = i[0]
        modify_gen = [x+1 for x in gen_to_modify] #Add 1 to genotype values 
        modified_gen.append(modify_gen)
    int_ref = ref[0]
    nums = [[i if i != int_ref+1 else 0 for i in x] for x in modified_gen]
    seen = []
    seen2 = []
    for i,(a,b) in enumerate(nums):
        if a != 0:
            seen.append(a)
        if b != 0:
            seen.append(b)
    [seen2.append(item) for item in seen if item not in seen2]
    for y,(a,b) in enumerate(nums):
        for index, i in enumerate(seen2):                
            if a==i:
                nums[y][0] = index +1
            if b ==i:
                nums[y][1] = index +1
    NewData=[]
    for bigrams in nums:
        NewData.append(str(bigrams).replace(",","|"))
        ax = repr(NewData).replace(' ', '')
        newD= ax.replace(",","\t").replace("'","").replace("[","").replace("]","")
        alt = getalts(modified_gen, ref)
    inode = newD
    l = list(map(str, range(4)))
    for i in l:
        inode = inode.replace(i, ".")
#    print(inode)        
    return alt, newD, inode

def getalts(modified_gen, ref):

    bas=[] # base values 
    int_ref = ref[0] # change reference value from list to integer
#    print(int_ref)
    for i, (x,y) in enumerate(modified_gen):
        l = (x,y) # get tuples in modified genotype values
        for i in l: #loop checks if base value in modified genotypes are not equal to the reference value
            if i ==1 and i != int_ref+1:
                bas.append("A")
            if i ==2 and i != int_ref+1:
                bas.append("G")
            if i ==3 and i != int_ref+1:
                bas.append("C")
            if i ==4 and i != int_ref+1:
                bas.append("T")
    alt = []   #list to store alt values
    [alt.append(item) for item in bas if item not in alt] #checks base value and adds it to alt if its not in alt
    alt_list = removebrackets(alt).replace("'","").strip()
    alts = (alt_list).replace(" ", "")  #remove space from between alt values                  
    return alts
