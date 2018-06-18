# -*- coding: utf-8 -*-
"""
Created on Sun May 20 23:03:07 2018

@author: eyeamnice
"""
import argparse,csv

"""
    Functions required for string manipulations, 
    checking extensions and processing inputs
"""

def convert_to_string(sequence):    
    """
    Converts a DNA sequence represented as a list of values {0, 1, 2, 3, 4}
    to a string of bases {A, C, G, T} and gap character -
    """
    string = ""
    base = ["A","G","C","T","N"]
    for value in sequence:
        for x, y in enumerate(base):
            if value == x:
                string +=y
    return string

def removebrackets(list1):
    return str(list1).replace('[','').replace(']','')

def replacebraces(list1):
    ls = str(list1).replace('[','').replace(']',':')
    return ls

def valid_extension(path):
    if not path.endswith(".ped"):
        raise argparse.ArgumentTypeError("Only .ped files allowed")
    return path

def valid_output(path):
    if not path.endswith(".vcf"):
        raise argparse.ArgumentTypeError("Only .vcf files allowed")
    return path 

def read_csv(filename):
    with open(filename) as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            yield row       
        