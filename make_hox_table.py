#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File    	: make_hox_table.py
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

def parse_hmm_results(infile):
	with open(infile) as fh:
		data_dict = AutoVivification()
		species, hox = '',''
		for line in fh:
			if line.startswith('[SPECIES]'):
				species = line.lstrip("[SPECIES]\t").rstrip("\n")
			elif line.startswith('[HMM]'):
				hmm_line = line.lstrip("[HMM]\t").rstrip("\n").split()
				hox = hmm_line[0]
				hox_score = float(hmm_line[1]).rstrip("(").l
				hmm_bitscore = float(hmm_line[3])
				if best_hmm_bitscore < hmm_bitscore:
					best_hmm = hmm
					best_hmm_bitscore = hmm_bitscore
					best_hmm_eval = hmm_eval
			else:
				pass
	return data_dict

def generate_output(data_dict):
	order = ["X1", "X2", "X3", "X4", "X5", "X6a", "X6b", "X7a", "X7b", "X8a", "X8b", "X9", "X10", "X11"]
	hox_order = order
	hmm_found = 0
	output = ''
	for species in sorted(data_dict):
		output += "[SPECIES]\t" + species + "\n" 
		for hmm in order:
			output += "[HMM]\t" + hmm 
			for gene in data_dict[species]:
				if hmm == data_dict[species][gene]['hmm']:
					hmm_found = 1
					output += "\t" + gene +  " ("+str(data_dict[species][gene]['bitscore']) + ")"
			if hmm_found == 0:
				output += "\t-"
			output += "\n"		 
	return output

def write_to_file(outfile, output):
	with open(outfile, "w") as out_fh:
		out_fh.write(output)
	out_fh.close()

if __name__ == "__main__":
	infile = sys.argv[1]
	outfile = sys.argv[2]
	data_dict = parse_hmm_results(infile)
	output = generate_output(data_dict)
	write_to_file(outfile, output)