def tree_ref(tree,elem):
	if(isinstance(elem,(tuple,list))):
		head,*tail = elem
		if(head < len(tree)):
			if(len(tail) == 0):
				return tree[head]
			else:
				return tree_ref(tree[head],tail)
		else:
			return "out of bounds: index: "+head+" tree: "+tree
	elif(isinstance(elem,int)):
		if(elem < len(tree)):
			return tree[elem]
		else:
			return "out of bounds: index: "+elem+" tree: "+tree
	else:
		return "Invalid search params"

def main():
	tree = (((1, 2), 3), (4, (5, 6)), 7, (8, 9, 10))
	print(tree_ref(tree,(3,1))) #9
	print(tree_ref(tree,(1,1,1))) #6
	print(tree_ref(tree,(0))) #((1,2),3)

main()