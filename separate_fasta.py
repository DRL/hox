#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, collections

def parse_file(infile):
	data_dict = collections.defaultdict(dict) 
	seq = ''
	header = ''
	genes = []
	with open(infile) as fh:
		for line in fh:
			line = line.rstrip("\n")
			if (line.startswith(">")):
				if (seq):
					for gene in genes:
						data_dict[gene][header] = seq
					seq = ''
				header = line.rstrip("\n")
				genes = header.split("_")[1:]
			else:
				#line = line.replace("X","")
				seq = seq + line
	return data_dict

if __name__ == "__main__":
	infile = sys.argv[1]
	data = parse_file(infile)
	for gene in data:
		out = open(infile + "." + gene + ".fa", 'w')
		for header in data[gene]:
			out.write(header + "\n" + data[gene][header] + "\n")
