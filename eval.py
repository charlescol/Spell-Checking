import argparse
from fastDamerauLevenshtein import damerauLevenshtein

parser = argparse.ArgumentParser()
parser.add_argument("testfile", help = "test file") # fichier de test généré par corrige.py
parser.add_argument("correctionfile", help = "correction file")# fichier de correction contenant motDeBase \t motAcorriger
args = parser.parse_args()

def calcul_score(algorithm_results, solution_results) :
	total_bonus = 0
	total_malus = 0
	score = []
	total_right_answers = 0
	total_false = 0
	for i in range(len(algorithm_results)) :
		print(algorithm_results[i], " ", solution_results[i])
		for y in range(len(algorithm_results[i])) :
			if algorithm_results[i] == solution_results[i] :
				total_bonus += (1/(y+1))
				total_right_answers += 1
				break
			elif y == len(algorithm_results[i]) - 1 :
				total_malus += damerauLevenshtein(algorithm_results[i][0], solution_results[i], similarity=False)/10
				total_false += 1
		score.append(total_bonus - total_malus)
	print('total right : ', total_right_answers)
	print('total false : ', total_false)
	print('total score : ', total_bonus - total_malus)
	print('total bonus : ', total_bonus)
	print('total malus : ', total_malus)
	print('-----------------------\n-----------------------')
	print('Score evolution : ', score)


def main() :
	algorithm_results = []
	solution_results = []
	with open(args.testfile, 'r', encoding="utf8") as file : 
		for line in file.read().splitlines() :
			algorithm_results.append(line.split('\t')[1].split(','))
	with open(args.correctionfile, 'r', encoding="utf8") as file :
		for line in file.read().splitlines() :
			solution_results.append(line.split('\t')[1])

	calcul_score(algorithm_results, solution_results)

main()