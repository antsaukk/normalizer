from functools import *
from itertools import *
import itertools
from collections import OrderedDict

""" checks if object is empty """
def is_empty(object): 
	if object: 
		return False
	else:
		return True

""" splits problem in labels """
def dissect(string): 
	return list(chain.from_iterable([j.split(' ') for j in string.split('\n')]))

""" computes idle string in passive side """
def getIdleString(conf, idle_label):
	strings = conf.split('\n')
	matchings = [idle_label in line.split(' ') for line in strings]
	idle_conf = strings[matchings.index(True)]
	return idle_conf

#bug here if label is not present distinctly - compute label as intersection of all multisets 
""" computes idle label """
def getIdleLabel(col, alphabet):
	matchings = [label in list(alphabet) for label in col]
	return col[matchings.index(True)]

""" splits problem in lines """
def dissectInLines(problem): 
	return [string.split(' ') for string in problem.split('\n')]

""" creates alphabet from problem definition """
def createAlphabet(string):
	return set(filter(lambda x: x != ' ' and x != '\n', string))

""" checks whether all symbols are unique """
def myUnique(sample):
	arr = [e for (s,e) in sample]
	unique = set()
	return not any(x in unique or unique.add(x) for x in arr)

""" removes dublicates from the string"""
def removeDublicates(s):
	return "".join(OrderedDict.fromkeys(s))

""" splits collection into n parts """
def splitInto(string, degree):
	return [string[i:i + degree] for i in range(0, len(string), degree)]

""" computes degree of the graph where problem is defined """
def computeDegree(problem): 
	res = problem.split('\n')
	return len(res[0].split(' '))

""" merges dublicate labels in multiset """
def merge(problem): 
	degree = computeDegree(problem)
	line = [removeDublicates(label) for label in dissect(problem)]
	res = [' '.join(line) for line in splitInto(line, degree)]
	return '\n'.join(res)

""" implementation is taken from more-itertools library """
def flatten(list_of_lists):
    "Flatten one level of nesting"
    return chain.from_iterable(list_of_lists)

