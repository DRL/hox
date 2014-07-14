#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File    	: parse_hmm.py
Author  	: Dominik R. Laetsch, dominik.laetsch at gmail dot com 
Version 	: 0.1
"""

from __future__ import division
import os, sys

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def parse_hmm_table(infile, max_hits):
	with open(infile) as fh:
		data_dict = AutoVivification()
		hit_number = 0
		for line in fh:
			if line.startswith('#'):
				#species = line.lstrip("# ").rstrip("\n").split(".")[0]
				species = line.lstrip("# ").rstrip("\n")
				hit_number = 0
			else:
				data = line.rstrip("\n").split()
				hit_number += 1
				hit_name = data[0]
				hit_hox = data[2]
				hit_eval = data[4]
				hit_bitscore = data[5]
				if hit_number <= max_hits:
					data_dict[species][hit_name][hit_hox]['hit_number'] = hit_number  
					data_dict[species][hit_name][hit_hox]['hit_eval'] = hit_eval 
					data_dict[species][hit_name][hit_hox]['hit_bitscore'] = hit_bitscore
					if len(data) > 20:
						data_dict[species][hit_name]['hit_comments'] = ";".join(data[20:-1])
					else:
						data_dict[species][hit_name]['hit_comments'] = ""       
	return data_dict

def generate_output(data_dict):
	order = ["X1", "X2", "X3", "X4", "X5", "X6a", "X6b", "X7a", "X7b", "X8a", "X8b", "X9", "X10", "X11"]
	hox_order = order[:]
	output =''
	for species in sorted(data_dict):
		output += "[SPECIES] " + species + "\n"
		for gene in data_dict[species]:
			output += "[GENE]\t" + gene + " " + data_dict[species][gene]['hit_comments'] + "\n"
			output += "[\t\tHMM\thit\teval\tbitscore]\n" 
			for hox in order:
				if hox in data_dict[species][gene]: 
					output += "[HMM]\t\t" + hox + "\t" + str(data_dict[species][gene][hox]['hit_number']) + "\t"+  str(data_dict[species][gene][hox]['hit_eval']) + "\t"+  str(data_dict[species][gene][hox]['hit_bitscore']) + "\n"
		output += "###############\n"
	return output

def write_to_file(outfile, output):
	with open(outfile, "w") as out_fh:
		out_fh.write(output)

if __name__ == "__main__":
	infile = sys.argv[1]
	outfile = sys.argv[2]
	max_hits = int(sys.argv[3]) 
	data_dict = parse_hmm_table(infile, max_hits)
	output = generate_output(data_dict)
	write_to_file(outfile, output)