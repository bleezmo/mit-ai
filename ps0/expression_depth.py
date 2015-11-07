import sys

def depth(expr):
	if(isinstance(expr,tuple)):
		x = 1
		maxdepth = 0
		for elem in expr:
			if(isinstance(elem,tuple)):
				curdepth = depth(elem)
				if(maxdepth < curdepth):
					maxdepth = curdepth
		return x+maxdepth
	else:
		return 0

def main():
	print(depth('x')) #0
	print(depth(('expt', 'x', 2))) #1
	print(depth(('+', ('expt', 'x', 2), ('expt', 'y', 2)))) #2
	print(depth(('/', ('expt', 'x', 5), ('expt', ('-', ('expt', 'x', 2),1), ('/', 5, 2))))) #4


main()