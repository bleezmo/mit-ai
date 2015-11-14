# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
	prev_visited = [start]
	agenda = [[start]]
	while len(agenda) > 0:
		path = agenda.pop(0)
		if(path[-1] == goal):
			return path
		else:
			new_paths = []
			for ext_node in graph.get_connected_nodes(path[-1]):
				if(ext_node not in prev_visited):
					new_path = list(path)
					new_path.append(ext_node)
					new_paths.append(new_path)
					prev_visited.append(ext_node)
			[agenda.append(new_path) for new_path in new_paths]
	return "Could not find node "+goal+"!"


## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
	prev_visited = [start]
	agenda = [[start]]
	while len(agenda) > 0:
		path = agenda.pop(0)
		if(path[-1] == goal):
			return path
		else:
			new_paths = []
			for ext_node in graph.get_connected_nodes(path[-1]):
				if(ext_node not in prev_visited):
					new_path = list(path)
					new_path.append(ext_node)
					new_paths.append(new_path)
					prev_visited.append(ext_node)
			agenda = new_paths + agenda
	return "Could not find node "+goal+"!"


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
	agenda = [[start]]
	while len(agenda) > 0:
		# print("current agenda: "+str(agenda))
		path = agenda.pop(0)
		if(path[-1] == goal):
			return path
		else:
			new_paths = []
			for ext_node in graph.get_connected_nodes(path[-1]):
				if(ext_node not in path):
					new_path = list(path)
					new_path.append(ext_node)
					new_paths.append(new_path)
			sorted_paths = []
			while len(new_paths) > 0:
				shortest = 0
				path_index = 0
				count = 0
				for path in new_paths:
					length = graph.get_heuristic(path[-1],goal)
					if (shortest == 0 or length < shortest):
						shortest = length
						path_index = count
					count = count + 1
				# print("inserting into agenda: "+str(new_paths[path_index])+" of length "+str(shortest))
				sorted_paths.append(new_paths[path_index])
				new_paths.pop(path_index)
			agenda = sorted_paths + agenda
	return "Could not find node "+goal+"!"

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
	agenda = [[start]]
	count = 0
	while len(agenda) > 0:
		pop_list = []
		for path in agenda:
			if len(path) < count: pop_list.append(path)
		[agenda.remove(path) for path in pop_list]
		if(len(agenda) == 0): return agenda
		agenda.sort(cmp=lambda path1,path2: \
			graph.get_heuristic(path1[-1],goal)-graph.get_heuristic(path2[-1],goal))
		agenda = agenda[0:beam_width]
		for path in list(agenda):
			if(path[-1] == goal): return path
			agenda.remove(path)
			new_paths = []
			for ext_node in graph.get_connected_nodes(path[-1]):
				if(ext_node not in path):
					new_path = list(path)
					new_path.append(ext_node)
					new_paths.append(new_path)
			[agenda.append(new_path) for new_path in new_paths]
		count = count + 1
	return agenda

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
	total = 0
	count = 1
	while count < len(node_names):
		total = total + graph.get_edge(node_names[count-1],node_names[count]).length
		count = count + 1
	return total

def branch_and_bound(graph, start, goal):
	agenda = [{'elems':[start],'length':0}]
	goal_paths = []
	while len(agenda) > 0:
		path = agenda.pop(0)
		if path['elems'][-1] == goal:
			goal_paths.append(path)
		else:
			new_paths = []
			for ext_node in graph.get_connected_nodes(path['elems'][-1]):
				if(ext_node not in path['elems']):
					elems = list(path['elems'])
					elems.append(ext_node)
					new_paths.append({'elems': elems, 'length': path_length(graph,elems)})
			agenda = new_paths + agenda
	# print("goal paths: "+str(goal_paths))
	return sorted(goal_paths,cmp=lambda path1,path2:\
		path1['length']-path2['length'])[0]['elems']

def a_star(graph, start, goal):
	agenda = [{'elems':[start],'length':0+graph.get_heuristic(start,goal)}]
	visited = set([start])
	smallest = None
	while len(agenda) > 0:
		path = agenda.pop(0)
		if path['elems'][-1] == goal:
			if smallest == None or path['length'] < smallest['length']:
				smallest = path
		else:
			for ext_node in graph.get_connected_nodes(path['elems'][-1]):
				if(ext_node not in path['elems'] and ext_node not in visited):
					visited.add(ext_node)
					elems = list(path['elems'])
					elems.append(ext_node)
					length = path_length(graph,elems)+graph.get_heuristic(ext_node,goal)
					if(smallest == None or length < smallest['length']):
						i = 0
						for p in agenda:
							if(p['length'] > length):
								break
							i += 1
						agenda.insert(i,{'elems': elems, 'length': length})
	return smallest['elems']


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    raise NotImplementedError

def is_consistent(graph, goal):
    raise NotImplementedError

HOW_MANY_HOURS_THIS_PSET_TOOK = ''
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
