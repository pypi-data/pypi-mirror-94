from fstpso import FuzzyPSO	

def example_fitness( particle ):
	return sum(map(lambda x: x**2, particle))

if __name__ == '__main__':
	
	dims = 10
	FP = FuzzyPSO()
	FP.set_search_space( [[-10, 10]]*dims )	
	FP.set_fitness(example_fitness)	
	result =  FP.solve_with_fstpso(max_iter=100)
	print ("Best solution:", result[0])
	print ("Whose fitness is:", result[1])
