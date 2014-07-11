#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, collections
from Bio import SearchIO

hmm_file = sys.argv[1]
hmm_result = SearchIO.read(hmm_file, 'hmmer3-text')
print hmm_result