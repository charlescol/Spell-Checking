from Levenshtein import distance as lev
from fastDamerauLevenshtein import damerauLevenshtein
from scipy.spatial.distance import hamming
from pyjarowinkler import distance
import math
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("testfile", help = "test file") # fichier de test contenant une liste de mots a corriger
parser.add_argument("-j", "--jaro",  help = "to use Jaro distance", action='store_true')
parser.add_argument("-w", "--winkler",  help = "to use Jaro-Winkler distance", action='store_true')
parser.add_argument("-l", "--levenshtein", help = "to use Levenshtein distance", action='store_true')
parser.add_argument("-d", "--damerauLevenshtein", help = "to use Damerau-Levenshtein distance", action='store_true')
parser.add_argument("-e", "--hamming_normalized", help = "to use Hamming normalized distance", action='store_true')
parser.add_argument("-g", "--hamming", help = "to use Hamming distance", action='store_true')
parser.add_argument("-n", "--post_number", default = 3, help = "number of words selected", type = int)
parser.add_argument("-o", "--pre_number", default = 0, help = "number of words pre-selected by Leveinshtein Distance", type = int)
args = parser.parse_args()

def hamming_dist_normalized(x, y) :
	min_len = min(len(x), len(y))
	return hamming([x[i] for i in range(len(x)) if i < min_len], 
		[y[i] for i in range(len(y)) if i < min_len]) * min_len + abs(len(x) - len(y))

def hamming_dist(x, y) :
	if len(x) == len(y) :
		return hamming([char for char in x], [char for char in y]) * len(x)
	return math.inf

def correct(input_word, func, number_correction = 3) :
	cpu_usage = []
	correction = []
	dictionary = []
	with open('dic.txt', 'r', encoding="utf8") as file :
		dictionary = [line.split() for line in file.readlines()]
	for i in range(len(dictionary)) :
		current_score = func(input_word, dictionary[i][1]) 
		for number in range(number_correction) :
			if len(correction) <= number or current_score <= correction[number][1]:
				correction.insert(number, [dictionary[i][1], current_score, int(dictionary[i][0])])
				if len(correction) >  number_correction :
					correction.sort(reverse=True, key = lambda x: (-x[1],x[2]))
					correction.pop()
				break
	return correction

def open_testfile(test_filname) :
	test_data = []
	solution_data = []
	with open(test_filname, 'r', encoding="utf8") as file :
		for line in file.read().splitlines()  :
			current_line = line.split('\t')
			if len(current_line) != 0 :
				test_data.append(current_line[0])
				if len(current_line) != 1:
					solution_data.append(current_line[1])
	return test_data, solution_data

def save_results(test_data, algorithm_results) :
	with open(args.testfile[:-4] + '_result.txt', 'w') as file :
		for i in range(len(algorithm_results)) :
			file.write(test_data[i] + '\t')
			for y in range(len(algorithm_results[i])) :
				if y ==  len(algorithm_results[i]) - 1:
					file.write(algorithm_results[i][y][0] + '\n')
				else :
					file.write(algorithm_results[i][y][0] + ',')

def main() :
	algorithms = []
	if args.jaro :
		algorithms.append(lambda x,y: 1 - distance.get_jaro_distance(x, y, winkler=False, scaling=0.1))
	if args.winkler :
		algorithms.append(lambda x,y: 1 - distance.get_jaro_distance(x, y, winkler=True, scaling=0.1))
	if args.hamming :
		algorithms.append(lambda x,y: hamming_dist(x, y))
	if args.damerauLevenshtein :
		algorithms.append(lambda x,y: damerauLevenshtein(x, y, similarity=False))
	if args.levenshtein :
		algorithms.append(lambda x,y: lev(x, y))
	if args.hamming_normalized :
		algorithms.append(lambda x,y: hamming_dist_normalized(x, y))
	print(args.testfile)
	test_data, solution_data = open_testfile(args.testfile)
	algorithm_results = []
	for a,it in enumerate(algorithms) :
		if len(algorithms) > 1 :
			print('\n--------------------\n--------------------')
			print('ALGO : ', a)
			print('--------------------\n--------------------')
		for i in range(len(test_data)) :
			if args.pre_number :
				result = correct(test_data[i], lambda x,y: lev(x, y), args.pre_number)
				for current in result :
					current[1] = it(test_data[i], current[0])
				result.sort(reverse=True, key = lambda x: (-x[1],x[2]))
				result = result[:args.post_number]
			else :
				result = correct(test_data[i], it, args.post_number)
			algorithm_results.append(result)
			if len(algorithms) > 1 :
				print('\n--------------------\n--------------------')
				print(algorithm_results)
				print('--------------------\n--------------------')
			else :
				save_results(test_data, algorithm_results)					

main()





