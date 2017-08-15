#finding the lowest weight path through a weighted directed tree with a start point
# note: levels are numbers cannot be negetive. they are used to make sure it is a tree and add some structure. 
# they(levels) also correspond to time for requests 

class DirectedTree(object):
	def __init__(self):
	#names are keys and the corresponding object is the values
		self.vertex_dict = {}
		self.edge_dict = {}
		self.level_dict = {}
	#writing self.blank_dict[] is hard so get functions are made now i just right self.get_Blank(). 
	def get_Vertex(self, name):
		return self.vertex_dict[name]
		
	def get_Edge(self, name):
		return self.edge_dict[name]
		
	def get_Level(self, name):
		return self.level_dict[name]
	
	#name of edge is always (start,end) because to edges with the same endpoints and different weights are almost always redundant
	class Edge(object):
		def __init__(self, start, end, weight):
			self.start = start 
			self.end = end
			self.weight = weight
			
	#lots of useful information is stored in vertex and level classes.
	class Vertex(object):
		def __init__(self, name, level, weight):
			self.name = name
			#reminder:all children of a vertex in higher levels all parents in lower levels
			self.level = level
			self.weight = weight
			self.children = []
			self.parents = []
			#smallest level of child of a vertex initialized to -1 since it cannot be negetive
			#there is probably a more pythony way to do this but this way works and I can still have level 0 
			self.minlevel = -1

	class Level(object):
		def __init__(self, name):
			self.name = name
			self.vertices = []
			
	#add and delete functions delete using functions written later in the code, because it makes it easier to read
	
	def add_Level(self, name):
		self.level_dict[name] = self.Level(name)
		
	#deletes all vertices in level because why else would you delete a level
	def del_Level(self, name):
		for vertex in self.get_Level(name).vertices[:]:
			self.del_Vertex(vertex)
		del self.level_dict[name]
	
	#creates level if level not already created 
	def add_Vertex(self, name, level, weight=0): 
		if level in self.level_dict.keys():
			self.get_Level(level).vertices.append(name)
		else:
			self.add_Level(level)
			self.get_Level(level).vertices.append(name)
		self.vertex_dict[name]= self.Vertex(name, level, weight)
		
	#deletes all edges using vertex and its part in level
	def del_Vertex(self, name):
		for vertex in self.get_Vertex(name).children[:]:
			self.del_Edge(name,vertex)
		for vertex in self.get_Vertex(name).parents[:]:
			self.del_Edge(vertex,name)
		self.get_Level(self.get_Vertex(name).level).vertices.remove(name)
		del self.vertex_dict[name]
	
	# checks for vertex does not create new ones. 
	#I might try a version that makes new vertices when called so someone can make a graph with just edges and autocreated levels
	def add_Edge(self, start, end, weight=0):
		try: int(weight)
		except ValueError:
			return 'weight is not a number'
		if start not in self.vertex_dict.keys() or end not in self.vertex_dict.keys():
			return'this edge is not between two vertices'
		#assumes levels are numbers
		if self.get_Vertex(start).level > self.get_Vertex(end).level:
			return 'this edge goes from a higher level vertex to a lower level vertex'
		# to keep only edges with smallest or largest weights because the other edge is always wasted
		elif (start, end) in self.edge_dict.keys():
			#other option:
			#if get_Edge((start, end)).weight > weight:
			 if self.get_Edge((start, end)).weight < weight:
				self.get_Edge((start, end)).weight = weight
		else:
			self.edge_dict[(start,end)] = self.Edge(start,end,weight)
			self.get_Vertex(start).children.append(end)
			self.get_Vertex(end).parents.append(start)
			#minlevel stuff here again -1 is arbitrary 
			if self.get_Vertex(end).level < self.get_Vertex(start).minlevel or self.get_Vertex(start).minlevel==-1:
				self.get_Vertex(start).minlevel = self.get_Vertex(end).level
				
	#had a key error here fixed it with copying lists before deleting elements of them			
	def del_Edge(self, start, end):
		del self.edge_dict[(start,end)]
		#try:
		self.get_Vertex(start).children.remove(end)
		self.get_Vertex(end).parents.remove(start)
		#except KeyError:
		#	pass
		
	#some fun fuctions that did not turn out to be useful but were hard to make
	#note this can make the graph stop being a tree be wary 
	#that is why there is the commented part 
	def move_Vertex(self, name, level):
		#if level >= self.get_Vertex(name).minlevel and minlevel != -1:
		#	raise Exception('this will send a higher level vertex to a lower level vertex')
		if level not in self.level_dict.keys():
			self.add_Level(level)
		start_Level = self.get_Vertex(name).level
		self.get_Level(start_Level).vertices.remove(name)
		self.get_Vertex(name).level = level
		self.get_Level(level).vertices.append(name)
	
	#moves all vertices from start level to new level
	def move_Level(self,start, new):
		list=self.get_Level(start).vertices[:]
		for vertex in list:
			self.move_Vertex(vertex, new)
			
	#move all vertices from start level and higher up delta levels down
	#assumes levels are numbers 		
	def move_Levels(self,start, delta):
		sorted_keys = self.level_dict.keys()
		sorted_keys.sort()
		sorted_keys.reverse()
		for level in sorted_keys:
			try:
				if level >= start:
					next = level+delta
					self.move_Level(level, next)
			except ValueError:
				return 'cannot move levels if they are not numbers'
			
#functions for solving finding a maximum weight path

#turns a list of tuples into a list of a number element in the tuple
def list_of_tuples(list,number):
	out= []
	for element in list:
		sub_tuple=element[number]
		out.append(sub_tuple)
	return out

#takes a list of tuples returns tuple with highest first element
def max_first(list):
	weights = list_of_tuples(list,0)
	max_weight = max(weights)
	max_weight_index = weights.index(max_weight)
	tuple = list[max_weight_index]
	return tuple

#takes a directed tree with weighted edges and returns a path with maximum weight by working backwards 
#can probably be cleaned up 
#idea is we make a dictionary entry for each vertex which contains the maximum weight path along each child.
#then choose the maximum and send that info to the parent 
def optimal_weighted_path_edges(tree):
	#initialization sorting to go from the bottom level and making the dict
	dict={}
	for vertex in tree.vertex_dict.keys():
		dict[vertex]=[(0,['>'])]
	tree.level_dict.keys().sort
	sorted_levels=tree.level_dict.keys()[:]
	
	#recursive subfunction goes through bottom level and 
	#adds information to each parent of each bottom level vertex
	#finishes when out of levels
	def sub_function(sorted_levels,dict):
		bottom_level=tree.get_Level(sorted_levels.pop()).vertices
		list=[]	
		for vertex in bottom_level:
			weights_list = dict[vertex][:]
			max_weight_info = max_first(weights_list)
			tree.get_Vertex(vertex).weight = max_weight_info[0]
			prev = max_weight_info[1]
			prev.append(vertex)
			for parent in tree.get_Vertex(vertex).parents:
				weight=tree.get_Edge((parent,vertex)).weight+tree.get_Vertex(vertex).weight
				dict[parent].append((weight,prev))
		
			if len(sorted_levels)==0:
				list.append((max_weight_info[0], prev))
				
		if len(sorted_levels)==0:
			max_weight = max_first(list)
			max_weight[1].reverse()
			prev=max_weight[1]
			history=''
			for part in prev:
				history += str(part) + ' > '
			return max_weight[0], history[:-7], prev
		return sub_function(sorted_levels,dict)	
	return sub_function(sorted_levels,dict)
	
#takes a directed tree with weighted vertices and returns a path with maximum weight 
#if it also has weighted edges replace = with += in  the for loop	
#baisically make all edges the weight of the vertex they go to except for edges with 
#level 0 node for those add both vertices' weights to the edge
#level 0 is assumed lowest level 
def optimal_weighted_path_vertices(tree):
	for edge in tree.edge_dict.keys(): 
		tree.get_Edge(edge).weight=tree.get_Vertex(tree.get_Edge(edge).end).weight
	for top in tree.get_Level(0).vertices:
		for child in tree.get_Vertex(top).children:
			tree.get_Edge((top,child)).weight+=tree.get_Vertex(top).weight
	return optimal_weighted_path_edges(tree)

#assumes levels are numbers
#takes a directed tree with weighted vertices whose children are all vertices of a certain level and below and returns a path with maximum weight
#this was created as a solution for creating a maximum weight set of nonoverlapping requests from a set of requests with weights
#baisically organize jobs with weights on a machine. 
#solution turns jobs which are initially vertices with weights into edges and their levels into vertices
#from this it creates a new level system
#simpler solution can be made it is not organized into a tree but avtually into a set of jobs and times
def optimal_weighted_path_vertices_level(tree):
	newtree = DirectedTree()
	sorted_levels = sorted(tree.level_dict.keys())
	#new vertex at the bottom level for leaves to turn into edges that connect to this vertex
	bottom_level = sorted_levels[-1] + 1
	for level in tree.level_dict.keys():
		newtree.add_Vertex(level,level,1)
	newtree.add_Vertex(bottom_level,bottom_level,1)
	for vertex in tree.vertex_dict.keys():
		#turns vertex into a bunch of edges each edge between the start-level and 
		#each level that can be reached after the job is done it has the weight of the job 
		if tree.get_Vertex(vertex).children:
			for level in sorted_levels:
				if level >= tree.get_Vertex(vertex).minlevel: 
					newtree.add_Edge(tree.get_Vertex(vertex).level, level,tree.get_Vertex(vertex).weight) 
		else:
			newtree.add_Edge(tree.get_Vertex(vertex).level, bottom_level, tree.get_Vertex(vertex).weight)
	soln = optimal_weighted_path_edges(newtree)
	
	#rewriting solution to get an output in terms of vertices not levels
	soln_list=soln[2]
	soln_list.pop()
	out = []
	parents = []
	soln_list.reverse()
	
	for vertex in tree.get_Level(soln_list[1]).vertices:
		if not tree.get_Vertex(vertex).children:
			parents.append((tree.get_Vertex(vertex).weight,vertex))
	max_element = max_first(parents)
	out.append(max_element[1])
	i=2
	while i < len(soln_list):
		parents=[]
		for vertex in tree.get_Level(soln_list[i]).vertices:
			if tree.get_Vertex(vertex).minlevel<=soln_list[i-1]:
				parents.append((tree.get_Vertex(vertex).weight,vertex))
		max_element = max_first(parents)
		out.append(max_element[1])
		i += 1
	out.reverse()
	history = ''
	for part in out:
		history += str(part) + ' > '
	
	return soln[0], history[:-3], out 

#quick test cases
tree = DirectedTree()
for i in range(0,10):
	tree.add_Vertex('vert_'+str(i),i,1)
for i in range(0,10):
	for j in range(0,10):
		if i < j:
			tree.add_Edge('vert_' + str(i),'vert_' + str(j),1)	
print optimal_weighted_path_edges(tree)
