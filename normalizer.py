import io
import sys, getopt
from itertools import *
import functools 
import operator
from problem import *
import collections
from util import *


""" normalization algorithm """
def normalize(input_file):
	""" fetch data from file """
	f = open(input_file, "r")
	inputdat = f.read()
	relaxed_problem, canonical_problem = getData(inputdat)
	reactive = relaxed_problem.getActive()
	repassive = relaxed_problem.getPassive()
	alphaR = relaxed_problem.getAlphabet()
	active = canonical_problem.getActive()
	passive = canonical_problem.getPassive()
	alphaOrig = canonical_problem.getAlphabet()

	""" if cardinality of alphabets differs, reduce problem by removing idle label """
	if (len(alphaR) != len(alphaOrig)):
		new_reactive, new_repassive = reduceRelaxation(reactive, repassive, alphaR)
	else: 
		new_reactive, new_repassive = reactive, repassive

	""" compute configurations of old passive """
	passive_side_conf = dissect(passive)
	""" compute configurations of new passive """
	repassive_side_conf = dissect(new_repassive)
	""" rename candidate """
	renamings = rename(repassive_side_conf, passive_side_conf, new_reactive, new_repassive, passive)

	if is_empty(renamings): 
		return False

	active_configulation, passive_matched, mappings = renamings[0], renamings[1], renamings[2]

	merged = merge(active_configulation)
	expansions = expand(merged)
	active_matched = match(active, expansions)

	if active_matched == active:
		print("Relaxation is reduction of: ")
		print(active_matched + '\n') 
		print(passive_matched + '\n')
		print("Success")
	else:
		print("Relaxation is not reduction of the instance problem")

""" get data from file """
def getData(inputdat): 
	relaxation, original = inputdat.split("\n=>\n")
	alphabet = createAlphabet(relaxation)
	alphabet2 = createAlphabet(original)
	reactive, repassive = relaxation.split('\n\n')
	active, passive = original.split('\n\n')
	r_problem = RelaxedProblem(reactive, repassive, alphabet)
	c_problem = CanonicalProblem(active, passive, alphabet2)

	return (r_problem, c_problem)	

def reduceRelaxation(reactive, repassive, alphabet): 
	""" split labels of relaxation """
	labels = dissect(reactive)		
	""" fetch idle label """
	idle_label = getIdleLabel(labels, alphabet)
	""" compute idle string in active side """
	idle_conf = getIdleString(reactive, idle_label)
	""" compute idle string in passive side """
	idle_string = getIdleString(repassive, idle_label)

	new_reactive = reactive.replace('\n'+idle_conf, '')
	new_reactive = new_reactive.replace(idle_label, '')
	new_repassive = repassive.replace('\n'+idle_string, '')
	new_repassive = new_repassive.replace(idle_label, '')

	return (new_reactive, new_repassive)

""" rename relaxed problem and see if the exists correspondence with the original """
def rename(npa, opa, new_reactive, new_repassive, passive):
	npa_to_list = sorted(list(npa))
	opa_to_list = sorted(list(opa))

	""" create dictionary for renamings 
	  	such that for each label in original alphabet 
	  	there is one set of configurations from the passive side """
	dictionary = collections.OrderedDict([])
	for label in npa_to_list: 
		dictionary[label] = opa_to_list

	""" compute all possible renamings of new labes to old labels, that is (|old labels|)^(|new labels|) """
	results = []
	for substitutions in [zip(dictionary.keys(), letter) for letter in product(*dictionary.values())]: 
		temp = new_reactive 
		temp_b = new_repassive
		subs = []
		for pair in substitutions: 
			temp = temp.replace(*pair) 
			temp_b = temp_b.replace(*pair) 
			subs.append(pair)
		results.append((temp, temp_b, subs))	    

	""" narrow down the search by filtering out the dublicate renamings 
		and fetch the ones where passive sides match """
	results = list(filter(lambda x: myUnique(x[2]), results))
	results = list(filter(lambda x: x[1] == passive, results))
	results = list(flatten(results))
	
	""" compute multiset with maximum length from new passive configurations """
	max_conf = max([conf[1] for conf in results[2]], key=len) 
	""" if this multiset exists in all multisets of new active conf, perform additional reduction <=> special case for FDSO problem """
	if max_conf in dissect(results[0]): 
		configs = [set(conf) for conf in dissect(results[1])] 
		configs = list(filter(lambda x: x != set(max_conf), configs))
		configs = [list(x) for x in configs]
		configs = set(functools.reduce(operator.concat, configs))
		substitute = ''.join(set(max_conf).difference(configs))
		nact = results[0].replace(max_conf, substitute) 
		npass = results[1]
		subs = results[2]
		results = (nact, npass, subs)

	return results

"""	gets contracted version of the problem, which consists of string of multisets of labels
	expands it into string of sets of labels with no multisets """ 
def expand(strng):
	arr = dissectInLines(strng)
	"""lines = []
	for line in arr:
		lines.append([list(word) for word in line])"""
	lines = [[list(word) for word in line] for line in arr]

	"""expansions = []
	for line in lines:
		#print(*line)
		expansions.append(list(itertools.product(*line)))"""
	expansions = [list(itertools.product(*line)) for line in lines]

	strings = [' '.join(el) for el in functools.reduce(operator.iconcat, expansions, [])]
	[strings.append(' '.join(line)) for line in arr]
	return strings

""" for each configuration in original problem try to find one from expanded """
def match(active, actCandidate):
	matchings = [line if line in set(actCandidate) or line[::-1] in set(actCandidate) else '' for line in active.split('\n')] #better sort the strings
	return '\n'.join(matchings)

""" helper """
def usage():
	print('normalizer.py -f <input_file>')

def main():
	try: 
		opts, args = getopt.getopt(sys.argv[1:],"h:f:", ["help", "input_file="])
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit()

	input_file = None

	for opt, arg in opts: 
		if opt in ('-h', '--help'):
			usage()
			sys.exit()
		elif opt in ('-f', '--input_file'):
			input_file = arg
		else:
			print("Unknown option: " + opt)
			sys.exit()


	try:
		output = normalize(input_file)
	except: 
		print("Algorithm malfunctions")


if __name__ == "__main__":
	main()
